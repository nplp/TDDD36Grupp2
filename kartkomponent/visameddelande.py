#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
from databasklient import *
import inkorg


class VisaMeddelande (object):
	
    def __init__(self, _args):
	
	self.args = _args
	     
	#self.window=gtk.Window()
	#self.window.set_size_request(350, 250)
	#Vbox for innehall
	self.vbox = gtk.VBox(False,5)
	self.vbox.set_border_width(50)
	self.vbox.show()	
	
	self.scrolled_window=gtk.ScrolledWindow()
	self.scrolled_window.set_border_width(10)
	self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
	self.scrolled_window.show()
	
	#self.inkorg = inkorg.Inkorg()
	
	#Skriv ett amne
        self.amne = gtk.Label("Amne: " + self.args["subject"])
        self.amne.set_alignment(0, 0)
	self.amne.show()
	self.vbox.pack_start(self.amne, False, False, 0)
	
	#Skriv ett amne
        self.mottagare = gtk.Label("Avsandare: " + self.args["sender"])
        self.mottagare.set_alignment(0, 0)
	self.mottagare.show()
	self.vbox.pack_start(self.mottagare , False, False, 0)
	
	#Skriv ett meddelande
        self.meddelande = gtk.Label("Meddelande: ")
        self.meddelande.set_alignment(0, 0)
	self.meddelande.show()
        self.vbox.pack_start(self.meddelande, False, False, 0)
	
	self.entry1 = gtk.TextView()
	self.entry1.set_wrap_mode(gtk.WRAP_WORD_CHAR)
	self.textentry1 = self.entry1.get_buffer()
	self.textentry1.set_text(self.args["content"])	
	self.entry1.show()
	self.scrolled_window.add_with_viewport(self.entry1)
	self.vbox.pack_start(self.scrolled_window, True, True, 0)
	
	self.svara = gtk.Button("Svara")
        self.svara.connect("clicked", self.send, "Svara")
	self.svara.show()
	self.vbox.pack_start(self.svara,True,True,0)
	
	self.avsluta = gtk.Button("Avsluta")
        self.avsluta.connect("clicked", self.avs, "Avsluta")
	self.avsluta.show()
	self.vbox.pack_start(self.avsluta,True,True,0)
	
	self.popup = gtk.Window()
        self.popup.set_title( "Meddelande" )
	self.popup.set_size_request(500,500)
        self.popup.add(self.vbox)
        self.popup.set_modal(False)
        self.popup.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_DIALOG )
	
    def send(self, widget, event, data=None):
	print "hej hej"
	
	
    def avs(self, widget, event, data=None):
	    self.popup.destroy()
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    VisaMeddelande()
    main()

	
	
