#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class GTK_Main:

	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Awesome AP")
		window.set_default_size(500, 400)
		window.connect("destroy", gtk.main_quit, "WM destroy")
		vbox = gtk.VBox()
		window.add(vbox)
		self.movie_window = gtk.DrawingArea()
		vbox.add(self.movie_window)
		hbox = gtk.HBox()
		vbox.pack_start(hbox, False)
		hbox.set_border_width(10)
		hbox.pack_start(gtk.Label())
		self.button = gtk.Button("Start")
		self.button.connect("clicked", self.start_stop)
		hbox.pack_start(self.button, False)
		self.button2 = gtk.Button("Quit")
		self.button2.connect("clicked", self.exit)
		hbox.pack_start(self.button2, False)
		hbox.add(gtk.Label())
		window.show_all()
		#HOSTAR
		self.player= gst.parse_launch("v4l2src ! video/x-raw-yuv,width=352,height=288,framerate=8/1 ! hantro4200enc ! rtph263pay ! udpsink host=130.236.219.251 port=5434")
		print "skickar video"
		#Connectar
		self.player1 = gst.parse_launch("udpsrc port=5435 caps=application/x-rtp,clock-rate=90000 ! rtph263depay ! hantro4100dec ! xvimagesink")
		print "lyssnar video"
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
		print "startar bus"
		bus1= self.player1.get_bus()
		bus1.add_signal_watch()
		bus1.enable_sync_message_emission()
		bus1.connect("message", self.on_message)
		bus1.connect("sync-message::element", self.on_sync_message)
		print "startar bus1"
		
	def start_stop(self, w):
		if self.button.get_label() == "Start":
			self.button.set_label("Stop")
			self.player.set_state(gst.STATE_PLAYING)
			self.player1.set_state(gst.STATE_PLAYING)
		else:
			self.player.set_state(gst.STATE_NULL)
			self.player1.set_state(gst.STATE_NULL)
			self.button.set_label("Start")

	def exit(self, widget, data=None):
		gtk.main_quit()

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			self.player1.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.player.set_state(gst.STATE_NULL)
			self.player1.set_state(gst.STATE_NULL)
			self.button.set_label("Start")

	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			# Assign the viewport
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", False)
			imagesink.set_xwindow_id(self.movie_window.window.xid)

GTK_Main()
gtk.gdk.threads_init()
gtk.main()


