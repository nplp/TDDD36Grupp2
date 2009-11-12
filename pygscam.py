#! /usr/bin/env python

import string
import array
import time
import platform
import Numeric
import gtk
import gst

class ShowMe:
	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Webcam-Viewer")
		window.connect("destroy", gtk.main_quit, "WM destroy")
		vbox = gtk.VBox()
		window.add(vbox)
		self.movie_window = gtk.DrawingArea()
		vbox.add(self.movie_window)
		hbox = gtk.HBox()
		vbox.pack_start(hbox, False)
		hbox.set_border_width(10)
		hbox.pack_start(gtk.Label())
                self.takePicture = 0
		self.button0 = gtk.Button(" Oh Snap!")
		self.button0.connect("clicked", self.onTakePicture)
		hbox.pack_start(self.button0, False)
		self.button = gtk.Button("Start")
		self.button.connect("clicked", self.start_stop)
		hbox.pack_start(self.button, False)
		self.button2 = gtk.Button("Quit")
		self.button2.connect("clicked", self.exit)
		hbox.pack_start(self.button2, False)
		hbox.add(gtk.Label())
		window.show_all()
		self.width = 352
		self.height = 288
		self.width = 640
		self.height = 480
                self.machine = platform.uname()[4]
                self.imageSink = None
                self.probeHandlerID = None

                if self.machine == 'armv6l':
                    self.player = gst.Pipeline('ThePipe')
                    src = gst.element_factory_make("gconfv4l2src","camSrc")
                    self.player.add(src)
                    for p in src.pads():
                        #print p.get_caps().to_string()
                        print p.get_name()
                    caps = gst.element_factory_make("capsfilter", "caps")
                    caps.set_property('caps', gst.caps_from_string(\
                        'video/x-raw-rgb,width=%d,height=%d,\
                        framerate=15/1'%(self.width,self.height)))
                        #'video/x-raw-rgb,width=%d,height=%d,bpp=16,depth=16,\
                    self.player.add(caps)
                    #filt = gst.element_factory_make("ffmpegcolorspace", "filt")
                    #self.player.add(filt)
                    tee = gst.element_factory_make("tee", "tee")
                    self.player.add(tee)
                    screenQueue = gst.element_factory_make("queue", "screenQueue")
                    self.player.add(screenQueue)
                    screenCaps = gst.caps_from_string('video/x-raw-rgb,width=352,height=288,framerate=15/1')
                    caps2 = gst.element_factory_make("capsfilter", "caps2")
                    caps2.set_property('caps', gst.caps_from_string(
                        'video/x-raw-rgb,width=%d,height=%d,bpp=16,depth=16,\
                        framerate=15/1'%(self.width,self.height)))
                    self.player.add(caps2)
                    swidth = self.width
                    sheight = self.height
                    swidth = 352
                    sheight = 288
                    swidth = 320
                    sheight = 240
                    swidth = self.width/2
                    sheight = self.height/2
                    screenCaps = gst.element_factory_make("capsfilter", "screenCaps")
                    screenCaps.set_property('caps', gst.caps_from_string(\
                        'video/x-raw-rgb,width=%d,height=%d\
                        '%(swidth,sheight)))
                        #,framerate=15/1'%(swidth,sheight)))
                    self.player.add(screenCaps)
                    filt = gst.element_factory_make("videoscale", "filt")
                    self.player.add(filt)
                    #tee = gst.element_factory_make("tee", "tee")
                    #self.player.add(tee)
                    #screenQueue = gst.element_factory_make("queue", "screenQueue")
                    #self.player.add(screenQueue)
                    sink = gst.element_factory_make("xvimagesink", "sink")
                    #sink = gst.element_factory_make("autovideosink", "sink")
                    self.player.add(sink)
                    #pad = src.get_pad('src')
                    #pad.add_buffer_probe(self.doBuffer)
                    #src.link_filtered(filt,caps)
                    src.link(caps)
                    caps.link(tee)
                    tee.link(screenQueue)
                    screenQueue.link(filt)
                    filt.link(screenCaps)
                    screenCaps.link(sink)
                    #screenQueue.link(sink)
                    #caps.link(filt)
                    #filt.link(caps2)
                    #caps2.link(sink)
                    imageQueue = gst.element_factory_make("queue", "imageQueue")
                    self.player.add(imageQueue)
                    imageFilter = gst.element_factory_make("ffmpegcolorspace",\
                        "imageFilter")
                    pad = imageFilter.get_pad('sink')
                    #pad.add_buffer_probe(self.doQueueBuffer)
                    self.player.add(imageFilter)
                    imageCaps = gst.element_factory_make("capsfilter", "imageCaps")
                    iCaps = gst.caps_from_string(\
                        'video/x-raw-rgb,width=%d,height=%d,bpp=24,depth=24,\
                        framerate=15/1'%(self.width,self.height))
                    self.player.add(imageCaps)
                    self.imageSink = gst.element_factory_make("fakesink", "imageSink")
                    #pad = self.imageSink.get_pad('sink')
                    #pad.add_buffer_probe(self.doImageBuffer)
                    self.player.add(self.imageSink)
                    tee.link(imageQueue)
                    imageQueue.link(imageFilter)
                    imageFilter.link_filtered(self.imageSink,iCaps)
                    #imageFilter.link(imageCaps)
                    #imageCaps.link(self.imageSink)
                else:
                    self.player = gst.Pipeline('ThePipe')
                    src = gst.element_factory_make("v4l2src","src")
                    src.set_property('device','/dev/video0')
                    self.player.add(src)
                    sink = gst.element_factory_make("autovideosink", "sink")
                    self.player.add(sink)
                    pad = src.get_pad('src')
                    pad.add_buffer_probe(self.doBuffer)
                    src.link(sink)

		# Set up the gstreamer pipeline
		#self.player = gst.parse_launch ('gconfv4l2src ! video/x-raw-yuv,width=352,height=288,framerate=(fraction)15/1 ! autovideosink')
		#self.player = gst.parse_launch ('gconfv4l2src ! video/x-raw-yuv,width=352,height=288,framerate=(fraction)15/1 ! tee name=qole qole. ! ffmpegcolorspace ! queue ! filesink location=qole.raw qole. ! queue ! autovideosink')
		#self.player = gst.parse_launch ('gconfv4l2src ! video/x-raw-rgb,width=352,height=288,framerate=(fraction)15/1 ! tee name=qole qole. ! ffmpegcolorspace ! jpegenc ! filesink location=qole.raw qole. ! queue ! autovideosink')
		#self.player = gst.parse_launch ('v4l2src ! autovideosink')

		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)

	def doQueueBuffer(self, pad, buffer):
            if self.takePicture:
                return True
            else:
                return False

	def onTakePicture(self, w):
            self.takePicture = 1
            pad = self.imageSink.get_pad('sink')
            self.probeHandlerID = pad.add_buffer_probe(self.doImageBuffer)

	def doImageBuffer(self, pad, buffer):
	    print 'doImageBuffer',len(buffer)
            if self.takePicture:
                self.takePicture = 0
	        #print 'doImageBuffer',len(buffer)
                pad = self.imageSink.get_pad('sink')
                pad.remove_buffer_probe(self.probeHandlerID)
                caps = buffer.get_caps()
                #struct = caps.get_structure(0)
                struct = caps[0]
                print 'caps',caps
                for i in range(0,struct.n_fields()):
                    fn = struct.nth_field_name(i)
                    print '  ',fn,'=',struct[fn]
                print 'start',time.localtime()
                pb = gtk.gdk.pixbuf_new_from_data(buffer,gtk.gdk.COLORSPACE_RGB,                        False,8,self.width,self.height,self.width*3)
                pb.save('/home/user/MyDocs/.images/daperl01.png','png')
                #pb.save('/tmp/daperl00.png','png')
                print 'stop ',time.localtime()
	    return True

	def doBuffer(self, pad, buffer):
	    print 'doBuffer',len(buffer)
	    return True
            if self.takePicture:
                self.takePicture = 0
                self.start_stop(pad)
                print 'buffer length =',len(buffer)
                caps = buffer.get_caps()
                #struct = caps.get_structure(0)
                struct = caps[0]
                print 'caps',caps
                for i in range(0,struct.n_fields()):
                    fn = struct.nth_field_name(i)
                    print '  ',fn,'=',struct[fn]
                # 63488 2016 31
                # 0xf8  0x07,0xe0  0x1f
                if self.machine != 'armv6l':
                    return True
                da = array.array('H')
                da.fromstring(buffer)
                zo = array.array('B')
                zo.fromstring('0'*3*len(buffer))
                zos = zo.tostring()
                print 'da len',len(da)
                print 'zo len',len(zo)
                print 'zos len',len(zos)
                print 'start',time.localtime()
