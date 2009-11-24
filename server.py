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

from read_db import *
import os

# Kodkommentarer
#
# status har tre värden: 
# 0 = utloggad 
# 1 = inaktiv - ej implementerad än.
# 2 = aktiv 

ClientMutex = BoundedSemaphore(1)

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


# Skickar till enskild användare. Atomisk.
def atomic_sendTo(message,client):

	ClientMutex.acquire()
	index = search(client)
	if message:
		print "To " + socketArray[index].name + ": " + message
	if(socketArray[index].status > 0):  # Skillnad mellan active och inactive
		socketArray[index].socket.send(message)
	ClientMutex.release()


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

# Replikeringsfunktion. Replikerar från denna server till backupen. Atomisk.
def copydb():
	print 'Replikerar databas.db'
	ClientMutex.acquire()
	os.system('rsync -a data.db nikpe890@sysi-04.sysinst.ida.liu.se:TDDD36Grupp2/')
	ClientMutex.release()
	sleep(60)

# ----------------------------------------------------------------------------


# Funktioner som endast får anropas från atomiska funktioner------------------

# Broadcast.
# OBS! Ej atomisk! Får endast köras i atomiska läs-funktioner.
def sendAll(message):
	if message:
		print "To all: " + message
	for i in range(len(socketArray)):
		if(socketArray[i].status > 0): # Skillnad mellan active och inactive
			print "Send all: " + str(i)
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
		for s in socketArray:
			if(s.isAlive()):
				ip.append(s.name + " " + str(s.ADDR))
			else:
				ip.append("/ERROR")
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
				for t in temp:
					ip.append(t.name)
			ClientMutex.release()
			# --------------

		else:
			# Atomisk ------
			ClientMutex.acquire()
			for g in get_group_all():
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
				for t in temp:
					ip.append(t.name)
			ClientMutex.release()
			# --------------

		else:
			# Atomisk ------
			ClientMutex.acquire()
			for u in get_user_all():
				ip.append(u.name)
			ClientMutex.release()
			# --------------
		

	return ip

#HOST = '130.236.218.114'
HOST = '127.0.0.1'
#HOST = '130.236.189.22'
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

#session=Session()
#print session.query(User).all()
print USERS
#session.close()

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
		print "Back to " + self.name + ": " + message
		self.socket.send(message)
	
	#Sköter inloggningen.
	def authentication(self):
			
		CLIENTNAME = "Player1"
		try:
			
			while 1:
				self.socket.send("Type a name: ")
				CLIENTNAME = ""
				i = 0
				# Följande loop gör så att man slipper klienter som försöker ansluta och sedan bara lämna.
				# Av någon anledning skickar dessa klienter en stadig ström av tomma strängar.
				while(CLIENTNAME == "" and i<20):
					CLIENTNAME = self.socket.recv(BUFF)
					print "Login try: #" + CLIENTNAME + "#"
					i = i+1
				# Kicka om man inte skriver något efter 20 försök.
				if(CLIENTNAME == ""):
					return "/ERROR"
				session = Session()
				if(is_user(CLIENTNAME)):
					self.socket.send("Type your password " + CLIENTNAME)
					# Läser in login och gör om åäö.
					login = toEnglish(self.socket.recv(BUFF))
					

					# Atomisk ------
					ClientMutex.acquire()
					if(search(CLIENTNAME) == -1):
						if(login == get_password(CLIENTNAME)):
							self.name = CLIENTNAME
					
					ClientMutex.release()
					# --------------

					
					if(self.name == CLIENTNAME):
						return CLIENTNAME
				session.close()
		except Exception, e:
			print "Client lost: " + CLIENTNAME + "\nException: " + str(e)	
		return "/ERROR"


	#Behandlar övergripande kommunikationen med och mellan klienterna. Sköter även kommandon.
	def handler(self,zero):
		try:
			atomic_sendAll("Server message: " + str(self.name) + " connected.")
			self.sendBack("Inloggad på " + str(ADDR))

			while 1:
				data = self.socket.recv(BUFF)
				if(data.startswith('/cleanup')):
					thread.start_new_thread(atomic_reGroupClients, ())
				elif(data.startswith('/quit')):
					break
				elif(data.startswith('/status')): 
					self.sendBack("You are number " + str(search(self.name)))
				elif(data.startswith('/list')):
					msg = data.split()
					msg.pop(0)
					ip = listCMD(msg)

					for i in ip:
						self.sendBack(str(i))

				elif(data.startswith('/whisper')):
					msg = data.split(' ', 2)
					if(len(msg)>2):
						atomic_setReply(msg[1], self.name)
						atomic_sendTo(self.name + " (w): " + msg[2], msg[1])
						self.sendBack("You whispered to " + msg[1])
				elif(data.startswith('/reply')):
					msg = data.split(' ', 1)
					if(len(msg)>1):
						i = search(self.lastWhisper)
						atomic_setReply(self.lastWhisper, self.name)
						atomic_sendTo(self.name + " (w): " + msg[1], self.lastWhisper)
						self.sendBack("You whispered to " + self.lastWhisper)
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
				elif(data.startswith('/kick')):
					msg = data.split(' ', 1)
					if(len(msg) > 1):
						atomic_disconnect(msg[1])
				elif(data.startswith('/ip')):
					msg = data.split(' ', 1)
					if(len(msg) > 1):
						# Atomisk ------
						ClientMutex.acquire()
						ip = socketArray[search(msg[1])].ADDR
						ClientMutex.release()
						# --------------
						self.sendBack(msg[1] + " " + str(ip))

				elif(data != ""):
					atomic_sendAll(self.name + ": " + data)
		except Exception, e:
			print "client lost (handler): " + str(e)

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


#Lyssnar efter klienter som vill ansluta.
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
