#!/usr/bin/python2.5
import osso
import gtk

osso_c = osso.Context("sender", "0.0.1", False)


osso_rpc = osso.Rpc(osso_c)
osso_rpc.rpc_run("thor.receiver", "/thor/receiver", "thor.receiver", "do_something")
print "RPC sent"




gtk.main()































































'''
#!/usr/bin/python2.5  import osso import hildon import gtk
import osso

osso_c = osso.Context("sender", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)

osso_rpc.rpc_run("thor.receiver","/thor/receiver","thor.receiver", "callback_func")
print "RPC sent.."
print ".sup with that?"
'''