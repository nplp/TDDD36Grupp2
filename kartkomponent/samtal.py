import gtk
import osso

	
class Samtal():	
    choose = 1	
	
    def ringa(self, widget, event, data=None):
	osso_c = osso.Context("ring", "0.0.1", False)
	osso_rpc = osso.Rpc(osso_c)
	print "vi sparar!"
	osso_rpc.rpc_run("thor.voipproc", "/thor/voipproc", "thor.voipproc", "onlyone", (self.choose, "130.236.216.227", 5000, 5000))
	
    def samma(self,widget,event,data=None):
	self.rostknapp.set_active(False)
	self.rovknapp.set_active(False)
	self.videoknapp.set_active(False)
	
    def rost(self, widget, event, data=None):
	if widget.get_active():
		self.rostknapp.set_active(True)
		self.rovknapp.set_active(False)
		self.videoknapp.set_active(False)
		self.choose = 1
	else:
          	self.samma(widget, data)
		
    def video(self, widget, event, data=None):
	if widget.get_active():
		self.videoknapp.set_active(True)
		self.rovknapp.set_active(False)
		self.rostknapp.set_active(False)
		self.choose = 2
	else:
          	self.samma(widget, data)
		
    def rov(self, widget, event, data=None):
	if widget.get_active():
		self.rovknapp.set_active(True)
		self.rostknapp.set_active(False)
		self.videoknapp.set_active(False)
		self.choose = 3
	else:
          	self.samma(widget, data)
	
    def __init__(self):	
	#self.window=gtk.Window()
	#self.window.set_border_width(10)

        self.hbox = gtk.HBox(False, 0)
	#self.hbox.set_size_request(198, 100)
        self.vbox = gtk.VBox(True, 0)
	#self.vbox.set_size_request(198, 95)
        self.vbox.show()

    	# Rost
        self.rostknapp= gtk.ToggleButton("Rost")
        self.rostknapp.connect("toggled", self.rost, "Rost")
	self.rostknapp.show()
        self.vbox.pack_start(self.rostknapp, False, True, 0)
    	# Video
        self.videoknapp = gtk.ToggleButton("Video")
        self.videoknapp.connect("toggled", self.video, "Video")
	self.videoknapp.show()
        self.vbox.pack_start(self.videoknapp, True, True, 0)
    	# Rost och video
        self.rovknapp = gtk.ToggleButton("Rost och video")
        self.rovknapp.connect("toggled", self.rov, "Rost och video")
	self.rovknapp.show()
        self.vbox.pack_start(self.rovknapp, True, True, 0)
    	# Ring
        self.ringknapp = gtk.Button("Ring")
        self.ringknapp.connect("clicked", self.ringa, "Ring")
	self.ringknapp.show()
        self.vbox.pack_start(self.ringknapp, True, True, 20)
	
	self.hbox.pack_start(self.vbox,True,True,0)	
	self.lista = gtk.TextView()	
	self.lista.set_size_request(450,369)
	self.lista.show()
	self.hbox.pack_start(self.lista,True,True,0)
	#self.window.add(self.hbox)
	#self.window.show()

def main():
	gtk.main()

if __name__ == "__main__":
	Samtal()
	main()