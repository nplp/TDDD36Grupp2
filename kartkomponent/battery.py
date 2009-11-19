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
 
	#self.x = float(self.dev_obj.GetProperty('battery.reporting.current'))
	#self.y = float(self.dev_obj.GetProperty('battery.reporting.design'))
 
	self.batterylevel = (0,0)
	#x2 = float(dev_obj.GetProperty('battery.voltage.current'))
	#y2 = float(dev_obj.GetProperty('battery.voltage.design'))
	#print 'usage level', int((x2/y2)*100),'%'
 
 
    def getbattery(self):
	self.batterylevel = int((self.x/self.y)*100),'%'
	return self.batterylevel
 
 
    def listenBattery(self):
	while(1):
		self.batterylevel[0] = float(self.dev_obj.GetProperty('battery.reporting.current'))
		self.batterylevel[1] = float(self.dev_obj.GetProperty('battery.reporting.design'))
		time.sleep(60)
 
    def run(self):
	thread.start_new_thread(self.listenBattery,())
 
def main():
    gtk.main()
 
if __name__ == "__main__":
    Batteri().run()
    main()