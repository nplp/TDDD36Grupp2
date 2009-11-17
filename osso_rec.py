#!/usr/bin/python2.5
import osso
import gtk
 
def callback_func(user_data):
    print "RPC received"
    osso_c = user_data


osso_c = osso.Context("receiver", "0.0.1", False)
print "osso_test_receiver started"

osso_rpc = osso.Rpc(osso_c)

osso_rpc.set_rpc_callback("thor.receiver","/thor/receiver","thor.receiver",callback_func, osso_c)

gtk.main()




































'''
import osso
import gtk

def callback_func():
	print "har hander det grejer!"
	

osso_c = osso.Context("receiver", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.set_rpc_callback("thor.receiver","/thor/receiver","thor.receiver", callback_func, osso_c)

gtk.main()
'''