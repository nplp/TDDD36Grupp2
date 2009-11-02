# server
# coding:utf-8
# Ovanstående rad är ISO-kodning för att åäö ska funka.

from socket import *
from copy import copy
from threading import *
from time import time
from groups import *

# Kodkommentarer
#
# status har tre värden: 
# 0 = utloggad 
# 1 = inaktiv
# 2 = aktiv 
	
# Anropas när klient loggar ut eller tappar kontakten.
def disconnect(index):
	sessionArray[index].status = 0
	sendAll("Server message: " + str(sessionArray[index].name) + " disconnected.")
	sessionArray[index].socket.close()

# Broadcast
def sendAll(message):	
	print "To all: " + message
	for i in range(len(sessionArray)):
		if(sessionArray[i].status > 0): # Skillnad mellan active och inactive
			sessionArray[i].socket.send(message)

# Skickar till enskild användare
def sendTo(message,index):
	print "To " + sessionArray[index].name + ": " + message
	if(sessionArray[index].status > 0):  # Skillnad mellan active och inactive
		sessionArray[index].socket.send(message)

# Söker efter användarnamn och returnerar index
def search(client):
	for i in range(len(sessionArray)):
		if(sessionArray[i].name == client):
			if(sessionArray[i].status > 0): # Skillnad mellan active och inactive
				return i
	return -1

HOST = '127.0.0.1'
PORT = 2055
BUFF = 1024
ADDR = (HOST, PORT)

print "Binding serverSocket to: ", ADDR

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(20)

sessionArray = list()
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
	status = 2
	lastWhisper = "ADMIN"
	
	def __init__(self, _index, _socket):
		self.index = _index
		self.socket = _socket
		Thread.__init__(self)

	#Sköter inloggningen.
	def authentication(self):
		CLIENTNAME = "Player1"
		try:
			while 1:
				self.socket.send("Type a name: ")
				CLIENTNAME = self.socket.recv(BUFF)
				if(search(CLIENTNAME) == -1 and CLIENTNAME in USERNAMES):
					self.socket.send("Type your password: " + CLIENTNAME)
					if(self.socket.recv(BUFF) + "\n" == USERLOGIN[CLIENTNAME]):
						self.name = CLIENTNAME
						#kollar att det inte finns någon med namnet CLIENTNAME. Funkar ej.
						if(search(CLIENTNAME) != -1):
							return CLIENTNAME
		except Exception, e:
			print "Client lost"	
		return ""


	#Behandlar övergripande kommunikationen med och mellan klienterna. Sköter även kommandon.
	def handler(self,zero):
		try:
			sendAll("Server message: " + str(self.name) + " connected.")
	
			while 1:
				data = self.socket.recv(BUFF)
				if(data.startswith('/quit')):
					disconnect(self.index)
					break
				elif(data.startswith('/status')): 
					#sendTo("You are number " + str(self.index), self.index)
					print "hej"
				elif(data.startswith('/list')):
					String = ""
					for i in range(len(sessionArray)):
						String += str(i) + ": " + str(sessionArray[i].name)
						if(sessionArray[i].status == 2):
							String += " (Active)"
						elif(sessionArray[i].status == 1):
							String += " (Inactive)"
						else:
							String += " (Disconnected)"
						String += "\n"
					sendTo(String, self.index)
				elif(data.startswith('/whisper')):
					msg = data.split(' ', 2)
					if(len(msg)>2):
						i = search(msg[1])
						if(i>-1):
							sessionArray[i].lastWhisper = self.name
							sendTo(self.name + " (w): " + msg[2], i)
							sendTo("You whispered to " + msg[1], self.index)
				elif(data.startswith('/reply')):
					msg = data.split(' ', 2)
					if(len(msg)>1):
						i = search(self.lastWhisper)
						if(i>-1):
							sessionArray[i].lastWhisper = self.name
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
		self.name = self.authentication()
		if(self.name != ""):
			self.handler(0)
		disconnect(self.index)


print "Server meddelande: Servern är redo."

#Lyssnar efter klienter som vill ansluta.
while 1:
	inactive = len(sessionArray)
	#for i in range(len(sessionArray)):
	#	if(sessionArray[i].status == 0): 
	#		inactive = i;
	#		break;
	
	print len(sessionArray)

	socket, ADDR = copy(serverSocket.accept())
	#if(inactive == len(sessionArray)):
	sessionArray.append(sessionClass(inactive,socket))
	#else:
	#	sessionArray[inactive] = sessionClass(inactive,socket)
	sessionArray[inactive].start()

	#thread.start_new_thread(handler, (0))

serverSocket.close()
