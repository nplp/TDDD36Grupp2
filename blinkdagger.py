#!/usr/bin/python2.5

import osso
import gobject

# Example of using osso.DeviceState.display_state_on
# You need to set the display brightness period to 10 seconds. 
# This example will bright the display after each 11 seconds.

count = 0

def blink_cb(device, loop):
    print "hej"
    global count

    device.display_state_on()

    count += 1 
    if count == 5:
        loop.quit()
        return False

    return True

def main():
    global count
    loop = gobject.MainLoop()
    osso_c = osso.Context("osso_test_device_on", "0.0.1", False)
    device = osso.DeviceState(osso_c)
    
    gobject.timeout_add(11000, blink_cb, device, loop)

    loop.run()

if __name__ == "__main__":
    main()
