import osso

osso_rpc = None
name = None

class Dbus_registration():
	def __init__(self, name):
		self.name = name
		self.register_name(name)

	def register_name(self,newname):
		self.name = newname
		osso_c = osso.Context(newname, "0.0.1", False)
		self.osso_rpc = osso.Rpc(osso_c)
	
	def send_rpc(receiver, method, message):
		osso_rpc.rpc_run("thor."+receiver, "/thor/"+receiver, "thor."+receiver, method, (message,))
	
	def receive(metoden):
		self.osso_rpc.set_rpc_callback("thor."+name,"/thor/"+name,"thor."+name, metoden)
