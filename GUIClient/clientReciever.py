# clientReciever
# coding:utf-8
# Ovanstående rad är Utf8-kodning för att åäö ska funka.

from clientCommons import *

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
				if(data == '/x'):
					self.clientSocket.close()
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
					connect()
		except Exception, e:
			print e
	def run(self):
		self.reciever()

