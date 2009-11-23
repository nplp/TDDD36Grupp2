#!/usr/bin/python2.5
import osso
import hildon
import gtk

def send_rpc(widget, osso_c):
	osso_rpc = osso.Rpc(osso_c)
  	x = osso_rpc.rpc_run("spam.eggs.osso_test_receiver",
        "/spam/eggs/osso_test_receiver",
        "spam.eggs.osso_test_receiver", "do_something", (), wait_reply=True)
    print x
 
osso_c = osso.Context("osso_test_sender", "0.0.1", False)
window = hildon.Window()
window.connect("destroy", gtk.main_quit)
send_button = gtk.Button("Send RPC")
window.add(send_button)
send_button.connect("clicked", send_rpc, osso_c)
window.show_all()
gtk.main()
