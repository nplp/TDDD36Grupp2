#client

from socket import *
import thread
import subprocess
def receiver(clientSocket, ADDR):
	i = 1
	while 1:
		data = clientSocket.recv(BUFF)
		print data
subprocess.call('ssh -f kj@130.236.219.218 -L 2001:127.0.0.1:2161 sleep 4', shell=True)
message = ""
HOST = '127.0.0.1'
PORT = 2001
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
