import time
import gpsbt

# metod som ligger och vantar pa en koordinat

def waiting_for_a_fix():
	coord = (0,0)
	oldcoord = (0,0)
	i = 0
	print "Vi vantar pa en koordinat"
	while (coord == (0,0)):
		coord = gps.get_position()
    		print "Waiting: "+ str(i)
		i+=1
    		time.sleep(2)
	oldcoord = gps.get_position()
	print gps.get_position()

# Startar GPSEN
con = gpsbt.start()
time.sleep(2.0) # wait for gps to come up
#Getting GPS coordinats
gps = gpsbt.gps()
#Vantar pa en gps koordinat
waiting_for_a_fix()
# Turning of GPS
gpsbt.stop(con)
