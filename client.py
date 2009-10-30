#client
# coding:utf-8
# Ovanst￥ende rad ￤r ISO-kodning f￶r att ￥￤￶ ska funka.

import re
import sys
from socket import *
import thread
import os
from message import *
from time import time

#checkar servern
def checkServer():
    serverSocket = socket.socket()
    serverSocket.settimeout(0.25)
    try:
        serverSocket.connect((HOST, PORT))
    except socket.error:
        return 1


# Tar emot meddelanden
def receiver(clientSocket, ADDR):
    while 1:
        data = unicode(clientSocket.recv(BUFF), 'utf-8')
        if(data == ""): pass
        elif(data.startswith('/ping')):
            s = data.split(' ', 1)
            print s[0] + " " + str(time() - float(s[1]))
        else:
            print data

HOST = '192.160.200.1'
HOST2 = '130.236.216.90'
PORT = 2040
BUFF = 1024
#ADDR = (HOST, PORT)
clientSocket = socket(AF_INET, SOCK_STREAM)
status = checkServer()
if (status):
    print "poop"
    ADDR = (HOST2, PORT)
else:
    print "score"
    ADDR = (HOST, PORT)
    
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
