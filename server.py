# server
# coding:utf-8
# Ovanstående rad är ISO-kodning för att åäö ska funka.

import thread
import sys

from socket import *
from copy import copy
from threading import *
from time import *
from groups import *

from kartkomponent.databasmethod import *
import os
import simplejson as json

# Kodkommentarer
#
# status har tre värden: 
# 0 = utloggad 
# 1 = inaktiv - ej implementerad än.
# 2 = aktiv 

ClientMutex = BoundedSemaphore(1)

# Köfkn ----------------------------------------------------------------------



# ATOMISKA FUNKTIONER --------------------------------------------------------

# Broadcast. Atomisk.
def atomic_sendAll(message):
	if message:
		print "To all: " + message
	ClientMutex.acquire()
	for i in range(len(socketArray)):
		if(socketArray[i].status > 0): # Skillnad mellan active och inactive
			socketArray[i].socket.send(message)
	ClientMutex.release()

# Skickar till en hel grupp. Atomisk.
def atomic_sendToGroup(message,group):
	ClientMutex.acquire()
	temp = list()
	for n in get_group_users(group):
		temp.append(n.name)

	for n in temp:
		index = search(n)
		print "To " + n + ": " + message
		if(socketArray[index].status > 0):  # Skillnad mellan active och inactive
			socketArray[index].socket.send(message)

	ClientMutex.release()

# Skickar till enskild användare. Atomisk.
def atomic_sendTo(message,client):
	if message:
		sendToGrp = False
		ClientMutex.acquire()
		index = search(client)
		if(index != -1):
			print "To " + socketArray[index].name + ": " + message
			if(socketArray[index].status > 0):  # Skillnad mellan active och inactive
				socketArray[index].socket.send(message)
		else:
			temp = list()
			for n in get_group_all():
				temp.append(n.name) 
			if(client in temp):
				sendToGrp = True
		ClientMutex.release()
		if(sendToGrp):
			atomic_sendToGroup(message, client)

# Anropas när klient loggar ut eller tappar kontakten. Atomisk.
def atomic_disconnect(client):

	ClientMutex.acquire()

	index = search(client)
	if(index != -1):
		socketArray[index].status = 0
		sendAll("Server message: " + str(socketArray[index].name) + " disconnected.")
		socketArray[index].socket.close()
	ClientMutex.release()


# Sätter client:s lastwhisper. Atomisk.
def atomic_setReply(client, replier):
	ClientMutex.acquire()
	socketArray[search(client)].lastWhisper = replier
	ClientMutex.release()


# Tar bort avloggade klienter. Atomisk.
def atomic_reGroupClients():
	ClientMutex.acquire()
	delete = list()
	for i in range(len(socketArray)):
		if(not socketArray[i].isAlive()):
			delete.append(i)

	j = 0
	for i in delete:
		i = i-j
		print "Delete " + socketArray[i].name
		socketArray.pop(i)
		j = j+1
	ClientMutex.release()

# Replikeringsfunktion. Replikerar från denna server till backupen varje minut. Atomisk.
def copydb():
	print 'Replikerar databas.db'
	ClientMutex.acquire()
	os.system('rsync -a data.db nikpe890@sysi-04.sysinst.ida.liu.se:TDDD36Grupp2/')
	ClientMutex.release()
	sleep(60)


# Atomisk ------
def atomic_addUserToGroup(group,user):
	ClientMutex.acquire()
	session = Session()
	try:
		u=session.query(User).filter_by(name=user).first()
		g=session.query(Group).filter_by(name=group).first()
		u.groups.append(g)
	except:
		feedback.append(user + " couldn't join the group " + group)
	session.commit()
	session.close()
	ClientMutex.release()

# ----------------------------------------------------------------------------


# Funktioner som endast får anropas från atomiska funktioner------------------

# Broadcast.
# OBS! Ej atomisk! Får endast köras i atomiska läs-funktioner.
def sendAll(message):
	if message:
		print "To all: " + message
	for i in range(len(socketArray)):
		if(socketArray[i].status > 0): # Skillnad mellan active och inactive
			socketArray[i].socket.send(message)


# Söker efter användarnamn och returnerar index.
# OBS! Ej atomisk! Får endast köras i atomiska läs-funktioner.
def search(client):
	for i in range(len(socketArray)):
		if(socketArray[i].name == client):
			if(socketArray[i].status > 0): # Skillnad mellan active och inactive
				return i
	return -1

