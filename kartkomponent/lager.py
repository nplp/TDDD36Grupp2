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
	#combobox.set_size_request(30,300)
	
	for n in temp:
		combobox.insert_text(n.item_id, (n.name+" "+str (n.count)+" "+n.location))

	
	self.lagerboxen = gtk.VBox(False, 0)
	self.lagerboxen.pack_start(combobox, False, False, 0)
	
	#self.lagerboxen.set_size_request(50, 250)
	combobox.set_active(0)
	combobox.show()

def main():
	gtk.main()
	
if __name__ == "__main__":
    Lager()
    main()
