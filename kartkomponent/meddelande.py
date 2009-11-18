#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
class Meddelande (object):
	
    def send(self, widget, event, data=None):
    	print ("hej")	
	
    def __init__(self):
	    
	#Vbox for innehall
	self.vbox = gtk.VBox(False,5)
	self.vbox.set_border_width(50)	
	
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

	
	#Skriv ett meddelande
        self.meddelande = gtk.Label("Meddelande")
        self.meddelande.set_alignment(0, 0)
	self.meddelande.show()
        self.vbox.pack_start(self.meddelande, False, False, 0)
	
	self.entry1 = gtk.TextView()
	#self.entry1.set_size_request(50,200)
	#self.entry1.modify_font(pango.FontDescription("Sans 12"))	
	self.entry1.show()
	self.scrolled_window.add_with_viewport(self.entry1)
	self.vbox.pack_start(self.scrolled_window, True, True, 0)
	
	self.skicka = gtk.Button("Skicka")
        self.skicka.connect("clicked", self.send, "Skicka")
	self.skicka.show()
	self.vbox.pack_start(self.skicka,True,True,0)
	
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    Meddelande()
    main()

	

