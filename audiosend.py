#
import gobject, pygst
#
pygst.require("0.10")
#
import gst
#
 
#
# Callback for the decodebin source pad
#
def new_decode_pad(dbin, pad, islast):
        pad.link(convert.get_pad("sink"))
#
 
#
# create a pipeline and add [tcpserversrc ! decodebin ! audioconvert ! alsasink]
#
pipeline = gst.Pipeline("server")
#
 
#
tcpsrc = gst.element_factory_make("tcpserversrc", "source")
#
pipeline.add(tcpsrc)
#
tcpsrc.set_property("host", "127.0.0.1")
#
tcpsrc.set_property("port", 3000)
#
 
#
decode = gst.element_factory_make("decodebin", "decode")
#
decode.connect("new-decoded-pad", new_decode_pad)
#
pipeline.add(decode)
#
tcpsrc.link(decode)
#
 
#
convert = gst.element_factory_make("audioconvert", "convert")
#
pipeline.add(convert)
#
 
#
sink = gst.element_factory_make("alsasrc", "sink")
#
pipeline.add(sink)
#
convert.link(sink)
#
 
#
pipeline.set_state(gst.STATE_PLAYING)
#
 
#
# enter into a mainloop
#
loop = gobject.MainLoop()
#
loop.run()