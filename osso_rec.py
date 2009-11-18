import osso
import gtk
 
def callback_func(interface, method, arguments, user_data):
    if(method = "method1"):
    	method1(arguments[0])
    elif(method = "method2"):
	method2(arguments[0])
	
########################
osso_c = osso.Context("receiver", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.set_rpc_callback("thor.receiver","/thor/receiver","thor.receiver",callback_func)
########################

gtk.main()


def method1(arg):
	print "här printas det saker fran metod 1"
	print arg
	
def method2(arg):
	print "här printas det saker fran metod 2"
	print arg


