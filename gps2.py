import gpsbt
import time
 
def main():
context = gpsbt.start()
 
if context == None:
	print 'Problem while connecting!'
	return
 
# ensure that GPS device is ready to connect and to receive commands
time.sleep(2)
gpsdevice = gpsbt.gps()

# read 3 times and show information
for a in range(4):
	gpsdevice.get_fix()
        time.sleep(2)
 
        # print information stored under 'fix' variable
        print 'Altitude: %.3f'%gpsdevice.fix.altitude
        # dump all information available
        print gpsdevice
 
    # ends Bluetooth connection
gpsbt.stop(context)
 
main()

