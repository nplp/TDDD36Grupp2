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
#HOST = '130.236.216.128'
HOST = '130.236.189.14'
HOST2 = '130.236.189.14'
PORT = 2154
PORT2 = 2153
if(len(sys.argv) > 1):
	PORT = int(sys.argv[1])
BUFF = 1024
MYPORT = 2012
ADDR = ('127.0.0.1')
ADDR2 = ('127.0.0.1')
contactList = list()
primary = False



#Sekundärserver byte är uppskjutet, lite mer information finns i niklas_client.py där jag testar lite connection timeouts med mera.

#Aktivera clientsocket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket2 = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSocket2.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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
    global MYPORT
    global primary
    print "gor jag detta?"
    print primary
    primary = True
    print primary
    #SSH anrop, startar ssh tunnel mot servern
    try:
	MYPORT +=1
	subprocess.call('ssh -f nikpe890@'+HOST+' -L'+str(MYPORT)+':127.0.0.1:'+str(PORT)+' sleep 4', shell=True)
    except error:
	print 'no server baby i connect'
    print "waddap"
    clientSocket.connect((ADDR, MYPORT))
    print "waddap2"
    recThread = recieverClass(clientSocket, (ADDR,MYPORT))
    print "waddap3"
    recThread.start()
    print "waddap4"

def reconnect():
    global MYPORT
    global primary
    print "did i do this?"
    primary = False
        #SSH anrop, startar ssh tunnel mot servern
    clientSocket.close()
    try:
	MYPORT +=1
	subprocess.call('ssh -f nikpe890@'+HOST2+' -L'+str(MYPORT)+':127.0.0.1:'+str(PORT2)+' sleep 4', shell=True)
    except error:
	print 'no server baby i reconnect'
    print "baddap"
    clientSocket2.connect((ADDR2, MYPORT))
    print "baddap2"
    recThread2 = recieverClass(clientSocket2, (ADDR2,MYPORT))
    print "baddap3"
    recThread2.start()
    print "baddap4"
    
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
						print data
				else:
					print "rerouting"
					if(primary):
						self.clientSocket.close()
						reconnect()
					else:
						self.clientSocket.close()
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
		global primary
		print primary
		if(primary):
			clientSocket.send(data)
		else:
			clientSocket2.send(data)

clientSocket.close()
clientSocket2.close()