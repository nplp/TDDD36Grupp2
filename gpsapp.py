import time, gpsbt


# metod som ligger och vantar pa en koordinat

coordx,coordy= (0,0)
oldcoordx,oldcoordy = (0,0)
i = 0
def waiting_for_a_fix():
	print "Vi vantar pa en koordinat"
	while ((coordx == 0 and coordy == 0) or (coordx == oldcoordx and coordy == oldcoordy)):
		coordx,coordy =gps.get_position()
    		print "Wai-ting."+i
		i+=1
    		time.sleep(2)
	oldcoordx,oldcoordy = gps.get_position()
	print gps.get_position()

# Startar GPSEN
con = gpsbt.start()
time.sleep(2.0) # wait for gps to come up
#Getting GPS coordinats
gps = gpsbt.gps()
#Vantar pa en gps koordinat
waiting_for_a_fix()
waiting_for_a_fix()
# Turning of GPS
gpsbt.stop(con)