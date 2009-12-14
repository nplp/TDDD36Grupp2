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
from kartkomponent.databasklient import *
from threading import *
import gtk
import os
import osso
from message import *
from time import *
import subprocess
import gobject
#import dbus

	


class Client(object):
	
	def __init__(self):
		#Variabler
		#HOST = '130.236.216.128'
		self.HOST = '130.236.189.14'
		self.HOST2 = '130.236.189.14'
		self.PORT = 2150
		self.PORT2 = 2151
		if(len(sys.argv) > 1):
			self.PORT = int(sys.argv[1])
		#self.BUFF = 1024
		self.MYPORT = 2800
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

	def popuplogin(self):
		#Sag till anvandaren att man ska logga in
		self.osso_rpc.rpc_run("thor.guitest", "/thor/guitest", "thor.guitest", "show_popup")
		
	def send(self, interface, method, arguments, user_data):
		self.data = arguments[0]
			
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
			self.q.put(self.data)
			
	
	def sendfunction(self, data):
		self.data = data
		self.primary
		self.clientSocket
		self.clientSocket2
		print "primary = "+str(self.primary)
		if(self.primary):
			print "skickar till primary  "+self.data
			self.clientSocket.send(self.data)
		else:
			#print "skickar till backup  "+data
			self.clientSocket2.send(self.data)
	
	def deQueue(self):
		#print "online = "+str(online)
		global mutex
		#mutex.acquire()
		while self.online:
			temp = ""
			sleep(0.5)
			try:
				while not self.q.empty(): 
					print "tomat"
					temp = self.q.get()
					self.sendfunction(temp)
			except Exception, e:
				#print e
				self.q._put(temp)
				#fixa sa att det skickar nasta gang.
		#mutex.release()
	
	
	def update_online_status(self, online):
		self.osso_rpc.rpc_run("thor.guitest", "/thor/guitest", "thor.guitest", "online_status", (online,))
		
	
	def connect(self):
		print "primary i connect= "+str(self.primary)
		self.primary = True
		#print "primary i connect igen = "+str(primary)
		#SSH anrop, startar ssh tunnel mot servern
		try:
			self.MYPORT +=1
			subprocess.call('ssh -f nikpe890@'+self.HOST+' -L'+str(self.MYPORT)+':127.0.0.1:'+str(self.PORT)+' sleep 4', shell=True)
		except error:
			print 'no server baby i connect'
		#print "waddap"
		self.clientSocket.connect((self.ADDR, self.MYPORT))
		self.online = True
		#self.update_online_status(self.online)
		thread.start_new_thread(self.deQueue, ())
		#print "waddap2"
		recThread = recieverClass(self.clientSocket, (self.ADDR,self.PORT), self.primary, self.online)
		#print "waddap3"
		recThread.start()
		#print "waddap4"
	
	def reconnect(self):
		self.primary = False
		print "primary i reconnect igen = "+str(self.primary)
			#SSH anrop, startar ssh tunnel mot servern
		try:
			self.MYPORT +=1
			subprocess.call('ssh -f nikpe890@'+self.HOST2+' -L'+str(self.MYPORT)+':127.0.0.1:'+str(self.PORT2)+' sleep 4', shell=True)
		except error:
			print 'no server baby i reconnect'
		#print "baddap"
		self.clientSocket2.connect((self.ADDR2, self.MYPORT))
		self.online = True
		#self.update_online_status()
		thread.start_new_thread(self.deQueue, ())
		#print "baddap2"
		recThread2 = recieverClass(self.clientSocket2, (self.ADDR2,self.PORT2), self.primary, self.online)
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
			
			
	def run(self):
		#mutex = Lock()
		#q = PriorityQueue(Queue())
		#q = Queue()
		thread.start_new_thread(self.message_sync, ())
		self.connect()
	
	#metod som kors i en trad och hemtar nya objekt fran servern var 10:de sekund
	def message_sync(self):
		#global logged_in
		#print "detta ar vad logged_in ar i message_sync"+logged_in
		while(1):
			sleep(10)
			try:
				if(self.online):
					idstr = ""
					for item in getAllMessageID():
						idstr += " " + str(item)
					#for item in getAllPoiID():
					#	idstr += " " + str(item)
					args = '/sync' + idstr
					print idstr
					self.sendfunction(args)
					
			except: print "klienten er inte startad ennu sa man vet ej om den er online"
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
	
def addMsgs(p):
	if(p):
		print '#' + p + '#'
		msg = json.loads(p)
		try:
			if(msg["type"] == "text"):
				print "lagger till ett textmeddelande i klientdatabasen"+str(msg)
				addMessage(msg["sender"], msg["receiver"], msg["type"], msg["subtype"], msg["time_created"], msg["subject"], msg["message"], msg["response_to"])
			elif(msg["type"] == "poi"):
				print "lagger till en poi i klientdatabasen"+str(msg)
				addPoi(msg["coordx"], msg["coordy"], msg["name"], msg["time_created"], msg["type"], msg["subtype"])
		except KeyError, e: print "Not a msg"

	
class recieverClass(Thread):
	def __init__(self, _clientSocket, _ADDR, _primary, _online):
		self.online = _online
		self.primary = _primary
		self.clientSocket = _clientSocket
		self.ADDR = _ADDR
		self.BUFF = 1024
		Thread.__init__(self)
	
# Tar emot meddelanden
	def reciever(self):
		rest = ""
		try:
			while 1:
				data = str(self.clientSocket.recv(self.BUFF))
				if(data != "" and data != "/x"):
					print data
					if(data.startswith('/ping')):
						s = data.split(' ', 1)
						print "Ping: " + str(time() - float(s[1]))
					elif(data.startswith('Inloggad')):
						self.online = True
						klienten.update_online_status(self.online)
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
							#dict = json.loads(data)
							packets = data.split('\n')
							while('' in packets):
								packets.remove('')
							print packets
							if(len(packets) > 1):
								for p in packets[0:-2]: addMsgs(p)

							if(len(packets) > 0 and len(packets[-1]) > 0):
								if(packets[-1][-1] == '}'): addMsgs(packets[-1])
								elif(packets[-1][0] == '{'): rest = packets[-1]
							#if(dict["type"] == "text"):
							#	print "lagger till ett textmeddelande i klientdatabasen"+str(dict)
							#	addMessage(dict["sender"], dict["receiver"], dict["type"], dict["subtype"], dict["time_created"], dict["subject"], dict["message"], dict["response_to"])
							#elif(dict["type"] == "poi"):
							#	print "lagger till en poi i klientdatabasen"+str(dict)
							#	addPoi(dict["coordx"], dict["coordy"], dict["name"], dict["time_created"], dict["type"], dict["subtype"])
						elif(len(rest) > 0):
							data = rest + data
							rest = ""

						else: print data

				else:
					print "rerouting"
					self.online = False
					klienten.update_online_status(self.online)
					if(self.primary):
						klienten.reconnect()
						klienten.popuplogin()
						break
					else:
						klienten.connect()
						klienten.popuplogin()
						break
		except Exception, e:
			print e

	def run(self):
		self.reciever()


if __name__ == "__main__":
    gobject.threads_init()
    klienten = Client()
    klienten.run()
    gtk.main()


