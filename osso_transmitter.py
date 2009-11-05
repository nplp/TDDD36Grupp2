#!/usr/bin/python2.4
import osso
import hildon
import gtk
 
def send_rpc(widget, osso_c):
    rpc = osso.Rpc(osso_c)
    rpc.rpc_run("spam.eggs.osso_test_receiver",
                   "/spam/eggs/osso_test_receiver",
                   "spam.eggs.osso_test_receiver",
                   "smisk_smisk")
 
    print "RPC sent"

def send_rpc2(widget, osso_c):
    rpc = osso.Rpc(osso_c)
    rpc.rpc_run("spam.eggs.osso_test_receiver2",
                   "/spam/eggs/osso_test_receiver2",
                   "spam.eggs.osso_test_receiver2",
                   "do_something")
 
    print "RPC sent"
    
    
osso_c = osso.Context("osso_test_sender", "0.0.1", False)
 
window = hildon.Window()
window.connect("destroy", gtk.main_quit)

send_button = gtk.Button("Send RPC")
hbox = gtk.HBox(homogeneous=False, spacing=0)

window.add(hbox)

hbox.add(send_button)
send_button.connect("clicked",
                    send_rpc, osso_c)

send_button2 = gtk.Button("Send RPC2")
hbox.add(send_button2)
send_button2.connect("clicked",
                    send_rpc2, osso_c)
window.show_all()
gtk.main() 
