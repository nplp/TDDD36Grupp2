#ett window
#lista = vbox
#vad ar det som hander
#en hbox
#alternativ
#ikonen ar Button-Play-icon-32.png

import pygtk
pygtk.require('2.0')
import gtk

class Ring:

    def hej():
	print hej

    def laggpa(self, widget, event, data=None):
	self.vbox.hide()

    def __init__(self):	
        self.vbox = gtk.VBox(False, 0)
	
	#create a new label.
        self.label = gtk.Label("Hans Hansson ringer vill du")
        self.label.set_alignment(0, 0)
        self.label.show()	
        self.vbox.pack_start(self.label, False, False, 0)
	
	#Skapa en stor Hbox
	self.hbox = gtk.HBox(False, 0)
  	self.hbox.show()
	self.vbox.pack_start(self.hbox, False, False, 0)
	
        self.svara = gtk.Button("Svara")
        self.svara.connect("clicked", self.hej, "Svara")
        self.svara.show()
        self.hbox.pack_start(self.svara, False, False, 20)

        self.avsluta = gtk.Button("Lagg pa")
        self.avsluta.connect("clicked", self.laggpa, "Lagg pa")
	self.avsluta.show()
        self.hbox.pack_start(self.avsluta, False, False, 20)
	
def main():
    gtk.main()
    
if __name__ == "__main__":
    Ring()
    main()
