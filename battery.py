import dbus

bus = dbus.SystemBus()
hal_obj = bus.get_object ('org.freedesktop.Hal', 
                          '/org/freedesktop/Hal/Manager')
hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')
uids = hal.FindDeviceByCapability('battery')
dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])

#print 'charge design', dev_obj.GetProperty('battery.reporting.design')
#print 'charge current', dev_obj.GetProperty('battery.reporting.current')
float(x) = dev_obj.GetProperty('battery.reporting.current')
float(y) = dev_obj.GetProperty('battery.reporting.design')

print 'battery level: ', x/y
#print 'charge unit', dev_obj.GetProperty('battery.reporting.unit')

#print 'voltage current', dev_obj.GetProperty('battery.voltage.current')
#print 'voltage design', dev_obj.GetProperty('battery.voltage.design')
#print 'voltage unit', dev_obj.GetProperty('battery.voltage.unit')
