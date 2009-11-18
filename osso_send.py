import osso
import gtk

args = ("le tupel!",)

#################################
osso_c = osso.Context("sender", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.rpc_run(".receiver", "/receiver", ".receiver", "method1", args)
#################################
osso_c = osso.Context("sender", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.rpc_run(".receiver", "/receiver", ".receiver", "method2", args)


'''
#!/usr/bin/python2.5
import osso
import gtk

args = ("le tupel!",)
osso_c = osso.Context("sender", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.rpc_run("thor.receiver", "/thor/receiver", "thor.receiver", "metod", args)
print "RPC sent"
'''