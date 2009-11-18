import osso
import gtk
 
#callback_func far ett anrop och anropar i sin tur ratt metod enligt method argumentet
def callback_func(interface, method, arguments, user_data):
	print method
	if(method == "method1"):
    		method1(arguments[0])
	elif(method == "method2"):
		method2(arguments[0])
	
######################## 3 obligatoriska rader för registrering, ersätt "receiver" med valfritt namn, processen kommer hoppa till metoden med namnet callback_func
osso_c = osso.Context("receiver", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)
osso_rpc.set_rpc_callback("thor.receiver","/thor/receiver","thor.receiver",callback_func)
########################

def method1(arg):
	print "har printas det saker fran metod 1"
	print arg
	
def method2(arg):
	print "har printas det saker fran metod 2"
	print arg

#mainloop krävs för att lyssna efter rpc calls
gtk.main()

