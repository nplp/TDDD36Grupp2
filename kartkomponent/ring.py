import gtk
import simplejson as json
import osso
from databasmethod import *

import gtk
import osso

	
class Samtal():	
    choose = 2	
	
    def ringa(self, widget, event, data=None):
	osso_c = osso.Context("ring", "0.0.1", False)
	osso_rpc = osso.Rpc(osso_c)
	print "vi sparar!"
	osso_rpc.rpc_run("thor.voipproc", "/thor/voipproc", "thor.voipproc", "onlyone", (self.choose, "130.236.217.66", 5000, 5000))
	
    def samma(self,widget,event,data=None):
	self.rostknapp.set_active(False)
	self.videoknapp.set_active(False)
	
    def rost(self, widget, event, data=None):
	if widget.get_active():
		self.rostknapp.set_active(True)
		self.videoknapp.set_active(False)
		self.choose = 1
	else:
          	self.samma(widget, data)
		
    def video(self, widget, event, data=None):
	if widget.get_active():
		self.videoknapp.set_active(True)
		self.rostknapp.set_active(False)
		self.choose = 2
	else:
          	self.samma(widget, data)

    def __init__(self):

	self.vbox = gtk.VBox(False,5)
	self.vbox.set_border_width(5)	
	self.hbox = gtk.HBox(False,5)
	
	self.rostknapp = gtk.ToggleButton("Rostsamtal")
        self.rostknapp.connect("toggled", self.rost, "Rostsamtal")
	self.rostknapp.set_size_request(150,50)
	self.rostknapp.show()
	self.hbox.pack_start(self.rostknapp,False,False,2)
	
	self.videoknapp = gtk.ToggleButton("Video")
        self.videoknapp.connect("toggled", self.video, "Video")
	self.videoknapp.set_size_request(150,50)
	self.videoknapp.show()
	self.hbox.pack_start(self.videoknapp,False,False,0)
	self.vbox.pack_start(self.hbox,False,False,20)
	self.hbox.show()
	
	self.ringknapp = gtk.Button("Ring")
        self.ringknapp.connect("clicked", self.ringa, "Ring")
	self.ringknapp.set_size_request(130,50)
	self.ringknapp.show()
	self.vbox.pack_start(self.ringknapp,False,False,0)	
		
	#self.vbox.show()
	
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    Samtal()
    main()