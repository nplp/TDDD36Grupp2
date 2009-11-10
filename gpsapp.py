import time, gpsbt

# metod som hamtar en koordinat eller?
def has_a_fix(gps):
    gps.get_fix()
    return gps.satellites_used > 0

# metod som ligger och vantar på en koordinat
def waiting_for_a_fix()
	print "Vi vantar pa en koordinat"
	while not has_a_fix(gps):
    		print "Wai-ting..."
    		time.sleep(5)
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