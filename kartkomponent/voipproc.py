#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
import osso
pygst.require("0.10")
import gst

class Mainstream:
	def __init__(self):
		self.choose = 2
		self.HOSTIP = '130.236.217.66'
		self.MYPORT = 5000
		self.HOSTPORT = 5000
	def run(self, choose, HOSTIP, MYPORT, HOSTPORT):
		self.choose = choose
		self.HOSTIP = HOSTIP
		self.MYPORT = MYPORT
		self.HOSTPORT = HOSTPORT
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Videosamtal")
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
		#Rostsamtal = 1
		if(self.choose == 1):
			print "kor jag ettan?"
			print self.HOSTIP
			print self.MYPORT
			print self.HOSTPORT
			self.player = gst.parse_launch("udpsrc port="+str(self.MYPORT)+" ! audio/x-iLBC,rate=8000,channels=1,mode=20 ! dspilbcsink")
			self.player1 = gst.parse_launch("dspilbcsrc dtx=0 ! audio/x-iLBC,rate=8000,channels=1,mode=20  ! udpsink host="+self.HOSTIP+" port= "+str(self.MYPORT))
			bus = self.player.get_bus()
			bus.add_signal_watch()
			bus.enable_sync_message_emission()
			bus.connect("message", self.on_message)
			bus.connect("sync-message::element", self.on_sync_message)
			bus1 = self.player1.get_bus()
			bus1.add_signal_watch()
			bus1.enable_sync_message_emission()
			bus1.connect("message", self.on_message)
			bus1.connect("sync-message::element", self.on_sync_message)
		#Videosamtal = 2
		elif (self.choose == 2):
			print "kor jag tvaan?"
			self.player2 = gst.parse_launch("v4l2src ! video/x-raw-yuv,width=352,height=288,framerate=8/1 ! hantro4200enc ! rtph263pay ! udpsink host="+self.HOSTIP+" port="+str(self.MYPORT))
			self.player3 = gst.parse_launch("udpsrc port="+str(self.MYPORT)+" caps=application/x-rtp,clock-rate=90000 ! rtph263depay ! hantro4100dec ! xvimagesink")
			bus2 = self.player2.get_bus()
			bus2.add_signal_watch()
			bus2.enable_sync_message_emission()
			bus2.connect("message", self.on_message)
			bus2.connect("sync-message::element", self.on_sync_message)
			bus3 = self.player3.get_bus()
			bus3.add_signal_watch()
			bus3.enable_sync_message_emission()
			bus3.connect("message", self.on_message)
			bus3.connect("sync-message::element", self.on_sync_message)
		#Videorostsamtal = 3
		elif (self.choose == 3):
			print "kor jag trean?"
			self.player = gst.parse_launch("udpsrc port="+str(self.MYPORT)+" ! audio/x-iLBC,rate=8000,channels=1,mode=20 ! dspilbcsink")
			self.player1 = gst.parse_launch("dspilbcsrc dtx=0 ! audio/x-iLBC,rate=8000,channels=1,mode=20  ! udpsink host="+self.HOSTIP+" port= "+str(self.MYPORT))
			self.player2 = gst.parse_launch("v4l2src ! video/x-raw-yuv,width=352,height=288,framerate=8/1 ! hantro4200enc ! rtph263pay ! udpsink host="+self.HOSTIP+" port="+str(self.MYPORT))
			self.player3 = gst.parse_launch("udpsrc port="+str(self.MYPORT)+" caps=application/x-rtp,clock-rate=90000 ! rtph263depay ! hantro4100dec ! xvimagesink")
			bus = self.player.get_bus()
			bus.add_signal_watch()
			bus.enable_sync_message_emission()
			bus.connect("message", self.on_message)
			bus.connect("sync-message::element", self.on_sync_message)
			bus1 = self.player1.get_bus()
			bus1.add_signal_watch()
			bus1.enable_sync_message_emission()
			bus1.connect("message", self.on_message)
			bus1.connect("sync-message::element", self.on_sync_message)
			bus2 = self.player2.get_bus()
			bus2.add_signal_watch()
			bus2.enable_sync_message_emission()
			bus2.connect("message", self.on_message)
			bus2.connect("sync-message::element", self.on_sync_message)
			bus3 = self.player3.get_bus()
			bus3.add_signal_watch()
			bus3.enable_sync_message_emission()
			bus3.connect("message", self.on_message)
			bus3.connect("sync-message::element", self.on_sync_message)
	def start_stop(self, w):
		if self.button.get_label() == "Start":
			if (self.choose==1):
				self.player.set_state(gst.STATE_PLAYING)
				self.player1.set_state(gst.STATE_PLAYING)
			elif (self.choose==2):
				self.player2.set_state(gst.STATE_PLAYING)
				self.player3.set_state(gst.STATE_PLAYING)
				
			elif (self.choose==3):
				self.player.set_state(gst.STATE_PLAYING)
				self.player1.set_state(gst.STATE_PLAYING)
				self.player2.set_state(gst.STATE_PLAYING)
				self.player3.set_state(gst.STATE_PLAYING)
			self.button.set_label("Stop")
		else:
			if (self.choose==1):
				self.player.set_state(gst.STATE_NULL)
				self.player1.set_state(gst.STATE_NULL)
			elif (self.choose==2):
				self.player2.set_state(gst.STATE_NULL)
				self.player3.set_state(gst.STATE_NULL)
			elif (self.choose==3):
				self.player.set_state(gst.STATE_NULL)
				self.player1.set_state(gst.STATE_NULL)
				self.player2.set_state(gst.STATE_NULL)
				self.player3.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
				
	def exit(self, widget, data=None):
		gtk.main_quit()
		
	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			if (self.choose==1):
				self.player.set_state(gst.STATE_NULL)
				self.player1.set_state(gst.STATE_NULL)
			elif (self.choose==2):
				self.player2.set_state(gst.STATE_NULL)
				self.player3.set_state(gst.STATE_NULL)
			elif (self.choose==3):
				self.player.set_state(gst.STATE_NULL)
				self.player1.set_state(gst.STATE_NULL)
				self.player2.set_state(gst.STATE_NULL)
				self.player3.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
		elif t == gst.MESSAGE_ERROR:
			if (self.choose==1):
				self.player.set_state(gst.STATE_NULL)
				self.player1.set_state(gst.STATE_NULL)
			elif (self.choose==2):
				self.player2.set_state(gst.STATE_NULL)
				self.player3.set_state(gst.STATE_NULL)
			elif (self.choose==3):
				self.player.set_state(gst.STATE_NULL)
				self.player1.set_state(gst.STATE_NULL)
				self.player2.set_state(gst.STATE_NULL)
				self.player3.set_state(gst.STATE_NULL)
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
def main():
	gtk.main()

def onlyone(interface, method, arguments, user_data):
	print "nu er vi inne i onlyone"
	Mainstream().run(arguments[0],arguments[1],arguments[2],arguments[3])
	
if __name__ == "__main__":
	osso_c = osso.Context("voipproc", "0.0.1", False)
	osso_rpc = osso.Rpc(osso_c)
	osso_rpc.set_rpc_callback("thor.voipproc","/thor/voipproc","thor.voipproc",onlyone)
	#Mainstream().run(1,'130.236.219.132', '5000','5001')
	gtk.gdk.threads_init()
	main()
	




#CONNECTAR
		
