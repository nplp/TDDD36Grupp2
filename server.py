#server

from socket import *
from copy import copy
import thread

class socketClass:
	active = 0


class userClass:
	name = "Player1"
	password = "123"
	def __init__(self,_name):
		self.name = _name

	def checkPass(self,_password):
		if password == _password:
			return true
		return false

def handler(index,zero):
	try:
		sendAll("Server message: " + str(userArray[index].name) + " connected.")
	
		while 1:
			data = socketArray[index].socket.recv(BUFF)
			if(data == '/quit'): break
			sendAll(str(userArray[index].name) + ": " + data)
	except Exception, e:
		print "client disconnected"
	disconnect(index)

	
def disconnect(index):
	socketArray[index].active = 0
	sendAll("Server message: " + str(userArray[index].name) + " disconnected.")
	socketArray[index].socket.close()

def sendAll(message):	
	print message
	for i in range(len(socketArray)):
		if socketArray[i].active:
			socketArray[i].socket.send(message)
HOST = '130.236.219.209'
PORT = 2026
BUFF = 1024
ADDR = (HOST, PORT)

CLIENTNAME = "Player1"

print "Binding serverSocket to: ", ADDR

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(5)

socketArray = list()
userArray = list()

print "Server meddelande: Servern aer redo."

while 1:
	socketArray.append(socketClass())
	socketArray[len(socketArray) - 1].socket, socketArray[len(socketArray) - 1].ADDR = copy(serverSocket.accept())
	
	socketArray[len(socketArray) - 1].socket.send("Type a name: ")
	CLIENTNAME = socketArray[len(socketArray) - 1].socket.recv(BUFF)

	userArray.append(userClass(CLIENTNAME))
	socketArray[len(socketArray) - 1].active = 1;

	thread.start_new_thread(handler, ((len(socketArray) - 1),0))

serverSocket.close()
