#client
# -*- coding: ISO-8859-1 -*-
# Ovanstￃﾥende rad ￃﾤr ISO-kodning fￃﾶr att ￃﾥￃﾤￃﾶ ska funka.

import re
import sys
from socket import *
import thread
import os
from message import *
from time import time

# Tar emot meddelanden
def receiver(clientSocket, ADDR):
    while 1:
        data = unicode(clientSocket.recv(BUFF), 'utf-8')
        print data

HOST = '192.160.200.1'
HOST2 = '130.236.218.134'
#HOST2 = '192.160.200.1'
PORT = 2040
BUFF = 1024
ADDR = (HOST, PORT)

# \d matchar antales received paket
lifeline = re.compile(r"(\d) received")

#pingar given ip ger sammafattning av f�rs�k
ping = os.popen("ping -q -c2 " +HOST,"r")
sys.stdout.flush()

#Kollar igenom hela "filen" man f�r av ping.readline()
while 1:
   line = ping.readline()
   if not line: break
   igot = re.findall(lifeline,line)
   if igot:
    if(int(igot[0])==0):
        print "server down"
        ADDR = (HOST2, PORT)
    else:
        print "go ahead bitches"
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
