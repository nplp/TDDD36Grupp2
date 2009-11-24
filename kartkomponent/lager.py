import gtk
from databasklient import *

class Lager():
	
    def __init__(self):
        self.textview = gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textview.show()
	self.infile = get_item_all()

        if self.infile:
            self.string = ('har ska det vara en strang av det lager vi har eller read-only och inte en buffer')
            #self.infile.close()
            self.textbuffer.set_text(self.string)


    def run(self):
        #self.window.show_all()
        gtk.main()