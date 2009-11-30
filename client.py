# client
# coding:utf-8
# Ovanstï¿¯ï¾¿ï¾¥ende rad ï¿¯ï¾¿ï¾¤r ISO-kodning fï¿¯ï¾¿ï¾¶r att ï¿¯ï¾¿ï¾¥ï¿¯ï¾¿ï¾¤ï¿¯ï¾¿ï¾¶ ska funka.
from heapq import heappush, heappop
from Queue import Queue
import simplejson as json
import re
import sys
from socket import *
import thread
from threading import *
import gtk
import os
import osso
from message import *
from time import *
import subprocess
#import dbus


class Client(object):
	
	def __init__(self):
		#Variabler
		#HOST = '130.236.216.128'
		self.HOST = '130.236.189.14'
		self.HOST2 = '130.236.189.14'
		self.PORT = 2051
		self.PORT2 = 2017
		if(len(sys.argv) > 1):
			self.PORT = int(sys.argv[1])
		#self.BUFF = 1024
		self.MYPORT = 2317
		self.ADDR = ('127.0.0.1')
		self.ADDR2 = ('127.0.0.1')
		self.contactList = list()
		self.primary = False
		self.online = False		
		self.osso_c = osso.Context("client", "0.0.1", False)
		self.osso_rpc = osso.Rpc(self.osso_c)
		self.osso_rpc.set_rpc_callback("thor.client","/thor/client","thor.client",self.send)
		
		#Aktivera clientsocket
		self.clientSocket = socket(AF_INET, SOCK_STREAM)
		self.clientSocket2 = socket(AF_INET, SOCK_STREAM)
		self.clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.clientSocket2.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

		self.q = Queue()

	def send(self, interface, method, arguments, user_data):
		self.dict = json.loads(arguments[0])
		self.data = self.dict["content"]["message"]
		self.msg = Message(self.data)
		self.data = finishCMD(self.msg)
		
		if(self.data.startswith('/quit') or self.data.startswith('/exit')):
			try:
				self.clientSocket.send('/quit')
			except Exception, e:
				print "Server has gone down."
				self.clientSocket.close()
				self.clientSocket2.close()
		if(self.data.startswith('/ping')):
			temp = self.data.split(' ',1)
			if(len(temp) == 1):
				self.data = '/ping' + '/ ' + str(time())
		elif(self.data.startswith('/addcontact')):
			temp = self.data.split(' ',1)
			self.data = ""
			if(len(temp) > 1 and temp[1] not in self.contactList):
				self.contactList.append(temp[1])
		elif(self.data.startswith('/deletecontact')):
			temp = self.data.split(' ',1)
			self.data = ""
			if(len(temp) > 1 and temp[1] in self.contactList):
				self.contactList.remove(temp[1])
		elif(self.data.startswith('/showcontactlist')):
			self.data = ""
			print "Online contacts: "
			for n in contactList:
				print n
		elif(self.data != ""):
			#clientSocket.send(data)
			self.q.put(self.data)
			#global primary
			#print primary
			#if(primary):
				#clientSocket.send(data)
			#else:
				#clientSocket2.send(data)
	
	def sendfunction(self, data):
		self.data = data
		self.primary
		self.clientSocket
		self.clientSocket2
		#print "primary = "+str(primary)
		if(self.primary):
			#print "skickar till primary  "+data
			self.clientSocket.send(self.data)
		else:
			#print "skickar till backup  "+data
			self.clientSocket2.send(self.data)
	
	def deQueue(self):
		#print "online = "+str(online)
		#global mutex
		#mutex.acquire()
		while self.online:
			temp = ""
			sleep(0.5)
			try:
				while not self.q.empty(): 
					#print "tomat"
					temp = self.q.get()
					print "sparar undan  "+temp
					self.sendfunction(temp)
			except Exception, e:
				#print e
				#print "gurka"
				self.q._put(temp)
				#fixa sa att det skickar nasta gang.
		#mutex.release()
	
	def connect(self):
		print "wassap"
		print "gor jag detta?"
		#print "primary i connect= "+str(primary)
		#print "har borde jag satta primary till true"
		self.primary = True
		#print "primary i connect igen = "+str(primary)
		#SSH anrop, startar ssh tunnel mot servern
		try:
			self.MYPORT +=1
			subprocess.call('ssh -f nikpe890@'+self.HOST+' -L'+str(self.MYPORT)+':127.0.0.1:'+str(self.PORT)+' sleep 4', shell=True)
		except error:
			print 'no server baby i connect'
		print "waddap"
		print self.ADDR
		print self.MYPORT
		self.clientSocket.connect((self.ADDR, self.MYPORT))
		self.online = True
		thread.start_new_thread(self.deQueue, ())
		print "waddap2"
		recThread = recieverClass(self.clientSocket, (self.ADDR,self.MYPORT))
		print "waddap3"
		recThread.start()
		print "waddap4"
		gtk.main()
	
	def reconnect():
		self.primary = False
		print "primary i reconnect igen = "+str(primary)
			#SSH anrop, startar ssh tunnel mot servern
		try:
			self.MYPORT +=1
			subprocess.call('ssh -f nikpe890@'+self.HOST2+' -L'+str(self.MYPORT)+':127.0.0.1:'+str(self.PORT2)+' sleep 4', shell=True)
		except error:
			print 'no server baby i reconnect'
		#print "baddap"
		self.clientSocket2.connect((self.ADDR2, self.MYPORT))
		self.online = True
		thread.start_new_thread(self.deQueue, ())
		#print "baddap2"
		recThread2 = recieverClass(self.clientSocket2, (self.ADDR2,self.MYPORT))
		#print "baddap3"
		recThread2.start()
		#print "baddap4"
		gtk.main()
		
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
			
			
	def run(self):
		#mutex = Lock()
		#q = PriorityQueue(Queue())
		#q = Queue()
		self.connect()
	
### Klassen for prioritets ko
#class PriorityQueue(Queue):
## Initialize the queue representation
#def __init__ (self, maxsize):
	#self.maxsize = maxsize
	#self.queue = []
## Put a new item in the queue
#def _put(self, item):
	#return heappush(self.queue, item)
## Get an item from the queue
#def _get(self):
	#return heappop(self.queue)
	
	
class recieverClass(Thread):
	def __init__(self, _clientSocket, _ADDR,):
		self.clientSocket = _clientSocket
		self.ADDR = _ADDR
		self.BUFF = 1024
		Thread.__init__(self)
	
# Tar emot meddelanden
	def reciever(self):
		try:
			while 1:
				data = str(self.clientSocket.recv(self.BUFF))
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
					online = False
					if(primary):
						reconnect()
						break
					else:
						connect()
						break
		except Exception, e:
			print e

	def run(self):
		self.reciever()


if __name__ == "__main__":
    Client().run()
  


