import osso
#import osso_rec

osso_rpc = None
name = None

def register_name(newname):
	global osso_rpc, name
	osso_c = osso.Context(newname, "0.0.1", False)
	osso_rpc = osso.Rpc(osso_c)
	
	name = newname
	return osso_rpc
	
def send_rpc(receiver, method, message):
	osso_rpc.rpc_run("thor."+receiver, "/thor/"+receiver, "thor."+receiver, method, (message,))
	
	
#def receive():

