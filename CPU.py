import dbus
import dbus.glib
import sys

# get a connection to the system bus
bus = dbus.SystemBus ()

# get a HAL object and an interface to HAL to make function calls
hal_obj = bus.get_object ('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')

# find all devices that have the capability 'laptop_panel'
udis = hal.FindDeviceByCapability ('laptop_panel')



# get a device object
dev_obj = bus.get_object ('org.freedesktop.Hal', '/org/freedesktop/Hal/Device/LaptopPanel')

# get an interface to the device
dev = dbus.Interface (dev_obj, 'org.freedesktop.Hal.Device')
print dev.GetProperty ('info.product')
print "Brightness levels:", dev.GetProperty ('laptop_panel.num_levels')

# get a difference interface to the device
dev = dbus.Interface (dev_obj, 'org.freedesktop.Hal.Device.LaptopPanel')
# make some function calls
print "Current brightness:", dev.GetBrightness ()
dev.SetBrightness (int (sys.argv[1]))
print "New brightness:", dev.GetBrightness ()
