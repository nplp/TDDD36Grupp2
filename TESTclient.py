#client

from socket import *
import thread
import subprocess
def receiver(clientSocket, ADDR):
	i = 1
	while 1:
		data = clientSocket.recv(BUFF)
		print data
subprocess.call('ssh -f nikpe890@sysi-04.sysinst.ida.liu.se -L 2133:127.0.0.1:2000 sleep 4', shell=True)
message = ""
HOST = '127.0.0.1'
PORT = 2133
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
