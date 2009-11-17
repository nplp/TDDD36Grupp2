import osso
import gtk

def callback_func():
	print "har hander det grejer!"
	

osso_c = osso.Context("receiver", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.set_rpc_callback("thor.receiver","/thor/receiver","thor.receiver", callback_func, osso_c)

gtk.main()