import dbus
import thread
import time

def listenBattery():
	while(1):
		x = float(dev_obj.GetProperty('battery.reporting.current'))
		y = float(dev_obj.GetProperty('battery.reporting.design'))
		time.sleep(5)

bus = dbus.SystemBus()
hal_obj = bus.get_object ('org.freedesktop.Hal', 
                          '/org/freedesktop/Hal/Manager')
hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')
uids = hal.FindDeviceByCapability('battery')
dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])

x = float(dev_obj.GetProperty('battery.reporting.current'))
y = float(dev_obj.GetProperty('battery.reporting.design'))

batteryprint = int((x/y)*100),'%'
#x2 = float(dev_obj.GetProperty('battery.voltage.current'))
#y2 = float(dev_obj.GetProperty('battery.voltage.design'))
#print 'usage level', int((x2/y2)*100),'%'
	
thread.start_new_thread(listenBattery,())