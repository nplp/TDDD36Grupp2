#!/usr/bin/env python

# example table.py

import pygtk
pygtk.require('2.0')
import gtk

class Table:
    # Our callback.
    # The data passed to this method is printed to stdout
    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data

    # This callback quits the program
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # Set the window title
        self.window.set_title("Hannas!")

        # Set a handler for delete_event that immediately
        # exits GTK.
        self.window.connect("delete_event", self.delete_event)

        # Sets the border width of the window.
        self.window.set_border_width(20)

        # Create a 2x2 table
        table = gtk.Table(3, 4, True)

        # Put the table in the main window
        self.window.add(table)

        # Kommunikation
        button = gtk.Button("Kommunikation")
        button.connect("clicked", self.callback, "Kommunikation")
        table.attach(button, 0, 1, 0, 1)
        button.show()

        # Verktyg
        button = gtk.Button("Verktyg")
        button.connect("clicked", self.callback, "Verktyg")
        table.attach(button, 0, 1, 1, 2)
        button.show()
	
	# Filer
        button = gtk.Button("Filer")
        button.connect("clicked", self.callback, "Filer")
        table.attach(button, 0, 1, 2, 3)
        button.show()

	# Arbetsyta
        button = gtk.Button("Arbetsyta")
        button.connect("clicked", self.callback, "Arbetsyta")
        table.attach(button, 1, 4, 0, 4)
        button.show()

        # Create "Quit" button
        button = gtk.Button("Quit")

        # When the button is clicked, we call the main_quit function
        # and the program exits
        button.connect("clicked", lambda w: gtk.main_quit())

        # Insert the quit button into the both lower quadrants of the table
        table.attach(button, 0, 1, 3, 4)
        button.show()
        table.show()
        self.window.show()

def main():
    gtk.main()
    return 0       

if __name__ == "__main__":
    Table()
    main()
