# -*- coding: utf-8 -*-
mport osso
import gtk

#args = de argument som ska skickas som tupel
args = ("le tupel!",)

################################# anropar metod 1 i processen med registrerat namn receiver
osso_c = osso.Context("sender", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.rpc_run("thor.receiver", "/thor/receiver", "thor.receiver", "method1", args)
################################# anropar metod 2 i processen med registrerat namn receiver
osso_c = osso.Context("sender", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.rpc_run("thor.receiver", "/thor/receiver", "thor.receiver", "method2", args)