# Söker efter användarnamn och returnerar användare, oavsett om dene är aktiv eller inte.
# OBS! Ej atomisk! Får endast köras i atomiska läs-funktioner.
### FUNKAR EJ ÄN!!! ###
def getClient(client):
	for i in range(len(socketArray)):
		if(socketArray[i].name == client):
			return socketArray[i]
	return -1

# Gör en lista och skriver om folk är online.
# OBS! Ej atomisk! Får endast köras i atomiska läs-funktioner.
def statusList():
	String = ""
	for i in range(len(socketArray)):
		String += str(i) + ": " + str(socketArray[i].name)
		if(socketArray[i].status > 0):
			String += " (Active)"
		else:
			String += " (Disconnected)"
		if(socketArray[i].isAlive()):
			String += " isAlive"
		String += "\n"
	return String

# ----------------------------------------------------------------------------

# å,ä -> a, ö -> o
def toEnglish(string):
	for c in string:
		if(c=='å' or c=='ä'):
			c = 'a'
		elif(c=='ö'):
			c = 'o'
	return string

# Skapar en lista med användare eller grupper
def listCMD(arg):
	ip = list()

	# Skickar man inte med argument till /list får man alla användare som är online
	if not arg:
		# Atomisk ------
		ClientMutex.acquire()
		for s in socketArray:
			if(s.isAlive()):
				ip.append(s.name + " " + str(s.ADDR))
		ClientMutex.release()
		# --------------


	# Skickar man med argumentet "all" till /list får man alla användare som varit online.
	elif(arg[0].startswith('all')):
		# Atomisk ------
		ClientMutex.acquire()
		temp = list()
		for n in get_user_all():
			temp.append(n.name) 

		for t in temp:
			if(search(t) > -1):
				ip.append("/online " + t + '\n')
			else:
				ip.append("/online/ " + t + '\n')
		ClientMutex.release()
		# --------------


	# Skickar man med argumentet "group" till /list får man alla grupper.
	elif(arg[0].startswith('group')):
		# Skickar man med några gruppnamn returneras medlemmarna i dessa.
		if(len(arg) > 1):
			arg.pop(0)
			# Atomisk ------
			ClientMutex.acquire()
			for n in arg:
				ip.append("Group " + n + ":")
				temp = get_group_users(n)
				if temp:
					for t in temp:
						ip.append(t.name)
			ClientMutex.release()
			# --------------

		else:
			# Atomisk ------
			ClientMutex.acquire()
			temp = get_group_all()
			if temp:
				for g in temp:
					ip.append(g.name)
			ClientMutex.release()
			# --------------
		
	# Skickar man med argumentet "user" till /list får man alla användare.
	elif(arg[0].startswith('user')):
		# Skickar man med några användarnamn returneras de grupper de är med i.
		if(len(arg) > 1):
			arg.pop(0)
			# Atomisk ------
			ClientMutex.acquire()
			for n in arg:
				ip.append("User " + n + ":")
				temp = get_user_groups(n)
				if temp:
					for t in temp:
						ip.append(t.name)
			ClientMutex.release()
			# --------------

		else:
			# Atomisk ------
			ClientMutex.acquire()
			temp = get_user_all()
			if temp:
				for u in temp:
					ip.append(u.name)
			ClientMutex.release()
			# --------------
	return ip



def addCMD(arg):
	feedback = list()
	if len(arg) < 2:
		return

	# Syntax: "add user" username group1 group2 ...
	# Lägger till username i grupperna group1 group2 ...
	if(arg[0] == 'user'):
		# Lagrar alla usernames i temp. Vore bra med en färdig fkn databasen.
		temp = list()
		for n in get_user_all():
			temp.append(n.name) 
		if(arg[1] in temp):
			arg.pop(0)
			user = arg.pop(0)
			for group in arg:
				atomic_addUserToGroup(group,user)
		else:
			feedback.append("No user named " + arg[1])

	# Syntax: "add to" group username1 username2 ...
	# Lägger till username1, username2 ... i gruppen group
	elif(arg[0] == 'to'):
		# Lagrar alla grupper i temp. Vore bra med en färdig fkn databasen.
		temp = list()
		for n in get_group_all():
			temp.append(n.name) 
		if(arg[1] in temp):
			arg.pop(0)
			group = arg.pop(0)
			for user in arg:
				atomic_addUserToGroup(group,user)
		else:
			feedback.append("No group named " + arg[1])

	return feedback

