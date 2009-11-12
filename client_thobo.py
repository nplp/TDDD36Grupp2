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
#import dbus

#Variabler
HOST = '130.236.218.160'
HOST2 = '130.236.189.14'
PORT = 2150
if(len(sys.argv) > 1):
	PORT = int(sys.argv[1])
BUFF = 1024
MYPORT = 2000
ADDR = ('127.0.0.1', MYPORT)
contactList = list()


#SSH anrop, startar ssh tunnel mot servern
try:
	subprocess.call('ssh -f kj@'+HOST+' -L'+str(MYPORT)+':127.0.0.1:'+str(PORT)+' sleep 4', shell=True)
except error:
	print 'no server baby'

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
def connect():
    clientSocket.connect(ADDR)
    recThread = recieverClass(clientSocket, ADDR)
    recThread.start()

'''
    down = checkServer()
    if (down):
        print "poop"
        ADDR = (HOST, PORT)
    else:
        print "score"
        ADDR = (HOST, PORT)
'''

def checkBattery():
    try:
        bus = dbus.SystemBus()
        hal_obj = bus.get_object ('org.freedesktop.Hal', 
                              '/org/freedesktop/Hal/Manager')
        hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')
        uids = hal.FindDeviceByCapability('battery')
        dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])
        x = float(dev_obj.GetProperty('battery.reporting.current'))
        y = float(dev_obj.GetProperty('battery.reporting.design'))
        bat = int((x/y)*100)
        if(bat < 100):
            print 'Nu har du',bat,'% kvar i batteri.'
    except Exception, e :
            print "Du sitter pa en loser dator och har inget batteri"       

class recieverClass(Thread):
	def __init__(self, _clientSocket, _ADDR):
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
						print data
				else:
					print "rerouting"
					connect()
		except Exception, e:
			print e
	def run(self):
		self.reciever()

connect()

# Skickar meddelanden samt har hand om kommandon
while 1:
	data = raw_input()
	msg = Message(data)
	data = finishCMD(msg)
        
	if(data.startswith('/quit') or data.startswith('/exit')):
	 	try:
			clientSocket.send('/quit')
		except Exception, e:
			print "Server has gone down."
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

	if(data != ""):
		clientSocket.send(data)

clientSocket.close()
