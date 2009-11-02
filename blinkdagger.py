#!/usr/bin/python2.5

import osso
import gobject

# Example of using osso.DeviceState.display_state_on
# You need to set the display brightness period to 10 seconds. 
# This example will bright the display after each 11 seconds.

count = 0

def blink_cb(device, loop):
    
    global count

    device.display_state_on()

    count += 1 
    if count == 5:
        loop.quit()
        return False

    return True

def blink_cb2(device, loop):
    
    global count

    device.display_state_off()

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
    
    gobject.timeout_add(6000, blink_cb, device, loop)
    gobject.timeout_add(6000, blink_cb2, device, loop)


    loop.run()

if __name__ == "__main__":
    main()
