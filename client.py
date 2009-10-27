#client
# -*- coding: ISO-8859-1 -*-
# Ovanstående rad är ISO-kodning för att åäö ska funka.

from socket import *
import thread

# Tar emot meddelanden
def receiver(clientSocket, ADDR):
	i = 1
	while 1:
		data = clientSocket.recv(BUFF)
		print data

message = ""
HOST = '127.0.0.1'
PORT = 2031
BUFF = 1024
ADDR = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)

thread.start_new_thread(receiver, (clientSocket, ADDR))

# Skickar meddelanden samt har hand om kommandon
while 1:
	data = raw_input()
	message = data
	if (data == '/quit' or data == '/exit'):
		clientSocket.send('/quit')
		break
	clientSocket.send(data)

clientSocket.close()
