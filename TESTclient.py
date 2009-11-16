#client

from socket import *
import thread
import subprocess
def receiver(clientSocket, ADDR):
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
            print e
            #print "Connection lost"
def run(self):
	self.reciever()

subprocess.call('ssh -f nikpe890@130.236.189.14 -L 2007:127.0.0.1:2161 sleep 4', shell=True)
message = ""
HOST = '127.0.0.1'
PORT = 2007
BUFF = 1024
ADDR = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)

thread.start_new_thread(receiver, (clientSocket, ADDR))

while 1:
	data = raw_input()
	message = data
	if (data == '/quit'):
		clientSocket.send('/quit')
		break
	clientSocket.send(data)
	print "skickat:"+message

clientSocket.close()
