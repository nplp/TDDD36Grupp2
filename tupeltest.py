# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui
import time
import gpsbt
import thread

coord = (0,0)
hej = True

# Uppdaterar din kordinat
def updatecoord():
	global coord	
	print "uppdaterar"
	coord = gps.get_position()

# Väntar på att gpsen ska hitta en kordinat
def waiting_for_a_fix():
	i = 0
	print "Vi vantar pa en koordinat"
	global coord
	while (coord == (0,0)):
		#latitude,longitude = gps.get_position()
		coord = gps.get_position()
    		print "Waiting: "+ str(i)
		i+=1
    		time.sleep(3)
	print coord

# En loop som uppdaterar kartan med jämna mellanrum
def updatemap():
        global coord
	while(hej == True):
                
		print coord[0]
		print coord[1]
		
		print "Sov din javel"
		time.sleep(10.0)
		
		# Uppdaterar dina kordinater
		print "going to update"
		updatecoord()

# Startar GPSEN
con = gpsbt.start()
time.sleep(2.0) # wait for gps to come up

#Getting GPS coordinats
gps = gpsbt.gps()

#Vantar pa en gps koordinat
print "Waiting baby"
waiting_for_a_fix()

updatemap()
# Turning of GPS
# gpsbt.stop(con)



