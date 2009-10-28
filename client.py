#client
# -*- coding: ISO-8859-1 -*-
# Ovanstående rad är ISO-kodning för att åäö ska funka.

from socket import *
import thread
from message import *
from time import time

# Tar emot meddelanden
def receiver(clientSocket, ADDR):
	while 1:
		data = unicode(clientSocket.recv(BUFF), 'utf-8')
		print data


HOST = '130.236.217.40'
PORT = 2021
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
		
	if(data.startswith('/quit') or data.startswith('/exit')):
		clientSocket.send('/quit')
		break
	if(data.startswith('/ping')):
		data = '/ping' + " " + str(time())
		
	clientSocket.send(data)

clientSocket.close()
