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

class Lager():
    def __init__(self):	
	temp=get_item_all()
	combobox = gtk.combo_box_new_text()
	#combobox.set_size_request(300,50)
	
	for n in temp:
		combobox.insert_text(n.item_id, (n.name+" "+str (n.count)+" "+n.location))

	
	self.lagerboxen = gtk.HBox(True, 0)
	#cell = gtk.CellRendererText()
  	#combobox.pack_start(cell, True)
  	#combobox.add_attribute(cell, 'text', 0)
	self.lagerboxen.pack_start(combobox, True, True, 0)
	self.lagerboxen.set_size_request(50, 50)
	
	combobox.show()

def main():
	gtk.main()
	
if __name__ == "__main__":
    Lager()
    main()
