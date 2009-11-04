#Hur implementerar men detta sa att det gar att titta pa den i gui?
# Set size request
#!/usr/bin/env python
# example table.py
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
class Mall:
		
    def entry_toggle_editable(self, checkbutton, entry):
	entry.set_editable(checkbutton.get_active())

    def entry_toggle_visibility(self, checkbutton, entry):
	entry.set_visibility(checkbutton.get_active())
	
    def enter_callback(self, widget, entry):
	entry_text = entry.get_text()
	print "Entry contents: %s\n" % entry_text
	
    def skriv(self, widget, entry):
	out_file= open ("test.txt","w")
	out_file.write("Avsandare:" + self.entry.get_text()+'\n')
	out_file.write("Datum: " + self.dat.get_text()+'\n') 
	out_file.write("Plats:" + self.pla.get_text() + '\n') 
	out_file.write("Beskrivning:" + self.besk.get_text()+'\n')
	out_file.write("Tidatgang: " + self.tid.get_text()+'\n')
	out_file.write("Kontaktuppgifter:" + self.kont.get_text())
	out_file.writer("check?:" + self.check.get_active())
	out_file.close()
	
	# Read a file
	#in_file = open("test.txt", "r")
	#text = in_file.read()
	#in_file.close()
	
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False
	
    def __init__(self):
        #Skapa fonster
        self.window = gtk.Window()
        self.window.set_size_request(200, 100)
        self.window.set_title("GUI")
        self.window.connect("delete_event", lambda w,e: gtk.main_quit())
	
	
	#skapa skrollwindow
	self.scrolled_window=gtk.ScrolledWindow()
	self.scrolled_window.set_border_width(10)
	self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)	

	#Vbox for innehall
	self.vbox4 = gtk.VBox(False, 0)
	self.vbox4.set_border_width(50)
	
	#Anvsandare
        self.avsandare = gtk.Label("Avsandare")
        self.avsandare.set_alignment(0, 0)
        self.vbox4.pack_start(self.avsandare, False, False, 0)
        self.avsandare.show()
	
	self.entry = gtk.Entry()
        self.entry.set_max_length(250)
 #       entry.connect("activate", self.enter_callback, entry)
	self.entry.show()
        self.vbox4.pack_start(self.entry, True, True, 0)
	
	#Datum
        self.datum = gtk.Label("Datum")
        self.datum.set_alignment(0, 0)
        self.vbox4.pack_start(self.datum, False, False, 0)
        self.datum.show()
	
	self.dat = gtk.Entry()
        self.dat.set_max_length(250)
#        entry.connect("activate", self.enter_callback, entry)
	self.dat.show()
	self.vbox4.pack_start(self.dat, True, True,0)
	
	#Plats
        self.plats = gtk.Label("Platsbeskrivning")
        self.plats.set_alignment(0, 0)
        self.vbox4.pack_start(self.plats, False, False, 0)
        self.plats.show()
	
	self.pla = gtk.Entry()
        self.pla.set_max_length(250)
        #entry.connect("activate", self.enter_callback, entry)
	self.pla.show()
        self.vbox4.pack_start(self.pla, True, True, 0)

	#Beskrivning
        self.beskrivning = gtk.Label("Beskrivning")
        self.beskrivning.set_alignment(0, 0)
        self.vbox4.pack_start(self.beskrivning, False, False, 0)
        self.beskrivning.show()
	
	self.besk = gtk.Entry()
        self.besk.set_max_length(250)
  #      entry.connect("activate", self.enter_callback, entry)
	self.besk.show()
        self.vbox4.pack_start(self.besk, True, True, 0)
	
	#Tidsatgang
        self.tidatgang = gtk.Label("Tidsatgang")
        self.tidatgang.set_alignment(0, 0)
        self.vbox4.pack_start(self.tidatgang, False, False, 0)
        self.tidatgang.show()
	
	self.tid = gtk.Entry()
        self.tid.set_max_length(50)
   #     entry2.connect("activate", self.enter_callback, entry)
	self.tid.show()
        self.vbox4.pack_start(self.tid, True, True, 0)
	
	#Kontaktuppgifter
        self.kontakt = gtk.Label("Kontaktuppgifter")
        self.kontakt.set_alignment(0, 0)
        self.vbox4.pack_start(self.kontakt, False, False, 0)
        self.kontakt.show()
	
	self.kont = gtk.Entry()
        self.kont.set_max_length(50)
        #entry3.connect("activate", self.enter_callback, entry)
	self.kont.show()
        self.vbox4.pack_start(self.kont, True, True, 0)
	
	#Hbox for checkbox
	self.hbox2 = gtk.HBox(False,0)
	self.hbox2.set_border_width(20)
	self.hbox2.show()

	#Checkboxar
	check = gtk.CheckButton("Bifoga fil")
	self.hbox2.pack_start(check, True, True, 0)
	check.set_active(True)
	check.show()
    
	check = gtk.CheckButton("hej")
	self.hbox2.pack_start(check, True, True, 0)
	check.set_active(True)
	check.show()

	self.vbox4.pack_start(self.hbox2,True,True,0)

	#Hbox3
	self.hbox3 = gtk.HBox(False, 50)
	self.hbox3.set_border_width(20)
	self.hbox3.show()
	
	#Spara data till fil knapp
	self.spar= gtk.Button("Spara")
	self.spar.connect("clicked", self.skriv, "Spara")
	self.hbox3.pack_start(self.spar,False,True,0)
	self.spar.show()
	
	#Avsluta knapp
        self.avsluta= gtk.Button("Avsluta")
        self.avsluta.connect("clicked", lambda w: gtk.main_quit())
	self.hbox3.pack_start(self.avsluta, False, True,0)
        self.avsluta.show()
	
	self.vbox4.pack_start(self.hbox3,True,True,0)

	self.scrolled_window.add_with_viewport(self.vbox4)
	self.vbox4.show()
	self.window.add(self.scrolled_window)
	self.scrolled_window.show()
        self.window.show()
	
	
	
	
	
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    Mall()
    main()
