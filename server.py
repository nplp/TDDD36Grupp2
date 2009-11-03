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

# Kodkommentarer
#
# status har tre värden: 
# 0 = utloggad 
# 1 = inaktiv
# 2 = aktiv 

ClientMutex = BoundedSemaphore(1)




# ATOMISKA FUNKTIONER --------------------------------------------------------

# Broadcast. Atomisk.
def atomic_sendAll(message):
	print "To all: " + message

	ClientMutex.acquire()
	for i in range(len(socketArray)):
		if(socketArray[i].status > 0 and i != 0): # Skillnad mellan active och inactive
			socketArray[i].socket.send(message)
	ClientMutex.release()


# Skickar till enskild användare. Atomisk.
def atomic_sendTo(message,client):

	ClientMutex.acquire()
	index = search(client)
	print "To " + socketArray[index].name + ": " + message
	if(socketArray[index].status > 0):  # Skillnad mellan active och inactive
		socketArray[index].socket.send(message)
	ClientMutex.release()


# Söker efter användarnamn och returnerar index. Atomisk.
def atomic_search(client):
	ClientMutex.acquire()
	i = search(client)
	ClientMutex.release()
	return i # <== utanför semaphoren! Inte coolt!


# Anropas när klient loggar ut eller tappar kontakten. Atomisk.
def atomic_disconnect(client):

	ClientMutex.acquire()

	index = search(client)
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
#def atomic_reGroupClients():
#	ClientMutex.acquire()
#	for i in range(len(socketArray)):
#		if(not socketArray[i].isAlive()): 
#			socketArray[i].pop()
#	ClientMutex.release()

# ----------------------------------------------------------------------------


# Funktioner som endast får anropas från atomiska funktioner------------------

# Broadcast.
# OBS! Ej atomisk! Får endast köras i atomiska läs-funktioner.
def sendAll(message):
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

# ----------------------------------------------------------------------------

def statusList():
	String = ""
	for i in range(len(socketArray)):
		String += str(i) + ": " + str(socketArray[i].name)
		if(socketArray[i].status > 0):
			String += " (Active)"
		else:
			String += " (Inactive)"
		if(socketArray[i].isAlive()):
			String += " isAlive"
		String += "\n"
	return String

HOST = '130.236.216.83'
#HOST = '127.0.0.1'
PORT = 2147
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
openfile = open('users')
USERS = openfile.readlines()
USERLOGIN = dict()
USERNAMES = list()

for s in USERS:
	temp = (s.split(' ',1))
	USERLOGIN[temp[0]] = temp[1]
	USERNAMES.append(temp[0])

print USERNAMES

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
					print "Login try: " + CLIENTNAME
					i = i+1
				# Kicka om man inte skriver något efter 20 försök.
				if(CLIENTNAME == ""):
					return "/ERROR"
				print str(atomic_search(CLIENTNAME)-1)
				if(atomic_search(CLIENTNAME) == -1 and CLIENTNAME in USERNAMES):
					self.socket.send("Type your password " + CLIENTNAME)
					if(self.socket.recv(BUFF) + "\n" == USERLOGIN[CLIENTNAME]):
						self.name = CLIENTNAME
				# Fel: Två klienter kan logga in med samma acc om de gör det samtidigt.
						return CLIENTNAME
		except Exception, e:
			print "Client lost: " + CLIENTNAME + " exception: " + str(e)	
		return "/ERROR"


	#Behandlar övergripande kommunikationen med och mellan klienterna. Sköter även kommandon.
	def handler(self,zero):
		try:
			atomic_sendAll("Server message: " + str(self.name) + " connected.")
			self.sendBack("Inloggad på " + str(ADDR))

			while 1:
				data = self.socket.recv(BUFF)
				if(data.startswith('/quit')):
					break
				elif(data.startswith('/status')): 
					self.sendBack("You are number " + str(search(self.name)))
				elif(data.startswith('/list')):
					self.sendBack(statusList())
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
					i =  time()-float(msg[1])
					self.sendBack("Ping: " + str(i))
				else:
					atomic_sendAll(self.name + ": " + data)
		except Exception, e:
			print "client lost (handler): " + str(e)

	# körs när man anropar start()
	def run(self):
		self.name = ""
		while(self.name == ""):
			self.name = self.authentication()
			print "Number: " + self.name
		if(self.name != "/ERROR"):
			self.handler(0)
		atomic_disconnect(self.name)

print "Servermeddelande: Servern är redo."



#Lyssnar efter klienter som vill ansluta.
def listenToClients():
	while 1:
		freeSlot = len(socketArray)

		print statusList()

		#for i in range(len(socketArray)):
		#	print socketArray[i].name + ": " + str(socketArray[i].index)

		socket, ADDR = copy(serverSocket.accept())
	
		#socket, addr = copy(serverSocket.accept())
		#if(freeSlot == len(socketArray)):
		socketArray.append(sessionClass(socket, ADDR))
		#else:
		#	socketArray[freeSlot] = sessionClass(freeSlot,socket)
		socketArray[freeSlot].status = 2
		socketArray[freeSlot].start()

thread.start_new_thread(listenToClients, ())

SERVERRUN = 1

while SERVERRUN:

	String = raw_input()
	if(String.startswith("x")):
		SERVERRUN = 0

serverSocket.close()
