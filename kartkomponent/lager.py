import gtk
from databasklient import *

class Lager():
	
    def __init__(self):
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        sw.add(textview)
        sw.show()
        textview.show()
	
	infile = get_items_all()

        if infile:
            string = infile.read()
            infile.close()
            textbuffer.set_text(string)



