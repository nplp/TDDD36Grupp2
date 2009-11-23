#!/usr/bin/python2.5
import osso
import gtk

def callback_func(interface, method, arguments, user_data):
    print "RPC received"
    osso_c = user_data
    return "hej"

osso_c = osso.Context("osso_test_receiver", "0.0.1", False)
print "osso_test_receiver started"
osso_rpc = osso.Rpc(osso_c)
osso_rpc.set_rpc_callback("spam.eggs.osso_test_receiver",
    "/spam/eggs/osso_test_receiver",
    "spam.eggs.osso_test_receiver", callback_func, osso_c)
gtk.main()
