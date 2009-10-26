#client

from socket import *
import thread
def receiver(clientSocket, ADDR):
	i = 1
	while 1:
		data = clientSocket.recv(BUFF)
		print data

message = ""
HOST = '130.236.219.209'
PORT = 2026
BUFF = 1024
ADDR = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)

thread.start_new_thread(receiver, (clientSocket, ADDR))

while 1:
	data = raw_input()
	message = data
	if (data == '/quit' or data == '/exit'):
		clientSocket.send('/quit')
		break
	clientSocket.send(data)

clientSocket.close()
