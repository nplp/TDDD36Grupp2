import osso
import gtk
 
def callback_func(interface, method, arguments, user_data):
	print method
	if(method == "method1"):
    		method1(arguments[0])
	elif(method == "method2"):
		method2(arguments[0])
	
########################
osso_c = osso.Context("receiver", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.set_rpc_callback(".receiver","/receiver",".receiver",callback_func)
########################

def method1(arg):
	print "har printas det saker fran metod 1"
	print arg
	
def method2(arg):
	print "har printas det saker fran metod 2"
	print arg

gtk.main()


'''
#!/usr/bin/python2.5
import osso
import gtk
 
def metoden(interface, method, arguments, user_data):
    print "RPC received"
    print arguments[0]


osso_c = osso.Context("receiver", "0.0.1", False)
print "osso_test_receiver started"

osso_rpc = osso.Rpc(osso_c)

osso_rpc.set_rpc_callback("thor.receiver","/thor/receiver","thor.receiver",metoden)

gtk.main()
'''


