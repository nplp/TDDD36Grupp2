import gtk
from databasklient import *

class Lager():
	
    def __init__(self):
        self.textview = gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textview.show()
	self.line = ""

	L = get_item_all()
	for item in L:
        	self.line += item
        self.textbuffer.set_text(self.line)
	print self.line
	
    def run(self):
        #self.window.show_all()
        gtk.main()