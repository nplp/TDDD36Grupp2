import gtk

class Inlogg():
    
    def __init__(self):

	window = gtk.Window()
	#window.connect("delete_event", self.delete_event)
	#window.connect("destroy", self.destroy)
	
	#Vbox for innehall
	self.vbox = gtk.VBox(False,5)
	self.vbox.set_border_width(50)	
	
	#Skriv in en anvandare
        self.anvandare = gtk.Label("Anvandarnamn")
        self.anvandare.set_alignment(0, 0)
	self.anvandare.show()
	self.vbox.pack_start(self.anvandare, False, False, 0)
	
	self.entry = gtk.Entry()
        #self.entry.set_max_length(250)
	self.entry.show()	
	self.vbox.pack_start(self.entry, False, False, 0)
	
	#Skriv in ditt losen
        self.losen = gtk.Label("Losenord")
        self.losen.set_alignment(0, 0)
	self.losen.show()
	self.vbox.pack_start(self.losen, False, False, 0)
	
	self.entry1 = gtk.Entry()
        #self.entry1.set_max_length(250)
	self.entry1.show()	
	self.vbox.pack_start(self.entry1, False, False, 0)
	
	self.loggin = gtk.Button("Logga in")
        self.loggin.connect("clicked", self.send, "Logga in")
	self.loggin.show()
	self.vbox.pack_start(self.loggin,False,False,0)
	
	self.vbox.show()
	window.add(self.vbox)
	window.show()
    
    def send():
    	print "nu loggas jag in"
	
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    Inlogg()
    main()