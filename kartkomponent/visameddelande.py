#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
from databasklient import *

m= getMessage(1)

class VisaMeddelande (object):
	
    def __init__(self):
	     
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
	
	#Skriv ett amne
        self.amne = gtk.Label("Avsandare: "+m.sender)
        self.amne.set_alignment(0, 0)
	self.amne.show()
	self.vbox.pack_start(self.amne, False, False, 0)
	
	#Skriv ett amne
        self.mottagare = gtk.Label("Amne: "+m.type)
        self.mottagare.set_alignment(0, 0)
	self.mottagare.show()
	self.vbox.pack_start(self.mottagare , False, False, 0)
	
	#Skriv ett meddelande
        self.meddelande = gtk.Label("Meddelande")
        self.meddelande.set_alignment(0, 0)
	self.meddelande.show()
        self.vbox.pack_start(self.meddelande, False, False, 0)
	
	self.entry1 = gtk.TextView()
	self.entry1.set_wrap_mode(gtk.WRAP_WORD_CHAR)
	self.textentry1 = self.entry1.get_buffer()
	self.textentry1.set_text(m.content)	
	self.entry1.show()
	self.scrolled_window.add_with_viewport(self.entry1)
	self.vbox.pack_start(self.scrolled_window, True, True, 0)
	
	self.svara = gtk.Button("Svara")
        self.svara.connect("clicked", self.send, "Svara")
	self.svara.show()
	self.vbox.pack_start(self.svara,True,True,0)
	
	self.avsluta = gtk.Button("Avsluta")
        self.avsluta.connect("clicked", self.send, "Avsluta")
	self.avsluta.show()
	self.vbox.pack_start(self.avsluta,True,True,0)
	
	#self.window.add(self.vbox)
	#self.window.show()
	
    def send():
	print "hej hej"
	
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    VisaMeddelande()
    main()

	
	
