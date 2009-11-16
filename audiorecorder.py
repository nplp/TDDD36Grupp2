
#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import audio

audiofile= "e:\\audio.wav"

def recording():
	global S
	S=audio.Sound.open(audiofile)
	S.record()
	print "Recording"	
def playing():
	global S
	try:
		S=audio.Sound.open(audiofile)
		S.play()
		print "playing"
	except:
		print "record first"
	
def closing():
	global S
	S.stop()
	s.close()
	print "stopped"
	


class GTK_Main:

	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Awesome Sound")
		window.set_default_size(500, 400)
		window.connect("destroy", gtk.main_quit, "WM destroy")
		vbox = gtk.VBox()
		window.add(vbox)
		hbox = gtk.HBox()
		vbox.pack_start(hbox, False)
		hbox.set_border_width(10)
		hbox.pack_start(gtk.Label())
		self.button = gtk.Button("Record")
		self.button.connect("clicked", recording())
		hbox.pack_start(self.button, False)
		self.button2 = gtk.Button("Quit")
		self.button2.connect("clicked", self.exit)
		hbox.pack_start(self.button2, False)
		hbox.add(gtk.Label())
		hbox.pack_start(gtk.Label())
		self.button = gtk.Button("Play")
		self.button.connect("clicked", playing())
		hbox.pack_start(self.button, False)
		window.show_all()

	def exit(self, widget, data=None):
		gtk.main_quit()

GTK_Main()
gtk.gdk.threads_init()
gtk.main()