#!/usr/bin/python

# ZetCode PyGTK tutorial 
#
# This example demonstrates the ComboBox widget
#
# author: jan bodnar
# website: zetcode.com 
# last edited: February 2009
from databasklient import *
import gtk

class PyApp(gtk.Window):
    def __init__(self):
        super(PyApp, self).__init__()
        
        self.set_title("ComboBox")
        self.set_default_size(250, 200)
        self.set_position(gtk.WIN_POS_CENTER)
 
	
	temp=get_item_all()
	listan=""
	for n in temp:
        	listan+=(n.name+" "+str(n.count)+"st "+n.location+"\n")
	self.label = gtk.Label(listan)

        fixed = gtk.Fixed()
        #fixed.put(cb, 50, 30)
        
        fixed.put(self.label, 10, 10)
	#fixed.put(self.textview, 70, 150)
        self.add(fixed)


        self.connect("destroy", gtk.main_quit)
        self.show_all()


    #def on_changed(self, widget):
        #self.label.set_label(widget.get_active_text()) 

PyApp()
gtk.main()
