#server
# -*- coding: ISO-8859-1 -*-
# Ovanstående rad är ISO-kodning för att åäö ska funka.

from socket import *
from copy import copy
import thread

class socketClass:
	active = 0

#Användarklassen
class userClass:
	name = "Player1"
	password = "123"
	def __init__(self,_name):
		self.name = _name

	def checkPass(self,_password):
		if password == _password:
			return true
		return false

#Behandlar övergripande kommunikationen med och mellan klienterna. Sköter även kommandon.
def handler(index,zero):
	try:
		sendAll("Server message: " + str(userArray[index].name) + " connected.")
	
		while 1:
			data = socketArray[index].socket.recv(BUFF)
			if(data == '/quit'): break
			elif(data == '/status'): sendTo("You are number " + str(index), index)
			elif(data == '/list'):
				String = ""
				for i in range(len(userArray)):
					String += str(i) + ": " + str(userArray[i].name)
					if socketArray[i].active:
						String += " (Active)"
					else:
						String += " (Inactive)"
					String += "\n"
				sendTo(String, index)
			else:
				sendAll(str(userArray[index].name) + ": " + data)
	except Exception, e:
		print "client disconnected"
	disconnect(index)

	
#Anropas när klient loggar ut eller tappar kontakten.
def disconnect(index):
	socketArray[index].active = 0
	sendAll("Server message: " + str(userArray[index].name) + " disconnected.")
	socketArray[index].socket.close()

#Broadcast
def sendAll(message):	
	print message
	for i in range(len(socketArray)):
		if socketArray[i].active:
			socketArray[i].socket.send(message)

#Skickar till enskild användare
def sendTo(message,index):
	print "To " + userArray[index].name + ": " + message
	if socketArray[index].active:	
		socketArray[index].socket.send(message)

#Söker efter användarnamn och returnerar index
def search(client):
	for i in range(len(userArray)):
		if(userArray[i].name == client):
			return i
	return -1

HOST = '127.0.0.1'
PORT = 2031
BUFF = 1024
ADDR = (HOST, PORT)

print "Binding serverSocket to: ", ADDR

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(5)

socketArray = list()
userArray = list()

print "Server meddelande: Servern är redo."

#Sköter inloggningen.
def authentication(index):
	CLIENTNAME = "Player1"
	while 1:
		socketArray[index].socket.send("Type a name: ")
		CLIENTNAME = socketArray[index].socket.recv(BUFF)
		if(search(CLIENTNAME) == -1): break
	return CLIENTNAME

#Lyssnar efter klienter som vill ansluta.
while 1:
	inactive = -1
	for i in range(len(socketArray)):
		if(socketArray[i].active == 0): 
			inactive = i;
			break;

	#Om det inte finns några platser som är inaktiva
	if(inactive == -1):
		socketArray.append(socketClass())
		socketArray[len(socketArray) - 1].socket, socketArray[len(socketArray) - 1].ADDR = copy(serverSocket.accept())

		userArray.append(userClass(authentication(len(socketArray) - 1)))
		socketArray[len(socketArray) - 1].active = 1;

		thread.start_new_thread(handler, ((len(socketArray) - 1),0))

	#inactive är den inloggade inaktiva användaren med lägst index
	else:
		socketArray[inactive].socket, socketArray[inactive].ADDR = copy(serverSocket.accept())

		userArray[inactive].name = authentication(inactive)
		socketArray[inactive].active = 1;

		thread.start_new_thread(handler, ((inactive),0))

serverSocket.close()
