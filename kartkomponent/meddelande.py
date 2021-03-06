#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import simplejson as json
import gtk
import osso
#import time
import adresslista
import login
from datetime import *

class Meddelande (object):
	
    osso_c = osso.Context("meddelande", "0.0.1", False)
    osso_rpc = osso.Rpc(osso_c)
    argsy = None
		
    def send(self, widget, event, data=None):
	self.tbuffer = self.entry1.get_buffer()
	text = self.tbuffer.get_text(self.tbuffer.get_start_iter(), self.tbuffer.get_end_iter())
	amne = self.entry.get_text()
	mottagare = self.entry2.get_text()
	l = login.Inlogg()
	anvandare = login.Inlogg.get_user(l)
	datum = datetime.now()
	datum = str(datum)
	dict = {"id": 1, "sender": anvandare , "receiver": mottagare ,"type": 'text' , "subtype": "add", "time_created": datum, 'subject' : amne, 'message' : text, 'response_to' : 1}
	self.args = (json.dumps(dict),)
    
    def release(self, widget, event, data=None):
	self.osso_rpc.rpc_run("thor.client", "/thor/client", "thor.client", "method1", self.args)
	
    def __init__(self):
	#Vbox for innehall
	self.vbox = gtk.VBox(False,5)
	self.vbox.set_border_width(50)
	self.vbox.show()	
	
	self.scrolled_window=gtk.ScrolledWindow()
	self.scrolled_window.set_border_width(10)
	self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
	self.scrolled_window.show()
	
	#Skriv ett amne
        self.amne = gtk.Label("Amne")
        self.amne.set_alignment(0, 0)
	self.amne.show()
	self.vbox.pack_start(self.amne, False, False, 0)
	
	self.entry = gtk.Entry()
        self.entry.set_max_length(250)
	self.entry.show()	
	self.vbox.pack_start(self.entry, True, True, 0)
	
	#Skriv en mottagare
        self.mottagare = gtk.Label("Mottagare")
        self.mottagare.set_alignment(0, 0)
	self.mottagare.show()
	self.vbox.pack_start(self.mottagare , False, False, 0)
	
	self.entry2 = gtk.Entry()
        self.entry2.set_max_length(250)
	self.entry2.show()	
	self.vbox.pack_start(self.entry2, True, True, 0)
	
	#Lagg till mottagre
	self.skicka1 = gtk.Button("Lagg till mottagare")
        self.skicka1.connect("clicked", self.show_popup)
	self.skicka1.set_size_request(130,50)	
	self.skicka1.show()
	self.vbox.pack_start(self.skicka1,True,True,10)

	#Skriv ett meddelande
        self.meddelande = gtk.Label("Meddelande")
        self.meddelande.set_alignment(0, 0)
	self.meddelande.show()
        self.vbox.pack_start(self.meddelande, False, False, 0)
	
	self.entry1 = gtk.TextView()
	#self.entry1.set_size_request(50,200)
	#self.entry1.modify_font(pango.FontDescription("Sans 12"))
	self.entry1.set_wrap_mode(gtk.WRAP_WORD_CHAR)	
	self.entry1.show()
	self.scrolled_window.add_with_viewport(self.entry1)
	self.vbox.pack_start(self.scrolled_window, True, True, 0)
	
	self.skicka = gtk.Button("Skicka")
        self.skicka.connect("clicked", self.send, "Spara")
	self.skicka.connect("released", self.release, "Skicka")
	self.skicka.set_size_request(130,50)
	self.skicka.show()
	self.vbox.pack_start(self.skicka,True,True,10)
	
    def show_popup(self, skicka1):
	adress = adresslista.Adresslista()
        adress.popup.show()
	#adress = adresslista.Adresslista()
	#print "hej"
        #popup = gtk.Window()
        #popup.set_title( "Adresslista" )
	#popup.set_size_request(500,500)
        #popup.add(adress.vbox)
	##adress.vbox.show()	
        #popup.set_modal(False)
        ##popup.set_transient_for(self)
        #popup.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_DIALOG )
        #popup.connect( "destroy", lambda *w: gtk.main_quit() )
        #popup.show()
	
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    Meddelande()
    main()

	
	
