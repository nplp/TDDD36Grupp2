#!/usr/bin/python2.5
import osso
import gtk
 
def callback_func(interface, method, arguments, user_data):
    print "RPC received"
    test()
    osso_c = user_data
    osso_c.system_note_infoprint("osso_test_receiver: Received a RPC to %s." % method)
 
osso_c = osso.Context("osso_test_receiver2", "0.0.1", False)
print "osso_test_receiver started"
rpc = osso.Rpc(osso_c)
rpc.set_rpc_callback("spam.eggs.osso_test_receiver2",
                            "/spam/eggs/osso_test_receiver2",
                            "spam.eggs.osso_test_receiver2", callback_func,
                            osso_c)
def test():
    print "har var det massa text2"
gtk.main()
