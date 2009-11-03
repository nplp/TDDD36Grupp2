# server
# coding:utf-8
# Ovanstående rad är ISO-kodning för att åäö ska funka.

from socket import *
from copy import copy
from threading import *
import thread
from time import *
from groups import *

# Kodkommentarer
#
# status har tre värden: 
# 0 = utloggad 
# 1 = inaktiv
# 2 = aktiv 

# Anropas när klient loggar ut eller tappar kontakten.
def disconnect(index):
	socketArray[index].status = 0
	sendAll("Server message: " + str(socketArray[index].name) + " disconnected.")
	socketArray[index].socket.close()

# Broadcast
def sendAll(message):
	print "To all: " + message
	for i in range(len(socketArray)):
		if(socketArray[i].status > 0 and i != 0): # Skillnad mellan active och inactive
			socketArray[i].socket.send(message)

# Skickar till enskild användare
def sendTo(message,index):
	print "To " + socketArray[index].name + ": " + message
	if(socketArray[index].status > 0):  # Skillnad mellan active och inactive
		socketArray[index].socket.send(message)

# Söker efter användarnamn och returnerar index
def search(client):
	for i in range(len(socketArray)):
		if(socketArray[i].name == client):
			if(socketArray[i].status > 0): # Skillnad mellan active och inactive
				return i
	return -1

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

HOST = '130.236.219.66'
#HOST = '127.0.0.1'
PORT = 2145
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
	
	def __init__(self, _index, _socket, _ADDR):
		self.index = _index
		self.socket = _socket
		self.ADDR = ADDR
		Thread.__init__(self)

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
					i = i+1
				# Kicka om man inte skriver något efter 20 försök.
				if(CLIENTNAME == ""):
					return "/ERROR"
				if(search(CLIENTNAME) == -1 and CLIENTNAME in USERNAMES):
					self.socket.send("Type your password " + CLIENTNAME)
					if(self.socket.recv(BUFF) + "\n" == USERLOGIN[CLIENTNAME]):
						self.name = CLIENTNAME
						# Fel: Två klienter kan logga in med samma acc om de gör det samtidigt.
						return CLIENTNAME
		except Exception, e:
			print "Client lost: " + CLIENTNAME	
		return "/ERROR"


	#Behandlar övergripande kommunikationen med och mellan klienterna. Sköter även kommandon.
	def handler(self,zero):
		try:
			sendAll("Server message: " + str(self.name) + " connected.")
	
			while 1:
				data = self.socket.recv(BUFF)
				if(data.startswith('/quit')):
					break
				elif(data.startswith('/status')): 
					sendTo("You are number " + str(self.index), self.index)
				elif(data.startswith('/list')):
					sendTo(statusList(), self.index)
				elif(data.startswith('/whisper')):
					msg = data.split(' ', 2)
					if(len(msg)>2):
						i = search(msg[1])
						if(i>-1):
							socketArray[i].lastWhisper = self.name
							sendTo(self.name + " (w): " + msg[2], i)
							sendTo("You whispered to " + msg[1], self.index)
				elif(data.startswith('/reply')):
					msg = data.split(' ', 1)
					if(len(msg)>1):
						i = search(self.lastWhisper)
						if(i>-1):
							socketArray[i].lastWhisper = self.name
							sendTo(self.name + " (w): " + msg[1], i)
							sendTo("You whispered to " + self.lastWhisper, self.index)
				elif(data.startswith('/ping')):
					msg = data.split(' ', 1)
					i =  time()-float(msg[1])
					sendTo("Ping: " + str(i), self.index)
				else:
					sendAll(self.name + ": " + data)
		except Exception, e:
			print "client lost (handler)"

	# körs när man anropar start()
	def run(self):
		self.name = ""
		while(self.name == ""):
			self.name = self.authentication()
			print "Number: " + self.name + str(self.index)
		if(self.name != "/ERROR"):
			self.handler(0)
		disconnect(self.index)

print "Servermeddelande: Servern är redo."



#Lyssnar efter klienter som vill ansluta.
def listenToClients():
	print "hej"
	while 1:
		freeSlot = len(socketArray)
		#for i in range(len(socketArray)):
		#	if(not socketArray[i].isAlive()): 
		#		freeSlot = i;
		#		break;

		print statusList()

		#for i in range(len(socketArray)):
		#	print socketArray[i].name + ": " + str(socketArray[i].index)

		socket, ADDR = copy(serverSocket.accept())
	
		#socket, addr = copy(serverSocket.accept())
		#if(freeSlot == len(socketArray)):
		socketArray.append(sessionClass(freeSlot, socket, ADDR))
		#else:
		#	socketArray[freeSlot] = sessionClass(freeSlot,socket)
		socketArray[freeSlot].status = 2
		socketArray[freeSlot].start()

thread.start_new_thread(listenToClients, ())

SERVERRUN = 1

while SERVERRUN:

	String = raw_input()
	if(String.startswith("/exit")):
		SERVERRUN = 0


serverSocket.close()
