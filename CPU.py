import dbus
import dbus.glib
import sys

# get a connection to the system bus
bus = dbus.SystemBus ()

# get a HAL object and an interface to HAL to make function calls
hal_obj = bus.get_object ('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')

# find all devices that have the capability 'laptop_panel'
udis = hal.FindDeviceByCapability ('cpu')

dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])
print dev_obj.GetCPUFreqGovernor()
