#!/usr/bin/env python

import sys, os, time
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

BKGRNDR=0.0
BKGRNDG=0.2
BKGRNDB=0.7
BKGRNDA=0.8
WINDOW_STICK=False
WINDOW_KEEPABOVE=False
WINDOW_DECORATED=True

WIDTH=790
HEIGHT=480
TOP=100
LEFT=100

timeElapsed = 0
videoDevice="/dev/video0"
videoProperties="image/jpeg,width=640,height=480,framerate=30/1"
audioDevice="hw:1,0"
audioProperties="audio/x-raw-int,rate=16000,channels=1,depth=16"
videoSink="ximagesink"
filePath=os.path.expanduser("~") + '/Desktop'
mpeg4Properties=""

class GTK_Main:

	def __init__(self):
		global filePath, videoDevice, videoProperties, videoSink
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Video-Recorder")
		window.set_size_request(WIDTH, HEIGHT)
		window.set_decorated(WINDOW_DECORATED)
		window.connect("destroy", gtk.main_quit, "WM destroy")
		window.move(LEFT, TOP)
		mainBox = gtk.HBox()
		window.add(mainBox)
		vbox = gtk.VBox()
		mainBox.add(vbox)
		self.movie_window = gtk.DrawingArea()
		vbox.add(self.movie_window)
		controlBox = gtk.VBox()
		mainBox.pack_start(controlBox, False)
		controlBox.set_size_request(150,480)
		controlBox.set_border_width(10)
		controlBox.pack_start(gtk.Label())
		self.button = gtk.Button("Record (HQ)")
		self.button.connect("clicked", self.start_stop_recordHQ)
		controlBox.pack_start(self.button, False)
		self.button1 = gtk.Button("Record (LQ)")
		self.button1.connect("clicked", self.start_stop_recordLQ)
		controlBox.pack_start(self.button1, False)
		self.button3 = gtk.Button("Quit")
		self.button3.connect("clicked", self.exit)
		controlBox.pack_start(self.button3, False)
		controlBox.add(gtk.Label())
		self.ET = gtk.Label()
		self.ET.set_line_wrap(True)
		controlBox.pack_start(self.ET, False)
		window.show_all()

		self.player = gst.parse_launch ("v4l2src device="+videoDevice+" queue-size=16 ! "+videoProperties+" ! ffdec_mjpeg ! queue2 max-size-buffers=10000 max-size-bytes=0 max-size-time=0 ! ffmpegcolorspace ! "+videoSink)
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect('message', self.on_message)
		bus.connect('sync-message::element', self.on_sync_message)
		self.start(firstRun = True)
		self.recorderLQ = None
		self.recorderHQ = None

	def SetPipelines(self, Type):
		global filePath, videoDevice, videoProperties, videoSink, audioDevice, audioProperties, mpeg4Properties
		if Type == "LQ":
			self.recorderLQ = gst.parse_launch ("v4l2src device="+videoDevice+" queue-size=16 ! "+videoProperties+" ! ffdec_mjpeg ! queue max-size-buffers=10000 max-size-bytes=0 max-size-time=0 ! queue ! tee name=tee tee. ! ffmpegcolorspace ! queue ! ffenc_mpeg4 ! queue ! mux. avimux name=mux alsasrc device="+audioDevice+" ! audiorate ! "+audioProperties+" ! queue ! audioconvert ! lame !  mux. mux. ! queue ! filesink location="+filePath+time.strftime("%Y%m%d%H%M%S", time.localtime()) +".avi tee. ! ffmpegcolorspace ! queue ! "+videoSink)
			busrecLQ = self.recorderLQ.get_bus()
			busrecLQ.add_signal_watch()
			busrecLQ.enable_sync_message_emission()
			busrecLQ.connect('message', self.on_message)
			busrecLQ.connect('sync-message::element', self.on_sync_message)
			self.recorderHQ = None
		elif Type == "HQ":
			self.recorderHQ = gst.parse_launch ("v4l2src device="+videoDevice+" queue-size=16 ! "+videoProperties+" ! tee name=tee tee. ! queue ! mux. avimux name=mux alsasrc device="+audioDevice+" ! audiorate ! "+audioProperties+" ! queue ! audioconvert ! lame !  mux. mux. ! queue ! filesink location="+filePath+time.strftime("%Y%m%d%H%M%S", time.localtime()) +".avi tee. ! ffdec_mjpeg ! queue max-size-buffers=10000 max-size-bytes=0 max-size-time=0 ! queue ! ffmpegcolorspace ! "+videoSink)
			busrecHQ = self.recorderHQ.get_bus()
			busrecHQ.add_signal_watch()
			busrecHQ.enable_sync_message_emission()
			busrecHQ.connect('message', self.on_message)
			busrecHQ.connect('sync-message::element', self.on_sync_message)
			self.busrecLQ = None

	def start(self, firstRun = False):
		if (firstRun == True):
			time.sleep(1)
		self.player.set_state(gst.STATE_PLAYING)
	def start_stop_recordHQ(self, w):
		global timeElapsed
		if self.button.get_label() == "Record (HQ)":
			self.SetPipelines("HQ")
			timeElapsed = 0
			self.button.set_label("Stop Recording")
			self.player.set_state(gst.STATE_NULL)
			if self.recorderLQ != None:
				self.recorderLQ.set_state(gst.STATE_NULL)
			time.sleep(1)
			self.recorderHQ.set_state(gst.STATE_PLAYING)
			self.button.set_sensitive(True)
			self.button1.set_sensitive(False)
			self.updateET()
		else:
			self.recorderHQ.set_state(gst.STATE_NULL)
			time.sleep(1)
			if self.recorderLQ != None:
				self.recorderLQ.set_state(gst.STATE_NULL)
			self.player.set_state(gst.STATE_PLAYING)
			self.button.set_label("Record (HQ)")
			self.button.set_sensitive(True)
			self.button1.set_sensitive(True)
			self.ET.set_label("")
	def start_stop_recordLQ(self, w):
		global timeElapsed
		if self.button1.get_label() == "Record (LQ)":
			self.SetPipelines("LQ")
			timeElapsed = 0
			self.button1.set_label("Stop Recording")
			self.player.set_state(gst.STATE_NULL)
			if self.recorderHQ != None:
				self.recorderHQ.set_state(gst.STATE_NULL)
			time.sleep(1)
			self.recorderLQ.set_state(gst.STATE_PLAYING)
			self.button1.set_sensitive(True)
			self.button.set_sensitive(False)
			self.updateET()
		else:
			self.recorderLQ.set_state(gst.STATE_NULL)
			time.sleep(1)
			if self.recorderHQ != None:
				self.recorderHQ.set_state(gst.STATE_NULL)
			self.player.set_state(gst.STATE_PLAYING)
			self.button1.set_label("Record (LQ)")
			self.button.set_sensitive(True)
			self.button1.set_sensitive(True)
			self.ET.set_label("")
	def updateET(self):
		global timeElapsed
		self.ET.set_label(str(timeElapsed)+" sec.")
		print str(timeElapsed)+" sec."
		timeElapsed = timeElapsed + 1
		if self.button.get_label() == "Stop Recording" or self.button1.get_label() == "Stop Recording":
			gobject.timeout_add(1000, self.updateET)
		else:
			self.ET.set_label("")

	def exit(self, widget, data=None):
		gtk.main_quit()

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			if self.recorderHQ != None:
				self.recorderHQ.set_state(gst.STATE_NULL)
			if self.recorderLQ != None:
				self.recorderLQ.set_state(gst.STATE_NULL)
			self.button.set_label("Record (HQ)")
			self.button1.set_label("Record (LQ)")
			self.button.set_sensitive(True)
			self.button1.set_sensitive(True)
		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			gobject.timeout_add(1000, self.ET.set_label, "Error: %s" % err)
			self.player.set_state(gst.STATE_NULL)
			if self.recorderHQ != None:
				self.recorderHQ.set_state(gst.STATE_NULL)
			if self.recorderLQ != None:
				self.recorderLQ.set_state(gst.STATE_NULL)
			self.button.set_label("Record (HQ)")
			self.button1.set_label("Record (LQ)")
			self.button.set_sensitive(True)
			self.button1.set_sensitive(True)
	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == 'prepare-xwindow-id':
			# Assign the viewport
			imagesink = message.src
			imagesink.set_property('force-aspect-ratio', True)
			imagesink.set_xwindow_id(self.movie_window.window.xid)

GTK_Main()
gtk.gdk.threads_init()
gtk.main()
