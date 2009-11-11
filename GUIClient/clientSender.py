# client
# coding:utf-8
# Ovanstående rad är Utf8-kodning för att åäö ska funka.

from clientCommons import *

class senderClass(Thread):
	def __init__(self, _clientSocket, _ADDR):
		self.clientSocket = _clientSocket
		self.ADDR = _ADDR
		Thread.__init__(self)

	# Tar emot meddelanden
	def sender(self):
		try:
			while 1:
				data = raw_input()
		
				if(data.startswith('/quit') or data.startswith('/exit')):
				 	try:
						self.clientSocket.send('/quit')
					except Exception, e:
						print "Server has gone down."
					self.clientSocket.close()
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
					self.clientSocket.send(data)
		except Exception, e:
			print e

	def run(self):
		self.sender()
		self.clientSocket.close()

