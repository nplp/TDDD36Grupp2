import osso
import gtk
import Dbus_registration


def metoden(interface, method, arguments, user_data):
    print "RPC received"
    print arguments[0]

rpc = Dus_registration("receiver")
rpc.receive(metoden)
gtk.main()

















'''
#!/usr/bin/python2.5
import osso
import gtk
 
def metoden(interface, method, arguments, user_data):
    print "RPC received"
    print arguments[0]


osso_c = osso.Context("receiver", "0.0.1", False)
print "osso_test_receiver started"

osso_rpc = osso.Rpc(osso_c)

osso_rpc.set_rpc_callback("thor.receiver","/thor/receiver","thor.receiver",metoden)

gtk.main()
'''




