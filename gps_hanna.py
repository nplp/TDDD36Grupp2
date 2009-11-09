import socket

class BTReader:

def connect(self):
  self.sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
  address,services=socket.bt_discover()
  print "Discovered: %s, %s"%(address,services)
  target=(address,services.values()[0])
  print "Connecting to "+str(target)
  self.sock.connect(target)

def readposition(self):
  try:
  while 1:
    buffer=""
    ch=self.sock.recv(1)
    while(ch!='$'):
      ch=self.sock.recv(1)
      while 1:
        if (ch=='\r'):
          break
        buffer+=ch
        ch=self.sock.recv(1)
        if (buffer[0:6]=="$GPGGA"):
          (GPGGA,hhmmssss,l1ddmmmmmm,l1,l2dddmmmmmm,l2,q,xx,pp,ab,M,cd,M,xx,nnnn)=buffer.split(",")
          return (l1+l1ddmmmmmm, l2+l2dddmmmmmm)
  except Error:
          return None

def close(self):
  self.sock.close()

bt=BTReader()
bt.connect()
print bt.readposition()
print bt.readposition()
print bt.readposition()
bt.close()