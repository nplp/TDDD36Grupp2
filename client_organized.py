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
		self.HOST = '127.0.0.1'
		self.HOST2 = '130.236.189.14'
		self.PORT = 2150
		self.PORT2 = 2017
		if(len(sys.argv) > 1):
			self.PORT = int(sys.argv[1])
		self.BUFF = 1024
		self.MYPORT = 2338
		self.ADDR = ('127.0.0.1')
		self.ADDR2 = ('127.0.0.1')
		self.contactList = list()
		self.primary = False
		self.online = False		
		self.osso_c = osso.Context("client", "0.0.1", False)
		self.osso_rpc = osso.Rpc(self.osso_c)
		self.osso_rpc.set_rpc_callback("thor.client","/thor/client","thor.client",self.send)
		
		#Aktivera clientsocket
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket2 = socket(AF_INET, SOCK_STREAM)
		clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		clientSocket2.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

	def send(self, interface, method, arguments, user_data):
		
		self.dict = json.loads(arguments[0])
		self.data = dict["content"]["message"]
		self.msg = Message(data)
		self.data = finishCMD(msg)
		
		if(data.startswith('/quit') or data.startswith('/exit')):
			try:
				clientSocket.send('/quit')
			except Exception, e:
				print "Server has gone down."
				clientSocket.close()
				clientSocket2.close()
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
		elif(data != ""):
			#clientSocket.send(data)
			q.put(data)
			#global primary
			#print primary
			#if(primary):
				#clientSocket.send(data)
			#else:
				#clientSocket2.send(data)
	
	def sendfunction(data):
		global primary
		global clientSocket
		global clientSocket2
		#print "primary = "+str(primary)
		if(primary):
			#print "skickar till primary  "+data
			clientSocket.send(data)
		else:
			#print "skickar till backup  "+data
			clientSocket2.send(data)
	def deQueue():
		print "kommer jag till dequeue?"
		#print "online = "+str(online)
		global mutex
		global q
		#mutex.acquire()
		while online:
			temp = ""
			sleep(1)
			try:
				while not q.empty(): 
					#print "tomat"
					temp = q.get()
					print "sparar undan  "+temp
					sendfunction(temp)
			except Exception, e:
				#print e
				#print "gurka"
				q._put(temp)
				#fixa sa att det skickar nasta gang.
		#mutex.release()
	
	def connect():
		global MYPORT
		global primary
		global online
		#clientSocket = socket(AF_INET, SOCK_STREAM)
		print "wassap"
		print "gor jag detta?"
		#print "primary i connect= "+str(primary)
		#print "har borde jag satta primary till true"
		primary = True
		#print "primary i connect igen = "+str(primary)
		#SSH anrop, startar ssh tunnel mot servern
		#try:
			#MYPORT +=1
			#subprocess.call('ssh -f nikpe890@'+HOST+' -L'+str(MYPORT)+':127.0.0.1:'+str(PORT)+' sleep 4', shell=True)
		#except error:
			#print 'no server baby i connect'
		#print "waddap"
		clientSocket.connect((ADDR, PORT))
		online = True
		thread.start_new_thread(deQueue, ())
		#print "waddap2"
		recThread = recieverClass(clientSocket, (ADDR,MYPORT))
		#print "waddap3"
		recThread.start()
		#print "waddap4"
		gtk.main()
	
	def reconnect():
		global MYPORT
		global primary
		global online
		#clientSocket2 = socket(AF_INET, SOCK_STREAM)
		#print "did i do this reconnect?"
		#print "primary i reconnect = "+str(primary)
		#print "har borde jag satta primary till false"
		primary = False
		#print "primary i reconnect igen = "+str(primary)
			#SSH anrop, startar ssh tunnel mot servern
		#try:
			#MYPORT +=1
			#subprocess.call('ssh -f nikpe890@'+HOST2+' -L'+str(MYPORT)+':127.0.0.1:'+str(PORT2)+' sleep 4', shell=True)
		#except error:
			#print 'no server baby i reconnect'
		#print "baddap"
		clientSocket2.connect((ADDR2, MYPORT))
		online = True
		thread.start_new_thread(deQueue, ())
		#print "baddap2"
		recThread2 = recieverClass(clientSocket2, (ADDR2,MYPORT))
		#print "baddap3"
		recThread2.start()
		#print "baddap4"
	
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
			
			
	de run():
		#mutex = Lock()
		#q = PriorityQueue(Queue())
		q = Queue()
		connect()
	
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
		


