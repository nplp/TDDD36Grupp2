#!/usr/bin/python

import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk

class Main:
	def __init__(self):
		self.pipeline = gst.Pipeline("mypipeline")

		self.audiotestsrc = gst.element_factory_make("audiotestsrc", "audio")
		self.pipeline.add(self.audiotestsrc)

		self.sink = gst.element_factory_make("alsasink", "sink")
		self.pipeline.add(self.sink)

		self.audiotestsrc.link(self.sink)

		self.pipeline.set_state(gst.STATE_PLAYING)

start=Main()
gtk.main()
