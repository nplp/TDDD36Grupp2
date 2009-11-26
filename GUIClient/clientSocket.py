# client
# coding:utf-8
# Ovanstående rad är Utf8-kodning för att åäö ska funka.

import sys
from threading import *
import thread
import subprocess
import signal
from socket import *
from message import *

'''
clientSocket = socket(AF_INET, SOCK_STREAM)
BUFF = 1024
contactList = list()
'''

########### Conectdel - Petssons del är bättre

#Variabler
HOST = '127.0.0.1'
HOST2 = '130.236.189.14'
PORT = 2150
if(len(sys.argv) > 1):
	PORT = int(sys.argv[1])
MYPORT = 2020
if(len(sys.argv) > 2):
	MYPORT = int(sys.argv[2])
ADDR = ('127.0.0.1', PORT)
BUFF = 1024
contactList = list()

#SSH anrop, startar ssh tunnel mot servern
#subprocess.call('ssh -f kj@'+HOST+' -L'+str(MYPORT)+':127.0.0.1:'+str(PORT)+' sleep 4', shell=True)

#Sekundärserverbyte är uppskjutet, lite mer information finns i niklas_client.py där jag testar lite connection timeouts med mera.

#Aktivera clientsocket

clientSocket = socket(AF_INET, SOCK_STREAM)

def connect():
	c = clientSocket.connect_ex(ADDR)
	if(c!=0):
		print "Connection problem\n" + str(c)
	else:
		print "Connected to " + str(ADDR)


########### Reciever - Jag tror den är ganska oförändrad, jämför.

# Tar emot meddelanden
class Reciever(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.END = False

	def run(self):
		try:
			while(self.END == False):
				data = str(clientSocket.recv(BUFF))
				if(data == '/x'):
					self.END = True
					break
				elif(data != ""):
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
						print data
				else:
					self.END = True
					print "Empty strings"
		except Exception, e:
			print e

########### Sender - Primitiv, kan göras bättre. Ej trådad eller processad

S_END = False

def send(data):
	global S_END
	if(S_END):
		data = finishCMD(Message(data))
		try:
			print data
			#print data
			if(data.startswith('/quit') or data.startswith('/exit')):
				clientSocket.send('/quit')
				S_END = True
				#signal.signal(self.run, 1)

			elif(data.startswith('/ping')):
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
			elif(data != ""):
				clientSocket.send(data)

		except Exception, e:
			print e
