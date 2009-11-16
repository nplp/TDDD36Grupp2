#!/usr/bin/python
import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk
import gtk.glade

class Main:
	def __init__(self):

		# Create gui bits and bobs

		self.wTree = gtk.glade.XML("gui.glade", "mainwindow")
		
		signals = {
			"on_play_clicked" : self.OnPlay,
			"on_stop_clicked" : self.OnStop,
			"on_quit_clicked" : self.OnQuit,
		}

		self.wTree.signal_autoconnect(signals)

		# Create GStreamer bits and bobs

		self.pipeline = gst.Pipeline("mypipeline")

		self.audiotestsrc = gst.element_factory_make("audiotestsrc", "audio")
		self.audiotestsrc.set_property("freq", 200)
		self.pipeline.add(self.audiotestsrc)

		self.sink = gst.element_factory_make("alsasink", "sink")
		self.pipeline.add(self.sink)

		self.audiotestsrc.link(self.sink)

		self.window = self.wTree.get_widget("mainwindow")
		self.window.show_all()

	def OnPlay(self, widget):
		print "play"
		self.pipeline.set_state(gst.STATE_PLAYING)

	def OnStop(self, widget):
		print "stop"
		self.pipeline.set_state(gst.STATE_READY)
		
	def OnQuit(self, widget):
		gtk.main_quit()

start=Main()
gtk.main()
