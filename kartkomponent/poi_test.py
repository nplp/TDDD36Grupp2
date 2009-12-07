import gtk

class Poi_ruta():

    def __init__(self):
	window = gtk.Window()
	window.set_size_request(300,300)
	window.show()

        self.vbox = gtk.VBox(False, 0)
	self.vbox.set_border_width(50)	
        self.vbox.show()
	
	self.enhet = gtk.Label("Enhet")
        self.enhet.set_alignment(0, 0)
	self.enhet.show()
	self.vbox.pack_start(self.enhet, False, False, 0)
	
	self.x_coord = gtk.Label("X-kordinat")
        self.x_coord.set_alignment(0, 0)
	self.x_coord.show()
	self.vbox.pack_start(self.x_coord, False, False, 0)
	
	self.xentry = gtk.Entry()
	self.xentry.show()	
	self.vbox.pack_start(self.xentry, False, False, 0)

	self.y_coord = gtk.Label("Y-kordinat")
        self.y_coord.set_alignment(0, 0)
	self.y_coord.show()
	self.vbox.pack_start(self.y_coord, False, False, 0)
	
	self.yentry = gtk.Entry()
	self.yentry.show()	
	self.vbox.pack_start(self.yentry, False, False, 0)

	self.beskrivning = gtk.Label("Beskrivning")
        self.beskrivning.set_alignment(0, 0)
	self.beskrivning.show()
	self.vbox.pack_start(self.beskrivning, False, False, 0)

	self.beskriv = gtk.TextView()
	self.beskriv.set_wrap_mode(gtk.WRAP_WORD_CHAR)	
	self.beskriv.show()
	self.vbox.pack_start(self.beskriv, False, False, 0)
	
	self.stang = gtk.Button("Stang")
        self.stang.connect("clicked", self.send, "Stang")
	self.stang.show()
	self.vbox.pack_start(self.stang,True,True,0)

	window.add(self.vbox)

    def send():
    	print "hej"
	
def main():
	gtk.main()

if __name__ == "__main__":
    Poi_ruta()
    main()	