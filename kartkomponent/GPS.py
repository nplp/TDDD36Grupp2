# -*- coding: utf-8 -*-
import time
import gpsbt
import thread
import osso
import gtk

class GPS(object):

	def __init__(self):
		self.coord = (0,0)
		self.update = False
		self.hasfix = False
		self.osso_c = osso.Context("gps", "0.0.1", False)
		self.osso_rpc = osso.Rpc(self.osso_c)
		self.osso_rpc.set_rpc_callback("thor.gps","/thor/gps","thor.gps", self.callback_func)

	def to_string(self, tupel):
		stringen = ""
		for part in tupel:
			stringen += str(part) + " "
		return stringen


	#callback funktionen the onlyone
	def callback_func(self, interface, method, arguments, user_data):
		print "Callback: " + method
		if(method == updatecoord):
			print "update"
			return self.updatecoord()
		elif(method == hasfix):
			print "elif"
			return self.hasfix()

		
	# Uppdaterar din kordinat
	def updatecoord(self):
		self.coord = gps.get_position()
		return self.to_string(self.coord)

	# Om den har en GPS konrdinat
	def hasfix(self):
		print "inne i hasfix"
		return self.hasfix
	 
	# Väntar på att gpsen ska hitta en kordinat
	def waiting_for_a_fix(self):
		i = 0
		print "Vi vantar pa en koordinat"
		while (self.coord == (0,0)):
			time.sleep(2)
			self.coord = self.gps.get_position()
		

	def send_coordinates(self):
		self.update = True
		while (self.update == True):
			print self.coord[0]
			print self.coord[1]
			time.sleep(5)

	
	def run(self):
		# Startar GPSEN
		self.con = gpsbt.start()
		time.sleep(3.0) # wait for gps to come up
		 
		# Getting GPS coordinats
		self.gps = gpsbt.gps()
		 
		# Vantar pa en gps koordinat
		print "Waiting baby"
		self.waiting_for_a_fix()
		self.hasfix = True
		self.send_coordinates()


def main():
    gtk.main()

if __name__ == "__main__":
    GPS().run()
    main()


