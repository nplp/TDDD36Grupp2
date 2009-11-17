import osso

osso_c = osso.Context("sender", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.rpc_run("thor.receiver","thor/receiver","thor.receiver", "method1",(), wait_reply=True,system_bus = False)
