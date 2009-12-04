# client
# coding:utf-8
# Ovanstï¿¯ï¾¿ï¾¥ende rad ï¿¯ï¾¿ï¾¤r ISO-kodning fï¿¯ï¾¿ï¾¶r att ï¿¯ï¾¿ï¾¥ï¿¯ï¾¿ï¾¤ï¿¯ï¾¿ï¾¶ ska funka.

import re
import sys
from socket import *
from threading import *
import os
from message import *
from time import time
import subprocess
import simplejson as json

from read_db import *
#import dbus

#Variabler
#HOST = '130.236.216.128'
HOST = '130.236.189.14'
HOST2 = '130.236.189.14'
PORT = 2154
PORT2 = 2150
if(len(sys.argv) > 1):
	PORT = int(sys.argv[1])
BUFF = 1024
MYPORT = 2012
ADDR = ('127.0.0.1')
ADDR2 = ('127.0.0.1')
contactList = list()
recMsgs = list()

LOGGED_IN = False



#Sekundärserver byte är uppskjutet, lite mer information finns i niklas_client.py där jag testar lite connection timeouts med mera.

#Aktivera clientsocket
clientSocket = socket(AF_INET, SOCK_STREAM)

'''
#Checkar servern
def checkServer():
    serverSocket = socket()
    serverSocket.settimeout(1)
    try:
        serverSocket.connect(ADDR)
        serverSocket.shutdown(2)
        serverSocket.close()
        return 0
    except error:
        return 1

''' 



class recieverClass(Thread):
	def __init__(self, _clientSocket, _ADDR,):
		self.clientSocket = _clientSocket
		self.ADDR = _ADDR
		Thread.__init__(self)
    
    # Tar emot meddelanden
	def reciever(self):
		try:
			while 1:
				data = str(self.clientSocket.recv(BUFF))
				if(data != "" and data != "/x"):
					if(data.startswith('/ping')):
						s = data.split(' ', 1)
						print "Ping: " + str(time() - float(s[1]))
					elif(data.startswith('/online')):
						s = data.split(' ', 1)
						if(data[7] == '/'):
							print s[1] + " is not online."
							if(s[1] in contactList):
								contactList.remove(s[1])
						else:
							print s[1] + " is online."
							contactList.append(s[1])
					else:
						if(data.startswith('{')):
							# Delar upp meddelanden i {}-strängar. Man får inte använda }.
							packets = data.split('}')
							while('' in packets):
								packets.remove('')
							for p in packets:
								p = p + '}'
								print p
								msg = json.loads(p)
								try:
									recMsgs.append(msg["id"])
									print recMsgs	
								except KeyError, e: print "Not a msg"
						else: print data
				else:
					break
		except Exception, e:
			print e
	def run(self):
		self.reciever()

clientSocket.connect((ADDR, PORT))
recThread = recieverClass(clientSocket, (ADDR,PORT))
recThread.start()

idnr = 56

# Skickar meddelanden samt har hand om kommandon
while 1:
	idnr = idnr + 1
	data = raw_input()
	msg = sysMessage(data)
	data = finishCMD(msg)
        
	if(data.startswith('/quit') or data.startswith('/exit')):
	 	try:
			clientSocket.send('/quit')
		except Exception, e:
			print "Server has gone down."
		break
	elif(data.startswith('/lo')):
		LOGGED_IN = True

	if(data.startswith('/ping')):
		temp = data.split(' ',1)
		if(len(temp) == 1):
			data = '/ping' + '/ ' + str(time())
	elif(data.startswith('/addcontact')):
		temp = data.split(' ',1)
		data = ""
		if(len(temp) > 1 and temp[1] not in contactList):
			contactList.append(temp[1])
	elif(data.startswith('/deletecontact')):
		temp = data.split(' ',1)
		data = ""
		if(len(temp) > 1 and temp[1] in contactList):
			contactList.remove(temp[1])
	elif(data.startswith('/showcontactlist')):
		data = ""
		print "Online contacts: "
		for n in contactList:
			print n

	elif(data.startswith('/sync')):
		if(data.startswith('/sync all')):
			data = '/sync'
		else:
			data = '/sync'
			for r in recMsgs:
				data = data + ' ' + str(r)
	elif(not data.startswith('/') and LOGGED_IN == True):

		msg = data.split(' ',1)
		if(len(msg) > 1):
			m = Message()
			m.id = idnr
			m.sender = "kj"
			m.receiver = msg[0]
			m.message = msg[1]
			d = class2dict(m)
			print d
			data = json.dumps(d)

	if(data != ""):
		clientSocket.send(data)

clientSocket.close()
