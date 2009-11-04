#server

from socket import *
from copy import copy
import thread
import subprocess

class socketClass:
	active = 0

def handler(index,zero):
	try:
		send("Server message: " + str(socketArray[index].ADDR) + " connected.")
	
		while 1:
			data = socketArray[index].socket.recv(BUFF)
			if(data == '/quit'): break
			send (str(socketArray[index].ADDR) + " : " + data)
	except Exception, e:
		print "client disconnected"
	disconnect(index)

	
def disconnect(index):
	socketArray[index].active = 0
	send("Server message: " + str(socketArray[index].ADDR) + " disconnected.")
	socketArray[index].socket.close()

def send(message):	
	print message
	for i in range(len(socketArray)):
		if socketArray[i].active:
			socketArray[i].socket.send(message)
HOST = '127.0.0.1'
PORT = 2004
BUFF = 1024
ADDR = (HOST, PORT)

print "Binding serverSocket to: ", ADDR

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(5)

socketArray = list()

print "Server meddelande: Servern aer redo."

while 1:
	socketArray.append(socketClass())
	socketArray[len(socketArray) - 1].socket, socketArray[len(socketArray) - 1].ADDR = copy(serverSocket.accept())
	socketArray[len(socketArray) - 1].active = 1;
	
	thread.start_new_thread(handler, ((len(socketArray) - 1),0))

serverSocket.close()