import osso
import gtk

def method1():
	print "har hander det grejer!"
	

osso_c = osso.Context("receiver", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.set_rpc_callback("thor.receiver","/thor/receiver","thor.receiver", method1, osso_c)
