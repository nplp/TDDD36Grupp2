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
		self.has_fix = False
		self.osso_c = osso.Context("gps", "0.0.1", False)
		self.osso_rpc = osso.Rpc(self.osso_c)
		self.osso_rpc.set_rpc_callback("thor.gps","/thor/gps","thor.gps",self.updatecoord)

	def to_string(self, tupel):
		stringen = ""
		for part in tupel:
			stringen += str(part) + " "
		return stringen


	# Uppdaterar din kordinat
	def updatecoord(self, interface, method, arguments, user_data):
		print "inne i callback"
		#if(self.has_fix):
		#print "uppdaterar din koordinat"
		self.coord = self.gps.get_position()
		return self.to_string(self.coord)
		#return False


	def refresh(self):
		self.coord = self.gps.get_position()
	 
	# Väntar på att gpsen ska hitta en kordinat
	def waiting_for_a_fix(self):
		print "Vi vantar pa en koordinat"
		while (self.coord == (0,0)):
			self.coord = self.gps.get_position()
		print "fix aquizired!"
		self.has_fix = True


	def send_coordinates(self):
		self.update = True
		while (self.update == True):
			print self.coord[0]
			print self.coord[1]
			time.sleep(5)
			#self.refresh()
			self.updatecoord()

	
	def run(self):
		# Startar GPSEN
		self.con = gpsbt.start()
		time.sleep(3.0) # wait for gps to come up
		 
		# Getting GPS coordinats
		self.gps = gpsbt.gps()
		 
		# Vantar pa en gps koordinat
		print "Waiting baby"
		self.waiting_for_a_fix()
		self.send_coordinates()


def main():
    gtk.main()

if __name__ == "__main__":
    GPS().run()
    main()


