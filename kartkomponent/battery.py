import dbus
import thread
import time
 
class Batteri():
    
    def __init__(self):

	self.bus = dbus.SystemBus()
	self.hal_obj = self.bus.get_object ('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
	self.hal = dbus.Interface (self.hal_obj, 'org.freedesktop.Hal.Manager')
	self.uids = self.hal.FindDeviceByCapability('battery')
	self.dev_obj = self.bus.get_object ('org.freedesktop.Hal', uids[0])
 	'''
	self.x = float(self.dev_obj.GetProperty('battery.reporting.current'))
	self.y = float(self.dev_obj.GetProperty('battery.reporting.design'))
	'''
	self.batterylevel = 100
	#self.x = 50
	#self.y = 100
	#x2 = float(dev_obj.GetProperty('battery.voltage.current'))
	#y2 = float(dev_obj.GetProperty('battery.voltage.design'))
	#print 'usage level', int((x2/y2)*100),'%'
 
    def bluff(self):
    	self.x += 1
 
 
    def getbattery(self):
	x = float(self.dev_obj.GetProperty('battery.reporting.current'))
	y = float(self.dev_obj.GetProperty('battery.reporting.design'))
	self.batterylevel = int((x/y)*100)
	return self.batterylevel
 
 
    def listenBatt(self):
	while(1):
		self.bluff()
		#self.x = float(self.dev_obj.GetProperty('battery.reporting.current'))
		#self.y = float(self.dev_obj.GetProperty('battery.reporting.design'))
		time.sleep(5)
 
    def run(self):
	self.listenBatt()
 
def main():
    gtk.main()
 
if __name__ == "__main__":
    Batteri().run()
    main()