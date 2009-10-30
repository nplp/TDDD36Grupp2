#!/usr/bin/env python
# example table.py
# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui_map
import gui
import pygtk
pygtk.require('2.0')
import gtk
import gtk, gtk.glade

class MenuExample:
	
    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data
	
#   def verktyg_knapp(self, widget, data=None):
    def synas(self, widget, event, data=None):
	self.text.show()
	self.samtal.show()
	self.uppdragsmall.hide()
	self.tillbaka.show()
		
    def synas2(self, widget, event, data=None):
	    self.text.hide()
	    self.samtal.hide()
	    self.uppdragsmall.show()
	    self.karta.show()
	    self.tillbaka.show()
	    
    def tbaka(self,widget,event,data=None):
	    self.text.hide()
	    self.samtal.hide()
	    self.uppdragsmall.hide()
	    self.karta.hide()
	    self.tillbaka.hide()
	   
    def kartan(self, widget, event, data=None):
	    # Kartan
	self.tbaka("clicked", "hej")
	
	mapxml = map_xml_reader.MapXML("kartdata/map.xml")

	map = data_storage.MapData(mapxml.get_name(),
                           mapxml.get_levels())

	map.set_focus(15.5726, 58.4035)

# Ritar ut tre objekt
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
	self.startakarta.show()
	self.hbox.pack_start(self.startakarta, True, True, 0)

	
    # This callback quits the program
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False
    
    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(200, 100)
        self.window.set_title("GUI")
        self.window.connect("delete_event", lambda w,e: gtk.main_quit())
	
	#Hbox
	self.hbox = gtk.HBox(False, 0)
	
	#Vbox
        self.vbox = gtk.VBox(False, 0)
        self.vbox.show()

	#Knappar stor meny
        # Kommunikation
        self.kommunikation = gtk.Button("Kommunikation")
        self.kommunikation.connect("clicked", self.synas, "Kommunikation")
        self.kommunikation.show()
        self.vbox.pack_start(self.kommunikation, True, True, 0)

        # Verktyg
        self.verktyg = gtk.Button("Verktyg")
        self.verktyg.connect("clicked", self.synas2, "Verktyg")
        self.verktyg.show()
	self.vbox.pack_start(self.verktyg, True, True, 0)

    	# Filer
        self.filer= gtk.Button("Filer")
        self.filer.connect("clicked", self.callback, "Filer")
        self.vbox.pack_start(self.filer, True, True, 0)
	self.filer.show()

        # Avslutaknapp
        self.avsluta= gtk.Button("Avsluta")
        self.avsluta.connect("clicked", lambda w: gtk.main_quit())
	self.vbox.pack_start(self.avsluta, True, True,0)
        self.avsluta.show()
	
	self.hbox.pack_start(self.vbox, False, False, 0)
	

	#Knappar i undermenyer
	
	#Knappar Kommunikationsmeny
		#Vbox
        self.vbox2 = gtk.VBox(False, 0)
        self.vbox2.show()
	# Textmeddelande
	self.text = gtk.Button("Textmeddelande")
        self.text.connect("clicked", self.callback, "Textmeddelande")
	#text.show()
	self.vbox2.pack_start(self.text, True, True, 0)
	
	# Samtal
	self.samtal = gtk.Button("Samtal")
        self.samtal.connect("clicked", self.callback, "Samtal")
	#button.show()
	self.vbox2.pack_start(self.samtal, True, True, 0)
	
	# Tillbaka
	self.tillbaka = gtk.Button("Tillbaka")
        self.tillbaka.connect("clicked", self.tbaka, "Tillbaka")
	#button.show()
	self.vbox2.pack_start(self.tillbaka, True, True, 0)
	
	#Knappar i verktygsmeny
	
	#Uppdragsmall
	self.uppdragsmall = gtk.Button("uppdragsmall")
	self.uppdragsmall.connect("clicked", self.callback, "uppdragsmall")
	self.vbox2.pack_start(self.uppdragsmall, True, True,0)
	
	self.hbox.pack_start(self.vbox2, False, False, 0)
	#Karta
	self.karta = gtk.Button("karta")
	self.karta.connect("clicked", self.kartan, "karta")
	self.vbox2.pack_start(self.karta, True, True,0)
	
	# Tillbaka
	#self.tillbaka = gtk.Button("Tillbaka")
        #self.tilbaka.connect("clicked", self.tillbaka, "Tillbaka")
	#button.show()
	self.vbox2.pack_start(self.tillbaka, True, True, 0)
      
    	self.hbox.show()
	self.window.add(self.hbox)
        self.window.show()

def main():
    gtk.main()
    #return 0      

if __name__ == "__main__":
    MenuExample()
    main()