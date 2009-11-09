# client
# coding:utf-8
# Ovanst￯﾿ﾥende rad ￯﾿ﾤr ISO-kodning f￯﾿ﾶr att ￯﾿ﾥ￯﾿ﾤ￯﾿ﾶ ska funka.

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
HOST = '127.0.0.1'
PORT = 2150
if(len(sys.argv) > 1):
	PORT = int(sys.argv[1])
BUFF = 1024
ADDR = (HOST, PORT)


#SSH anrop, startar ssh tunnel mot servern
try:
	subprocess.call('ssh -f nikpe890@130.236.189.14 -L 2150:127.0.0.1:2000 sleep 4', shell=True)
except error:
	print 'no server baby'

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
                if(data != ""):
                    if(data.startswith('/ping')):
                        s = data.split(' ', 1)
                        print s[0] + " " + str(time() - float(s[1]))
                    else:
                        print data
                else:
                    print "rerouting"
                    connect()
        except Exception, e:
            print e
            #print "Connection lost"

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
        data = '/ping' + " " + str(time())
    clientSocket.send(data)

clientSocket.close()
