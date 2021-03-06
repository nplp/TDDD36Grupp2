# client
# coding:utf-8
# Ovanstående rad är Utf8-kodning för att åäö ska funka.

import sys
from threading import *
import subprocess
from socket import *
'''
clientSocket = socket(AF_INET, SOCK_STREAM)
BUFF = 1024
contactList = list()
'''

#Variabler
HOST = '130.236.216.128'
HOST2 = '130.236.189.14'
PORT = 2150
if(len(sys.argv) > 1):
	PORT = int(sys.argv[1])
MYPORT = 2014
if(len(sys.argv) > 2):
	MYPORT = int(sys.argv[2])
ADDR = ('127.0.0.1', MYPORT)
BUFF = 1024
contactList = list()

#SSH anrop, startar ssh tunnel mot servern
subprocess.call('ssh -f kj@'+HOST+' -L'+str(MYPORT)+':127.0.0.1:'+str(PORT)+' sleep 4', shell=True)

#Sekundärserverbyte är uppskjutet, lite mer information finns i niklas_client.py där jag testar lite connection timeouts med mera.

#Aktivera clientsocket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)


# Tar emot meddelanden
class Reciever(Thread):
	END = False
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		try:
			while 1:
				data = str(clientSocket.recv(BUFF))
				if(data == '/x'):
					END = True
					clientSocket.close()
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
					print "rerouting"
		except Exception, e:
			print e
		END = True
		clientSocket.close()

# Skickar meddelanden
class Sender(Thread):
	END = False
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		try:
			while 1:
				data = raw_input()

				if(data.startswith('/quit') or data.startswith('/exit')):
				 	try:
						clientSocket.send('/quit')
					except Exception, e:
						print "Server has gone down."
					clientSocket.close()
					break
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
				else:
					if(data != ""):
						clientSocket.send(data)
		except Exception, e:
			print e
		clientSocket.close()
		self.END = True
