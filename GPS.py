# -*- coding: utf-8 -*-
import time
import gpsbt
import thread
import gtk

class GPS(object):

	def __init__(self):
		self.coord = (0,0)
		self.update = False

	def to_string(self, tupel):
		stringen = ""
		for part in tupel:
			stringen += str(part) + " "
		return stringen


	# Uppdaterar din kordinat
	def updatecoord(self):
		self.coord = self.gps.get_position()
		return self.coord
	 
	# Väntar på att gpsen ska hitta en kordinat
	def waiting_for_a_fix(self):
		i = 0
		print "Vi vantar pa en koordinat"
		while (self.coord == (0,0)):
			self.coord = self.gps.get_position()
		

	def send_coordinates(self):
		self.update = True
		while (self.update == True):
			print self.coord[0]
			print self.coord[1]
			time.sleep(5)
			#try:
			self.updatecoord()
			#except:
			#	gpsbt.stop(self.con)


	
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


