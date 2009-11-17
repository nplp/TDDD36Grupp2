#!/usr/bin/python2.5  import osso import hildon import gtk
import osso

osso_c = osso.Context("sender", "0.0.1", False)
#osso_rpc = osso.Rpc(osso_c)

osso_c.rpc_run("thor.receiver","/thor/receiver","thor.receiver", "method1")
print "RPC sent"