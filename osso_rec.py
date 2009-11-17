 #!/usr/bin/python2.5
 import osso
 import gtk
 
 def callback_func(interface, method, arguments, user_data):
     print "RPC received"
     osso_c = user_data
     osso_sysnote = osso.SystemNote(osso_c)
     osso_sysnote.system_note_infoprint("osso_test_receiver: Received an RPC to %s." % method)
 
 osso_c = osso.Context("osso_test_receiver", "0.0.1", False)
 print "osso_test_receiver started"
 osso_rpc = osso.Rpc(osso_c)
 osso_rpc.set_rpc_callback("spam.eggs.osso_test_receiver",
     "/spam/eggs/osso_test_receiver",
     "spam.eggs.osso_test_receiver", callback_func, osso_c)
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