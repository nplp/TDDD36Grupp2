#!/usr/bin/python2.5

import osso
import gobject

# Example of using osso.DeviceState.device_state_callback
# You need to set the display brightness period to 10 seconds. 
# This example will register a generic callback that will be called
# everytime the device changes to or from the offline mode.

calls = 0

def state_cb(shutdown, save_unsaved_data, memory_low, system_inactivity, 
    message, loop):
    global calls

    print "Shutdown: ", shutdown
    print "Save unsaved data: ", save_unsaved_data
    print "Memory low: ", memory_low
    print "System Inactivity: ", system_inactivity
    print "Message: ", message

    calls += 1

    if calls == 5:
        loop.quit()
    return False

def main():
    global count
    loop = gobject.MainLoop()
    osso_c = osso.Context("osso_test_device_on", "0.0.1", False)
    device = osso.DeviceState(osso_c)

    device.set_device_state_callback(state_cb, user_data=loop)

    loop.run()

    device.set_device_state_callback(None)

if __name__ == "__main__":
    main()
