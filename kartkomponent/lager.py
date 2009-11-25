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
	temp=get_item_all()
	listan=""
	for n in temp:
        	listan+=(n.name+" "+str(n.count)+"st "+n.location+"\n")
	self.label = gtk.Label(listan)

        self.fixed = gtk.Fixed()
        #fixed.put(cb, 50, 30)
	
        self.fixed.put(self.label, 10, 10)
	#fixed.put(self.textview, 70, 150)

        self.show_all()
	self.label.show()
	self.fixed.show()
        self.add(self.fixed)

def main():
	gtk.main()
	return 0
	
if __name__ == "__main__":
    PyApp()
    main()
