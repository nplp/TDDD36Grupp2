import osso

osso_rpc = None
name = None


def metoden2(self, interface, method, arguments, user_data):
	print "ere na fel eller?"
	metoden(interface, method, arguments, user_data)
	
def __init__(self, name):
	print "hejsan"
	self.name = name
	self.register_name(name)

def register_name(self,newname):
	self.name = newname
	osso_c = osso.Context(newname, "0.0.1", False)
	self.osso_rpc = osso.Rpc(osso_c)
	
def send_rpc(receiver, method, message):
	osso_rpc.rpc_run("thor.%s" % receiver, "/thor/%s" % receiver, "thor.%s" % receiver, method, (message,))
	
def receive(self,metoden):
	print "bajs"
	self.osso_rpc.set_rpc_callback("thor.receiver" ,"/thor/receiver" ,"thor.receiver", self.metoden2)
	print "pa dig"