def removeCMD(arg):
	feedback = list()
	if len(arg) < 2:
		return

	# Syntax: "/remove from " grupp user1 user2 ...
	elif(arg[0] == 'from'):
		# Lagrar alla usernames i temp. Vore bra med en färdig fkn databasen.
		temp = list()
		for n in get_group_all():
			temp.append(n.name) 
		if(arg[1] in temp):
			arg.pop(0)
			group = arg.pop(0)
			for username in arg:
				# Atomisk ------
				ClientMutex.acquire()
				session = Session()
				try:
					u=session.query(User).filter_by(name=username).first()
					g=session.query(Group).filter_by(name=group).first()
					u.groups.remove(g)
				except:
					feedback.append(username + "is not member of " + group)
				session.commit()
				session.close()
				ClientMutex.release()
				# --------------
		else:
			feedback.append("No group named " + arg[1])

	return feedback


HOST = '127.0.0.1'
PORT = 2150
if(len(sys.argv) > 1):
	PORT = int(sys.argv[1])
BUFF = 1024
ADDR = (HOST, PORT)

print "Binding serverSocket to: ", ADDR

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(5)

connectionQueue = list() # Låter endast en användare per IP ansluta åt gången
socketArray = list() # Innehåller alla sockets vi kör

# Sessionsklassen
class sessionClass(Thread):
		
	groups = list()
	lastWhisper = "ADMIN"
	status = 0

	def __init__(self, _socket, _ADDR):
		self.socket = _socket
		self.ADDR = ADDR
		Thread.__init__(self)


	def sendBack(self, message):
		#print "Back to " + self.name + ": " + message
		self.socket.send(message)

	# Replikerar alla Message:s.
	def replicateMsg(self, arg):
		intarg = list()
		for a in arg:
			try:
				intarg.append(int(a))
			except: print "a är inget nummer"
		msgQueue = list()

		try:	
			session = Session()
			# Atomisk ------
			ClientMutex.acquire()
			msgQueue.extend(session.query(Message).filter_by(receiver=self.name).all())
			msgQueue.extend(session.query(Poi).all())
			ClientMutex.release()
			# --------------
			session.close()
		except Exception, e: print e

		# Sorterar ut meddelanden som klienten redan har
		while(len(intarg) != 0):
			j = -1
			for i in range(len(msgQueue)):
				if(msgQueue[i].id == intarg[0]):
					j = i
					break
			if(j!=-1):
				msgQueue.pop(j)
			intarg.pop(0)

		for m in msgQueue:
			data = json.dumps(class2dict(m))
			self.sendBack(data + '\n')


	
	# Sköter inloggningen.
	def authentication(self):
			
		CLIENTNAME = "Player1"
		try:
			
			while 1:
				self.socket.send("Login: (name pass): ")
				name_pass = ""
				i = 0
				while(name_pass == "" and i<20):
					name_pass = self.socket.recv(BUFF)
					print "Login try: #" + name_pass + "#"
					i = i+1
				# Kicka om man inte skriver något efter 20 försök.
				if(name_pass == ""):
					return "/ERROR"

				# Gör om Message till sträng
				if(name_pass[0] == '{'):
					msg = json.loads(name_pass)
					try:
						if(msg["type"] == "login"):
							name_pass = msg["sender"]+' '+msg["content"]["message"]
					except KeyError, e: print "Unknown datatype"

				temp = name_pass.split(' ')
				uname = temp[0]

				if(len(temp) == 2):
					login = temp[1]

					loginSession = Session()
					# Atomisk ------
					ClientMutex.acquire()
					user = loginSession.query(User).filter_by(name = uname).first()
					username = ""

					try:
						username = user.name
					except Exception, e: pass

					if(username == uname and search(uname) == -1):
						p=loginSession.query(User).filter_by(name=uname).first()
						try:
							if(login == p.password):
								self.name = uname
						except Exception, e: pass

					ClientMutex.release()
					# --------------
					loginSession.close()

				if(self.name == uname):
					return uname
		except Exception, e:
			print "Client lost: " + CLIENTNAME + "\nException: " + str(e)	
		return "/ERROR"


	# Behandlar övergripande kommunikationen med och mellan klienterna. Sköter även kommandon.
	def handler(self,zero):
		if 1:#try:
			atomic_sendAll("Server message: " + str(self.name) + " connected.")
			self.sendBack("Inloggad på " + str(ADDR))

			while 1:
				data = self.socket.recv(BUFF)
				if(data.startswith('/add')):
					msg = data.split(' ')
					msg.pop(0)
					response = addCMD(msg)
					for i in response:
						self.sendBack(str(i) + "\n")
				elif(data.startswith('/cleanup')):
					thread.start_new_thread(atomic_reGroupClients, ())
				elif(data.startswith('/delete')):
					msg = data.split(' ')
					msg.pop(0)
					response = removeCMD(msg)
					for i in response:
						self.sendBack(str(i) + "\n")

				elif(data.startswith('/ip')):
					msg = data.split(' ', 1)
					if(len(msg) > 1):
						# Atomisk ------
						ClientMutex.acquire()
						ip = socketArray[search(msg[1])].ADDR
						ClientMutex.release()
						# --------------
						self.sendBack(msg[1] + " " + str(ip))
				elif(data.startswith('/kick')):
					msg = data.split(' ', 1)
					if(len(msg) > 1):
						atomic_disconnect(msg[1])

				elif(data.startswith('/list')):
					msg = data.split(' ')
					msg.pop(0)
					ip = listCMD(msg)
					for i in ip:
						self.sendBack(str(i))

				elif(data.startswith('/ping')):
					msg = data.split(' ', 1)
					if(msg[0] == '/ping/'):
						#i =  time()-float(msg[1])
						self.sendBack("/ping " + msg[1])
					else:
						# Atomisk ------
						ClientMutex.acquire()
						temp = search(msg[1])
						ClientMutex.release()
						# --------------
						if(temp != -1):	self.sendBack("/online " + msg[1])
						else:	self.sendBack("/online/ " + msg[1])
				elif(data.startswith('/quit')):
					break
				elif(data.startswith('/reply')):
					msg = data.split(' ', 1)
					if(len(msg)>1):
						i = search(self.lastWhisper)
						atomic_setReply(self.lastWhisper, self.name)
						atomic_sendTo(self.name + " (w): " + msg[1], self.lastWhisper)
						self.sendBack("You whispered to " + self.lastWhisper)
				# Replikering mot klienten
				elif(data.startswith('/sync')):
					msg = data.split(' ')
					msg.pop(0)
					self.replicateMsg(msg)

				elif(data.startswith('/whisper')):
					msg = data.split(' ',2)
					if(len(msg)>2):
						atomic_setReply(msg[1], self.name)
						atomic_sendTo(self.name + " (w): " + msg[2], msg[1])
						self.sendBack("You whispered to " + msg[1])
				# json-strängar! Startar med '{'. Vbf message
				elif(data.startswith('{')):
					msg = json.loads(data)
					# Atomisk ------
					ClientMutex.acquire()
					try:
						if(msg['type']=='text'):
							addMessage(msg["sender"], msg["receiver"], 'text', "change", datetime.now(), msg["content"]["subject"], msg["content"]["message"], 1)
						else:
							addPoi(msg["coordx"], msg["coordy"], msg["type"], datetime.now(), msg["type"], msg["sub_type"])
					except KeyError, e: pass
					ClientMutex.release()
					# --------------
				elif(data != ""):
					atomic_sendAll(self.name + ": " + data)
		#except Exception, e:
		#	print "client lost (handler): " + str(e)

	# körs när man anropar start()
	def run(self):
		self.name = ""
		while(self.name == ""):
			self.name = self.authentication()
			print "Logged in: " + self.name
		if(self.name != "/ERROR"):
			self.handler(0)
		atomic_disconnect(self.name)

print "Servermeddelande: Servern är redo."


# Lyssnar efter klienter som vill ansluta.
def listenToClients():
	while 1:
		socket, ADDR = copy(serverSocket.accept())
		print statusList()
		
		# Atomisk ------ (reGroup kan råka ta bort socketen om de körs samtidigt)
		ClientMutex.acquire()
		socketArray.append(sessionClass(socket, ADDR))
		socketArray[len(socketArray)-1].status = 2
		socketArray[len(socketArray)-1].start()
		ClientMutex.release()
		# --------------

thread.start_new_thread(listenToClients, ())

# Här startar replikeringen.
#thread.start_new_thread(copydb, ())

SERVERRUN = 1

while SERVERRUN:
	String = raw_input()
	if(String.startswith("x")):
		SERVERRUN = 0
	elif(String.startswith("r")):
		thread.start_new_thread(atomic_reGroupClients, ())
	elif(String.startswith("l")):
		print statusList()

serverSocket.close()
