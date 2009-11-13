#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk, gobject
import gtk
import sys
sys.path.append('.kartkomponent/kartdata')
import data_storage
import map_xml_reader
import gui_map
import gui
import rapport
import pango

	
class MenuExample:
	
    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data
	
    def send(self, widget, data=None):
        print "Hello again - %s was pressed" % data
	
	
	#Tillbaka
    def tbaka(self,widget,event,data=None):
	 self.verktyg.set_active(False)
	 self.filer.set_active(False)
	 self.kommunikation.set_active(False)
	 self.vbox2.hide()

	
	#Rapport
    def rapp(self, widget, event, data=None):
	 self.kommunikation.set_active(False)
	 self.filer.set_active(False)
	 self.verktyg.set_active(False)
	 self.vbox2.hide()
	 self.label.hide()
	 self.startakarta.hide()
	 self.amne.hide()
	 self.entry.hide()
	 self.meddelande.hide()
	 self.entry1.hide()
	 self.skicka.hide()
         self.scrolled_window.show()	
	
	#Kommunikation
    def komm(self, widget, event, data=None):
	if widget.get_active():
		self.kommunikation.set_active(True)
		self.verktyg.set_active(False)
		self.filer.set_active(False)
		self.vbox2.show()
          	self.text.show()
		self.samtal.show()
		self.video.show()
		self.uppdragsmall.hide()
		self.karta.hide()
		self.uppdrag.hide()
		self.rapport.hide()
		self.lager.hide()
		self.tillbaka.show()
      	else:
          	self.tbaka(widget, data)		
		
	#Vektyg	
    def verk(self, widget, event, data=None):
	if widget.get_active():
		self.verktyg.set_active(True)
		self.kommunikation.set_active(False)
		self.filer.set_active(False)
		self.vbox2.show()
		self.text.hide()
		self.samtal.hide()
		self.video.hide()
		self.uppdragsmall.show()
		self.karta.show()
		self.uppdrag.hide()
		self.rapport.hide()
		self.lager.hide()
		self.tillbaka.show()
	else:
          	self.tbaka(widget, data)
	    
	#Filer
    def fil(self,widget,event,data=None):
	 if widget.get_active():
		self.filer.set_active(True)
		self.kommunikation.set_active(False)
		self.verktyg.set_active(False)
		self.vbox2.show()
		self.text.hide()
		self.samtal.hide()
		self.video.hide()
		self.uppdragsmall.hide()
		self.karta.hide()
		self.uppdrag.show()
		self.rapport.show()
		self.lager.show()
		self.tillbaka.show()
	 else:
          	self.tbaka(widget, data)
	
	#Visa kartan
    def kartan(self, widget, event, data=None):
	 self.verktyg.set_active(False)
	 self.vbox2.hide()
	 self.label.hide()
	 self.amne.hide()
	 self.entry.hide()
	 self.meddelande.hide()
	 self.entry1.hide()
	 self.skicka.hide()
	 self.scrolled_window.hide()
	 self.startakarta.show()
	 
    def textmedd(self, widget, event, data=None):
	 self.kommunikation.set_active(False)
	 self.filer.set_active(False)
	 self.verktyg.set_active(False)
	 self.vbox2.hide()
	 self.label.hide()
	 self.startakarta.hide()
	 self.amne.show()
	 self.entry.show()
	 self.meddelande.show()
	 self.entry1.show()
	 self.skicka.show()
	
        #Avsluta programmet
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False
    
    # Clean up allocated memory and remove the timer
    def destroy_progress(self, widget, data=None):
        self.timer = 0
        gobject.source_remove(self.timer)
        gtk.main_quit()

    def __init__(self):
        #Skapa fonster
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.window.set_size_request(200, 100)
        self.window.set_title("GUI")
        self.window.connect("delete_event", lambda w,e: gtk.main_quit())
	
	#Skapa en Vbox som sedan ska in i Hboxen och innehallar huvudknapparna i menyn
        self.vbox = gtk.VBox(False, 0)
	self.vbox.set_size_request(198, 95)
        self.vbox.show()
	
	#Skapa en stor Hbox
	self.hbox = gtk.HBox(False, 0)
  	self.hbox.show()
	self.hbox.pack_start(self.vbox, False, False, 0)

	#Knappar stor meny
        # Kommunikation
        self.kommunikation = gtk.ToggleButton("Kommunikation")
        self.kommunikation.connect("toggled", self.komm, "Kommunikation")
        self.kommunikation.show()
        self.vbox.pack_start(self.kommunikation, True, True, 0)

        # Verktyg
        self.verktyg = gtk.ToggleButton("Verktyg")
        self.verktyg.connect("toggled", self.verk, "Verktyg")
        self.verktyg.show()
	self.vbox.pack_start(self.verktyg, True, True, 0)

    	# Filer
        self.filer= gtk.ToggleButton("Filer")
        self.filer.connect("toggled", self.fil, "Filer")
	self.filer.show()
        self.vbox.pack_start(self.filer, True, True, 0)

        # Avslutaknapp
        self.avsluta= gtk.Button("Avsluta")
        self.avsluta.connect("clicked", lambda w: gtk.main_quit())
	self.avsluta.show()
	self.vbox.pack_start(self.avsluta, True, True,0)

	#Knappar i undermenyer
	#Knappar under kommunikation
	#i en vbox
        self.vbox2 = gtk.VBox(True, 0)
	self.vbox2.set_size_request(198, 95)
	
	# Textmeddelande
	self.text = gtk.Button("Textmeddelande")
        self.text.connect("clicked", self.textmedd, "Textmeddelande")
	self.vbox2.pack_start(self.text, True, True, 0)
	
	# Samtal
	self.samtal = gtk.Button("Samtal")
        self.samtal.connect("clicked", self.callback, "Samtal")
	self.vbox2.pack_start(self.samtal, True, True, 0)
	
	# Video
	self.video = gtk.Button("Video")
        self.video.connect("clicked", self.callback, "Video")
	self.vbox2.pack_start(self.video, True, True, 0)
	
	# Tillbaka
	self.tillbaka = gtk.Button("Tillbaka")
        self.tillbaka.connect("clicked", self.tbaka, "Tillbaka")
	self.vbox2.pack_start(self.tillbaka, True, True, 0)
	
	#Knappar i verktygsmeny
	#Uppdragsmall
	self.uppdragsmall = gtk.Button("   Uppdragsmall  ")
	self.uppdragsmall.connect("clicked", self.callback, "Uppdragsmall")
	self.vbox2.pack_start(self.uppdragsmall, True, True,0)
	
	#Karta
	self.karta = gtk.Button("Karta")
	self.karta.connect("clicked", self.kartan, "Karta")
	self.vbox2.pack_start(self.karta, True, True,0)
	
	# Tillbaka
	self.tillbaka = gtk.Button("Tillbaka")
        self.tillbaka.connect("clicked", self.tbaka, "Tillbaka")
	self.vbox2.pack_start(self.tillbaka, True, True, 0)
	
	#Knappar i filmenyn
	#Uppdrag
	self.uppdrag = gtk.Button("       Uppdrag      ")
	self.uppdrag.connect("clicked", self.callback, "Uppdrag")
	self.vbox2.pack_start(self.uppdrag, True, True,0)
	
	#Rapport
	self.rapport = gtk.Button("Rapport")
	self.rapport.connect("clicked", self.rapp, "Rapport")
	self.vbox2.pack_start(self.rapport, True, True,0)
	
	#Lager
	self.lager = gtk.Button("Lager")
	self.lager.connect("clicked", self.callback, "Lager")
	self.vbox2.pack_start(self.lager, True, True,0)
	
	# Tillbaka
	self.tillbaka = gtk.Button("Tillbaka")
        self.tillbaka.connect("clicked", self.tbaka, "Tillbaka")
	self.vbox2.pack_start(self.tillbaka, True, True, 0)
	self.hbox.pack_start(self.vbox2, False, False, 0)
	self.tbaka("clicked", "hej")
		
	mapxml = map_xml_reader.MapXML("kartdata/map.xml")
	map = data_storage.MapData(mapxml.get_name(),
			mapxml.get_levels())
	map.set_focus(15.5726, 58.4035)
	map.add_object("Ambulans1", data_storage.MapObject({"longitude":15.57796,
						"latitude":58.40479},
						"ikoner/ambulans.png"))
	map.add_object("Brandbil1", data_storage.MapObject({"longitude":15.5729,
						"latitude":58.40193},
						"ikoner/brandbil.png"))
	map.add_object("Sjukhus1", data_storage.MapObject({"longitude":15.5629,
						"latitude":58.4093},
						"ikoner/sjukhus.png"))
	map.add_object("Shape1", data_storage.MapObject({"longitude":15.5829,
						"latitude":58.4093},
						"arc(x - 5, y - 5, 10, 0, 2 * math.pi)",
						"set_source_rgb(0, 0, 0)"))
	self.startakarta = gui_map.Map(map)
	self.rapportera = rapport.Mall()
	self.vbox3 = gtk.VBox(False, 0)
        self.vbox3.show()
	
	
	self.scrolled_window=gtk.ScrolledWindow()
	self.scrolled_window.set_border_width(10)
	self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		
	#create a new label.
        self.label = gtk.Label("Anvandare	symbol	datum tid")
        self.label.set_alignment(0, 0)
        self.vbox3.pack_start(self.label, False, False, 0)
        self.label.show()
	
	#Skriv ett amne
        self.amne = gtk.Label("Amne")
        self.amne.set_alignment(0, 0)
	self.vbox3.pack_start(self.amne, False, False, 0)
	
	self.entry = gtk.Entry()
        self.entry.set_max_length(250)
	self.vbox3.pack_start(self.entry, True, True, 0)
	
	#Skriv ett meddelande
        self.meddelande = gtk.Label("Meddelande")
        self.meddelande.set_alignment(0, 0)
        self.vbox3.pack_start(self.meddelande, False, False, 0)
	
	self.entry1 = gtk.TextView()
        #self.entry1.set_max_length(250)
	self.entry1.set_size_request(50,200)
	#self.entry1.modify_font(pango.FontDescription("Sans 12"))	
	self.vbox3.pack_start(self.entry1, True, True, 0)
	
	self.skicka = gtk.Button("Skicka")
        self.skicka.connect("clicked", self.send, "Skicka")
	self.vbox3.pack_start(self.skicka,True,True,0)
	self.scrolled_window.add_with_viewport(self.rapportera.vbox4)
	
	#Packa karta
	self.vbox3.pack_start(self.startakarta,True,True,0)
	self.vbox3.pack_start(self.scrolled_window, True, True, 0)
	self.hbox.pack_start(self.vbox3, True, True, 0)
    	self.hbox.show()
	self.window.add(self.hbox)
	self.window.show()

def main():
    gtk.main()

if __name__ == "__main__":
    MenuExample()
    main()