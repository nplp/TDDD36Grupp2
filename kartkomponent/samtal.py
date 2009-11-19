import gtk
import osso

	
class Samtal():	
    choose = 1	
    def fil():
	print hej
	
    def ringa(self, widget, event, data=None):
	osso_c = osso.Context("ring", "0.0.1", False)
	osso_rpc = osso.Rpc(osso_c)
	print "vi sparar!"
	osso_rpc.rpc_run("thor.voipproc", "/thor/voipproc", "thor.voipproc", "onlyone", (self.choose, "127.0.0.1", 4000, 4001))
    
    def rost():
    	self.rovknapp.set.active(False)
	self.videoknapp.set.active(False)
    	self.rostknapp.set.active(True)
	self.choose = 1
	
    def video():
    	self.rovknapp.set.active(False)
	self.rostknapp.set.active(False)
	self.videoknapp.set.active(True)
	self.choose = 2
    def rov():
    	self.rostknapp.set.active(False)
    	self.videoknapp.set.active(False)
    	self.rovknapp.set.active(True)
	self.choose = 3
	
    def __init__(self):	
	#self.window=gtk.Window()
	#self.window.set_border_width(10)

        self.hbox = gtk.HBox(True, 0)
	self.hbox.set_size_request(198, 100)
        self.vbox = gtk.VBox(True, 0)
	#self.vbox.set_size_request(198, 95)
        self.vbox.show()

    	# Rost
        self.rostknapp= gtk.ToggleButton("Rost")
        self.rostknapp.connect("toggled", self.fil, "Filer")
	self.rostknapp.show()
        self.vbox.pack_start(self.rostknapp, True, True, 0)
    	# Video
        self.videoknapp = gtk.ToggleButton("Video")
        self.videoknapp.connect("toggled", self.fil, "Filer")
	self.videoknapp.show()
        self.vbox.pack_start(self.videoknapp, True, True, 0)
    	# Rost och video
        self.rovknapp = gtk.ToggleButton("Rost och video")
        self.rovknapp.connect("toggled", self.fil, "Filer")
	self.rovknapp.show()
        self.vbox.pack_start(self.rovknapp, True, True, 0)
    	# Ring
        self.ringknapp = gtk.Button("Ring")
        self.ringknapp.connect("clicked", self.ringa, "Filer")
	self.ringknapp.show()
        self.vbox.pack_start(self.ringknapp, True, True, 0)
	
	self.hbox.pack_start(self.vbox,True,True,0)	
	self.lista = gtk.TextView()	
	self.lista.show()
	self.hbox.pack_start(self.lista,True,True,0)
	#self.window.add(self.hbox)
	#self.window.show()

def main():
	gtk.main()

if __name__ == "__main__":
	Samtal()
	main()