import gtk

	
class Samtal():	
	scrolled_window=gtk.ScrolledWindow()
	scrolled_window.set_border_width(10)
	scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        hbox = gtk.HBox(False, 0)
	hbox.show()
        vbox = gtk.VBox(False, 0)
	vbox.set_size_request(198, 95)
        vbox.show()


    	# Rost
        rost= gtk.ToggleButton("Rost")
        rost.connect("toggled", fil, "Filer")
	rost.show()
        vbox.pack_start(rost, True, True, 0)
    	# Video
        video= gtk.ToggleButton("Video")
        video.connect("toggled", fil, "Filer")
	video.show()
        vbox.pack_start(video, True, True, 0)
    	# Rost och video
        rov= gtk.ToggleButton("Rost och video")
        rov.connect("toggled", fil, "Filer")
	rov.show()
        vbox.pack_start(rov, True, True, 0)
    	# Ring
        ring= gtk.Button("Filer")
        ring.connect("clicked", fil, "Filer")
	ring.show()
        vbox.pack_start(ring, True, True, 0)
	
	lista = gtk.TextView()	
	lista.show()
	hbox.pack_start(lista,True,True,0)

	hbox.pack_start(vbox,True,True,0)
	scrolled_window.add(hbox)
	scrolled_window.show()

def main():
	gtk.main()

if __name__ == "__main__":
	Samtal()
	main()