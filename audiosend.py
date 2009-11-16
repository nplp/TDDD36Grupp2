#!/usr/bin/env python
# -=- encoding: utf-8 -=-
#mathias och niklas aeger
import gobject, pygst
pygst.require("0.10")
import gst
import gobject
import sys
import os
import readline


# To the laptop that will catch everything
REMOTE_HOST = '130.236.218.122'
WRITE_AUDIO_CAPS = 'audio.caps'

mainloop = gobject.MainLoop()
pipeline = gst.Pipeline('server')
bus = pipeline.get_bus()

#alsasrc = gst.element_factory_make("autoaudiosrc")
alsasrc = gst.element_factory_make("alsasrc")
alsasrc.set_property('device', 'plughw:1,0')
q1 = gst.element_factory_make("queue", "q1")
q2 = gst.element_factory_make("queue", "q2")
audioconvert1 = gst.element_factory_make("audioconvert")
audioconvert2 = gst.element_factory_make("audioconvert")
vorbisenc = gst.element_factory_make("vorbisenc")
rtpvorbispay = gst.element_factory_make("rtpvorbispay")
udpsink_rtpout = gst.element_factory_make("udpsink", "udpsink0")
udpsink_rtpout.set_property('host', REMOTE_HOST)
udpsink_rtpout.set_property('port', 11000)
udpsink_rtcpout = gst.element_factory_make("udpsink", "udpsink1")
udpsink_rtcpout.set_property('host', REMOTE_HOST)
udpsink_rtcpout.set_property('port', 11001)
udpsrc_rtcpin = gst.element_factory_make("udpsrc", "udpsrc0")
udpsrc_rtcpin.set_property('port', 11002)

rtpbin = gst.element_factory_make('gstrtpbin', 'gstrtpbin')

# Add elements
pipeline.add(alsasrc, q1, audioconvert1, audioconvert2, vorbisenc, rtpvorbispay, rtpbin, udpsink_rtpout, udpsink_rtcpout, udpsrc_rtcpin)

# Link them
alsasrc.link(audioconvert1)
audioconvert1.link(vorbisenc)
vorbisenc.link(rtpvorbispay)
rtpvorbispay.link_pads('src', rtpbin, 'send_rtp_sink_0')
rtpbin.link_pads('send_rtp_src_0', udpsink_rtpout, 'sink')
rtpbin.link_pads('send_rtcp_src_0', udpsink_rtcpout, 'sink')
udpsrc_rtcpin.link_pads('src', rtpbin, 'recv_rtcp_sink_0')

def go():
    print "Setting locked state for udpsink"
    print udpsink_rtcpout.set_locked_state(gst.STATE_PLAYING)
    print "Setting pipeline to PLAYING"
    print pipeline.set_state(gst.STATE_PLAYING)
    print "Waiting pipeline to settle"
    print pipeline.get_state()
    print "Final caps writte to", WRITE_AUDIO_CAPS
    open(WRITE_AUDIO_CAPS, 'w').write(str(udpsink_rtpout.get_pad('sink').get_property('caps')))
    mainloop.run()

go()
