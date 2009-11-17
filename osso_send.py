 #!/usr/bin/python2.5
 import osso
 import hildon
 import gtk
 
 def send_rpc(widget, osso_c):
     osso_rpc = osso.Rpc(osso_c)
     osso_rpc.rpc_run("spam.eggs.osso_test_receiver",
         "/spam/eggs/osso_test_receiver",
         "spam.eggs.osso_test_receiver", "do_something")
     print "RPC sent"
 
 osso_c = osso.Context("osso_test_sender", "0.0.1", False)
 window = hildon.Window()
 window.connect("destroy", gtk.main_quit)
 send_button = gtk.Button("Send RPC")
 window.add(send_button)
 send_button.connect("clicked", send_rpc, osso_c)
 window.show_all()
 gtk.main()































































'''
#!/usr/bin/python2.5  import osso import hildon import gtk
import osso

osso_c = osso.Context("sender", "0.0.1", False)
osso_rpc = osso.Rpc(osso_c)

osso_rpc.rpc_run("thor.receiver","/thor/receiver","thor.receiver", "callback_func")
print "RPC sent.."
print ".sup with that?"
'''