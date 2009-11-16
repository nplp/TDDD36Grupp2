#!/usr/bin/python2.5
import osso
import gtk
 
def callback_func(interface, method, arguments, user_data, rpc_args):
	print user_data
	print rpc_args
	print rpc_args[0]
osso_c = osso.Context("osso_test_receiver", "0.0.1", False)
rpc = osso.Rpc(osso_c)
rpc.set_rpc_callback("spam.eggs.osso_test_receiver",
                            "/spam/eggs/osso_test_receiver",
                            "spam.eggs.osso_test_receiver", callback_func,
                            osso_c)

gtk.main()


    
wget http://repository.maemo.org/stable/diablo/maemo-scratchbox-install_4.1.2.sh
