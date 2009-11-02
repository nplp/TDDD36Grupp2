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
#import dbus

#checkar servern
def checkServer():
    serverSocket = socket()
    serverSocket.settimeout(1)
    try:
        serverSocket.connect((HOST, PORT))
    except error:
        return 1
    
def connect():
    status = checkServer()
    if (status):
        print "poop"
        ADDR = (HOST2, PORT)
    else:
        print "score"
        ADDR = (HOST, PORT)
    
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(ADDR)

        recThread = recieverClass(clientSocket, ADDR)
        recThread.start()

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
        if(bat < 20):
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
                data = unicode(self.clientSocket.recv(BUFF), 'utf-8')
                if(data != ""):
                    if(data.startswith('/ping')):
                        s = data.split(' ', 1)
                        print s[0] + " " + str(time() - float(s[1]))
                    else:
                        print data
        except Exception, e:
            print "Connection lost"

    def run(self):
        self.reciever()


HOST = '130.236.189.22'
HOST2 = '130.236.216.90'
PORT = 2066
BUFF = 1024

connect()

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
    try:    
        clientSocket.send(data)
    except Exception, e:
        print "Server has gone down, redirecting."
        print "The last messeage you sent had been lost and will have to resent"
        connect()
    

clientSocket.close()