#                for i in range(0,8):
#                    for j in range(0,8):
#                        print "%04X %02x%02x" % (da[i*8+j],\
#                            ord(buffer[i*16+j*2]),ord(buffer[i*16+j*2+1])),
#                    print ''
                i = 0
                for v in da:
                    zo[i] = (0xf800 & v) >> 8
                    zo[i+1] = (0x07e0 & v) >> 3
                    zo[i+2] = (0x001f & v) << 3
                    i += 3
                pb = gtk.gdk.pixbuf_new_from_data(zo,gtk.gdk.COLORSPACE_RGB,                        False,8,self.width,self.height,self.width*3)
                #pb.save('/home/user/MyDocs/.images/daperl00.png','png')
                pb.save('/tmp/daperl00.png','png')
                print 'stop ',time.localtime()
                print pb.get_width(),pb.get_height()
                self.start_stop(pad)
                return True
                p = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,352,288)
                pa = p.get_pixels()
                pa = p.get_pixels()
                pal = list(pa)
                for i in range(0,len(buffer)/2):
                    pal[i*3] = "%c" % (0xf8 & ord(buffer[i*2+1]))
                    pal[i*3+1] = "%c" % (((0x07 & ord(buffer[i*2+1])) << 5) |\
                        ((0xe0 & ord(buffer[i*2])) >> 5))
                    pal[i*3+2] = "%c" % ((0x1f & ord(buffer[i*2])) << 3)
            return True

	def start_stop(self, w):
		if self.button.get_label() == "Start":
			self.button.set_label("Stop")
			self.player.set_state(gst.STATE_PLAYING)
		else:
			self.player.set_state(gst.STATE_NULL)
			self.button.set_label("Start")

	def exit(self, widget, data=None):
		gtk.main_quit()

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.player.set_state(gst.STATE_NULL)
			self.button.set_label("Start")

	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			# Assign the viewport
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			imagesink.set_xwindow_id(self.movie_window.window.xid)

if __name__ == "__main__":
    gtk.gdk.threads_init()
    ShowMe()
    gtk.main()
