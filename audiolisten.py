#!/usr/bin/env python
# -=- encoding: utf-8 -=-
########### AUDIO RECEIVER

import gobject, pygst
pygst.require("0.10")
import gst


# Stream to:
REMOTE_HOST = '130.236.218.122'
READ_AUDIO_CAPS = 'audio.caps'

caps = open(READ_AUDIO_CAPS).read().replace('\\', '')

pipeline = gst.Pipeline('audio-receiver')

rtpbin = gst.element_factory_make('gstrtpbin')
rtpbin.set_property('latency', 1000)
udpsrc_rtpin = gst.element_factory_make('udpsrc')
udpsrc_rtpin.set_property('port', 11000)
udpsrc_caps = gst.caps_from_string(caps)
udpsrc_rtpin.set_property('caps', udpsrc_caps)
udpsrc_rtcpin = gst.element_factory_make('udpsrc')
udpsrc_rtcpin.set_property('port', 11001)
udpsink_rtcpout = gst.element_factory_make('udpsink')
udpsink_rtcpout.set_property('host', REMOTE_HOST)
udpsink_rtcpout.set_property('port', 11002)

rtpvorbisdepay = gst.element_factory_make('rtpvorbisdepay')
q1 = gst.element_factory_make("queue", "q1")
q2 = gst.element_factory_make("queue", "q2")

audioconvert = gst.element_factory_make("audioconvert")
vorbisdec = gst.element_factory_make('vorbisdec')
autoaudiosink = gst.element_factory_make('pulsesink')

pipeline.add(rtpbin, udpsrc_rtpin, udpsrc_rtcpin, udpsink_rtcpout, audioconvert,
             rtpvorbisdepay, q1, vorbisdec, autoaudiosink)

# Receive the RTP and RTCP streams
udpsrc_rtpin.link_pads('src', rtpbin, 'recv_rtp_sink_0')
udpsrc_rtcpin.link_pads('src', rtpbin, 'recv_rtcp_sink_0')
# reply with RTCP stream
rtpbin.link_pads('send_rtcp_src_0', udpsink_rtcpout, 'sink')
# Plus the RTP into the rest of the pipe...

def rtpbin_pad_added(obj, pad):
    print "PAD ADDED"
    print "  obj", obj
    print "  pad", pad
    rtpbin.link(rtpvorbisdepay)
rtpbin.connect('pad-added', rtpbin_pad_added)

gst.element_link_many(rtpvorbisdepay, q1, vorbisdec, audioconvert,
                      autoaudiosink)

def start():
    pipeline.set_state(gst.STATE_PLAYING)
    udpsink_rtcpout.set_locked_state(gst.STATE_PLAYING)
    print "Started..."

def loop():
    print "Running..."
    gobject.MainLoop().run()

if __name__ == '__main__':
    start()
    loop()
