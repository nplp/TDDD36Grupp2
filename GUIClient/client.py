# client
# coding:utf-8
# Ovanstående rad är Utf8-kodning för att åäö ska funka.

from clientCommons import *
from clientGUI import *
from clientReciever import *
from clientSender import *

import re
import sys
from socket import *

#import os
#from time import time
import subprocess

#Variabler
HOST = '130.236.216.160'
HOST2 = '130.236.189.14'
PORT = 2150
if(len(sys.argv) > 1):
	PORT = int(sys.argv[1])

MYPORT = 2000
ADDR = ('127.0.0.1', MYPORT)


#SSH anrop, startar ssh tunnel mot servern
try:
	subprocess.call('ssh -f kj@'+HOST+' -L'+str(MYPORT)+':127.0.0.1:'+str(PORT)+' sleep 4', shell=True)
except error:
	print 'no server baby'

#Sekundärserverbyte är uppskjutet, lite mer information finns i niklas_client.py där jag testar lite connection timeouts med mera.

#Aktivera clientsocket
clientSocket = socket(AF_INET, SOCK_STREAM)

if __name__ == "__main__":
	clientSocket.connect(ADDR)
	recThread = recieverClass(clientSocket, ADDR)
	recThread.start()
	senThread = senderClass(clientSocket, ADDR)
	senThread.start()
	GUIThread = GUIClass()
	GUIThread.start()
