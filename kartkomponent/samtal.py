import gtk

	
class Samtal():	
	
    def fil():
	print hej
	
    def __init__(self):	
	#self.window=gtk.Window()
	#self.window.set_border_width(10)

        self.hbox = gtk.HBox(True, 0)
	self.hbox.set_size_request(198, 100)
        self.vbox = gtk.VBox(True, 0)
	#self.vbox.set_size_request(198, 95)
        self.vbox.show()

    	# Rost
        self.rost= gtk.ToggleButton("Rost")
        self.rost.connect("toggled", self.fil, "Filer")
	self.rost.show()
        self.vbox.pack_start(self.rost, True, True, 0)
    	# Video
        self.video= gtk.ToggleButton("Video")
        self.video.connect("toggled", self.fil, "Filer")
	self.video.show()
        self.vbox.pack_start(self.video, True, True, 0)
    	# Rost och video
        self.rov= gtk.ToggleButton("Rost och video")
        self.rov.connect("toggled", self.fil, "Filer")
	self.rov.show()
        self.vbox.pack_start(self.rov, True, True, 0)
    	# Ring
        self.ring= gtk.Button("Ring")
        self.ring.connect("clicked", self.fil, "Filer")
	self.ring.show()
        self.vbox.pack_start(self.ring, True, True, 0)
	
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