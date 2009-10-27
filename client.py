#client
# -*- coding: ISO-8859-1 -*-
# Ovanstående rad är ISO-kodning för att åäö ska funka.

from socket import *
import thread
from message import *
#import message

# Tar emot meddelanden
def receiver(clientSocket, ADDR):
	i = 1
	while 1:
		data = unicode(clientSocket.recv(BUFF), 'utf-8')
		print data

HOST = '127.0.0.1'
PORT = 2005
BUFF = 1024
ADDR = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)

thread.start_new_thread(receiver, (clientSocket, ADDR))

# Skickar meddelanden samt har hand om kommandon
while 1:
	data = raw_input()
	msg = Message(data)
	data = finishCMD(msg)
		
	if (data == '/quit' or data == '/exit'):
		clientSocket.send('/quit')
		break
	clientSocket.send(data)

clientSocket.close()
