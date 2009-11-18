# -*- coding: utf-8 -*-
import time
import gpsbt
import thread

class GPS:
	
	coord = (0,0)
	update = False

	# Uppdaterar din kordinat
	def updatecoord(self):
		print "uppdaterar"
		self.coord = gps.get_position()
	 
	# Väntar på att gpsen ska hitta en kordinat
	def waiting_for_a_fix(self):
		i = 0
		print "Vi vantar pa en koordinat"
		while (self.coord == (0,0)):
			self.coord = gps.get_position()
			print "Waiting: "+ str(i)
			i+=1
			time.sleep(2)

	def send_coordinates(self):
		self.update = True
		while (self.update == True):
			print self.coord[0]
			print self.coord[1]
			time.sleep(5)
			try:
				updatecoord()
			except:
				gpsbt.stop(__con)
		

	# Startar GPSEN
	con = gpsbt.start()
	time.sleep(2.0) # wait for gps to come up
	 
	#Getting GPS coordinats
	gps = gpsbt.gps()
	 
	#Vantar pa en gps koordinat
	print "Waiting baby"
	self.waiting_for_a_fix()

	self.send_coordinates()

