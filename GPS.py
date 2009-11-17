# -*- coding: utf-8 -*-
import time
import gpsbt
import thread


class GPS:
	
	# Tupel där dina kordinater sparas
	__coord = (0,0)
	__update == False
	__con

	# Uppdaterar din kordinat
	def updatecoord():
		print "uppdaterar"
		__coord = gps.get_position()
	 
	# Väntar på att gpsen ska hitta en kordinat
	def waiting_for_a_fix():
		i = 0
		print "Vi vantar pa en koordinat"
		global coord
		while (coord == (0,0)):
			coord = gps.get_position()
			print "Waiting: "+ str(i)
			i+=1
			time.sleep(2)

	def send_coordinates():
		__update == True
		while (__update == True):
			print __coord[0]
			print __coord[1]			
			time.sleep(5)
			try:			
				updatecoord()
			except:
				gpsbt.stop(con)
		

	# Startar GPSEN
	con = gpsbt.start()
	time.sleep(2.0) # wait for gps to come up
	 
	#Getting GPS coordinats
	gps = gpsbt.gps()
	 
	#Vantar pa en gps koordinat
	print "Waiting baby"
	waiting_for_a_fix()

	send_coordinates()

