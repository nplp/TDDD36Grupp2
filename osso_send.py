import osso
import gtk

args = ("le tupel!",)

#################################
osso_c = osso.Context("sender", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.rpc_run("thor.receiver", "/thor/receiver", "thor.receiver", "metod1", args)
#################################
osso_c = osso.Context("sender", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.rpc_run("thor.receiver", "/thor/receiver", "thor.receiver", "metod2", args)