import dbus

bus = dbus.SystemBus()
hal_obj = bus.get_object ('org.freedesktop.Hal', 
                          #'/org/freedesktop/Hal/Manager')
hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')
uids = hal.FindDeviceByCapability('battery')
dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])

x = float(dev_obj.GetProperty('battery.reporting.current'))
y = float(dev_obj.GetProperty('battery.reporting.design'))

batteryprint = int((x/y)*100),'%'
#x2 = float(dev_obj.GetProperty('battery.voltage.current'))
#y2 = float(dev_obj.GetProperty('battery.voltage.design'))
#print 'usage level', int((x2/y2)*100),'%'

