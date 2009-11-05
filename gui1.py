#Ar det inte battre om detta sparas i en databas som man kan anvanda sig av?
#Jag kan inte se min progressbar, vad hander egentligen?
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

def progress_timeout(pbobj):
    	if pbobj.activity_check.get_active():
		pbobj.pbar.pulse()
	else:
		new_val = pbobj.pbar.get_fraction() + 0.01
	if new_val > 1.0:
	   new_val = 0.0
        # Set the new value
       	pbobj.pbar.set_fraction(new_val)
	return True
	
class MenuExample:
	
    # Callback that toggles the activity mode of the progress
    # bar	
    def toggle_activity_mode(self, widget, data=None):
        if widget.get_active():
            self.pbar.pulse()
        else:
            self.pbar.set_fraction(0.0)

    def toggle_orientation(self, widget, data=None):
        if self.pbar.get_orientation() == gtk.PROGRESS_LEFT_TO_RIGHT:
            self.pbar.set_orientation(gtk.PROGRESS_RIGHT_TO_LEFT)
        elif self.pbar.get_orientation() == gtk.PROGRESS_RIGHT_TO_LEFT:
            self.pbar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
	
    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data
	
	#Tillbaka
    def tbaka(self,widget,event,data=None):
	 self.verktyg.set_active(False)
	 self.filer.set_active(False)
	 self.kommunikation.set_active(False)
	 self.text.hide()
	 self.samtal.hide()
	 self.video.hide()
	 self.uppdragsmall.hide()
	 self.karta.hide()
	 self.uppdrag.hide()
	 self.rapport.hide()
	 self.lager.hide()	
	 self.tillbaka.hide()
	
	#Rapport
    def rapp(self,widget,event,data=None):
	 self.filer.set_active(False)
	 self.text.hide()
	 self.samtal.hide()
	 self.video.hide()
	 self.uppdragsmall.hide()
	 self.karta.hide()
	 self.uppdrag.hide()
	 self.rapport.hide()
	 self.lager.hide()	
	 self.tillbaka.hide()
	 self.startakarta.hide()
	 self.label.hide()
	 self.vbox4.show()
	
	#Kommunikation
    def komm(self, widget, event, data=None):
	if widget.get_active():
		self.verktyg.set_active(False)
		self.filer.set_active(False)
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
		self.kommunikation.set_active(False)
		self.filer.set_active(False)
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
		self.kommunikation.set_active(False)
		self.verktyg.set_active(False)
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
	 self.text.hide()
	 self.samtal.hide()
	 self.video.hide()
	 self.uppdragsmall.hide()
	 self.karta.hide()
	 self.uppdrag.hide()
	 self.rapport.hide()
	 self.lager.hide()	
	 self.tillbaka.hide()
	 self.label.hide()
	 self.startakarta.show()
	
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
        self.window.set_size_request(200, 100)
        self.window.set_title("GUI")
        self.window.connect("delete_event", lambda w,e: gtk.main_quit())
	
	
	#Skapa en Vbox som sedan ska in i Hboxen och innehallar huvudknapparna i menyn
        self.vbox = gtk.VBox(False, 0)
	self.vbox.set_size_request(198, 95)
        self.vbox.show()
	
	# Create a centering alignment object
        self.align = gtk.Alignment(0.5, 0.5, 0, 0)
        self.vbox.pack_start(self.align, False, False, 5)
        self.align.show()
	
	#Progressbar
        self.pbar = gtk.ProgressBar()
	self.align.add(self.pbar)
	self.pbar.show()
	
	self.timer = gobject.timeout_add(600, progress_timeout, self)
	
	# rows, columns, homogeneous
        self.table = gtk.Table(1, 1, False)
        self.vbox.pack_start(self.table, False, True, 0)
        self.table.show()
	
	
        # Add a check button to select displaying of the trough text
        self.check = gtk.CheckButton()
	self.activity_check = self.check
        self.table.attach(self.check, 0, 1, 0, 1,
                     gtk.EXPAND  | gtk.FILL, gtk.EXPAND | gtk.FILL,
                     1, 1)
        self.check.connect("clicked", self.toggle_activity_mode)

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
        self.vbox.pack_start(self.filer, True, True, 0)
	self.filer.show()

        # Avslutaknapp
        self.avsluta= gtk.Button("Avsluta")
        self.avsluta.connect("clicked", lambda w: gtk.main_quit())
	self.vbox.pack_start(self.avsluta, True, True,0)
        self.avsluta.show()

	#Knappar i undermenyer
	#Knappar under kommunikation
	#i en vbox
        self.vbox2 = gtk.VBox(True, 0)
	self.vbox2.set_size_request(198, 95)
        self.vbox2.show()
	
	# Textmeddelande
	self.text = gtk.Button("Textmeddelande")
        self.text.connect("clicked", self.callback, "Textmeddelande")
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

	# Ritar ut fyra objekt
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
	self.vbox3 = gtk.VBox(False, 0)
        self.vbox3.show()
	
	#create a new label.
        self.label = gtk.Label("Anvandare	symbol	datum tid")
        self.label.set_alignment(0, 0)
        self.vbox3.pack_start(self.label, False, False, 0)
        self.label.show()
	
	#Packa karta
	self.vbox3.pack_start(self.startakarta,True,True,0)
	self.hbox.pack_start(self.vbox3, True, True, 0)
    	self.hbox.show()
	self.window.add(self.hbox)
        self.window.show()

def main():
    gtk.main()

if __name__ == "__main__":
    MenuExample()
    main()