#!/usr/bin/python

# ZetCode PyGTK tutorial 
#
# This example shows a TreeView widget
# in a list view mode
#
# author: jan bodnar
# website: zetcode.com 
# last edited: February 2009


import gtk

anvandare = [('Manuela', '66.249.65.81 ', 'offline'), ('Hanna', '66.249.65.83 ', 'online'),
    ('KJ', '66.249.65.91 ', 'online'), ('Christoffer', '66.249.65.85 ', 'offline'),
    ('Thor', '66.249.65.90 ', 'offline'), ('Niklas', '66.249.65.88 ', 'online'),('Mathias', '66.249.65.00 ', 'online')]


class Adresslista(gtk.Window): 

    def klarlyssnare(self, widget, data=None):
	print "Adresslista - %s was pressed" % data
	self.popup.destroy()
	
    def __init__(self):
        #super(Adresslista, self).__init__()
        
        #self.set_size_request(350, 250)
        #self.set_position(gtk.WIN_POS_CENTER)
      
        #self.connect("destroy", gtk.main_quit)
        #self.set_title("Adresslista")

        self.vbox = gtk.VBox(False, 0)
	self.vbox.show()
	
	hbox = gtk.HBox(True,0)
	self.vbox.pack_start(hbox, False, False, 0)
	hbox.show()

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.vbox.pack_start(scrolled_window, True, True, 0)
	#hbox.pack_start(scrolled_window, True, True,0)

        store = self.create_model()

        treeView = gtk.TreeView(store)
        treeView.connect("row-activated", self.on_activated)
        treeView.set_rules_hint(True)
        scrolled_window.add(treeView)

        self.create_columns(treeView)
        self.statusbar = gtk.Statusbar()
	
	button = gtk.Button("Klar")
	button.set_size_request(70,30)
	button.connect("clicked", self.klarlyssnare, "Klar")
	#button.add(hbox)
	self.vbox.pack_start(button, False, False, 0)
	hbox.show()
	button.show()
	
	self.avsluta = gtk.Button("Avsluta")
        self.avsluta.connect("clicked", self.avs, "Avsluta")
	self.avsluta.show()
	self.vbox.pack_start(self.avsluta,True,True,0)
	
        self.vbox.pack_start(self.statusbar, False, False, 0)

	self.popup = gtk.Window()
        self.popup.set_title( "Adresslista" )
	self.popup.set_size_request(500,500)
        self.popup.add(self.vbox)
        self.popup.set_modal(False)
        self.popup.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_DIALOG )
        #self.add(vbox)
	#self.add(hbox)
        self.vbox.show_all()

    def avs(self, widget, event, data=None):
	    self.popup.destroy()

    def create_model(self):
        store = gtk.ListStore(str, str, str)

        for act in anvandare:
            store.append([act[0], act[1], act[2]])
        return store
	

    def create_columns(self, treeView):
	
    	#
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Namn", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("IP", rendererText, text=1)
        column.set_sort_column_id(1)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Status", rendererText, text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)
	
	#Toggle Check
	rendererCheck = gtk.CellRendererToggle()
	rendererCheck.set_property('activatable', True)
	#rendererCheck.connect('toggled', self.desc_toggled, treeView )
	
	column = gtk.TreeViewColumn("Check", rendererCheck)
	column.add_attribute(rendererCheck, "active",3)
	column.set_sort_column_id(3)
	treeView.append_column(column)
	
    #def desc_edited(self, caller, path, new_text, treeView):
	#model[path][0] = new_text
	#DEBUG("Desc %s changed to %s"%(path,new_text))
	
    #def desc_toggled(self, caller, path, treeView):
		#model[path][3] = not model[path][3]
		#DEBUG("Done %s changed to %s"%(path, model[path][3]))

    def on_activated(self, widget, row, col):
        
        model = widget.get_model()
        text = model[row][0] + ", " + model[row][1] + ", " + model[row][2] + ", " +model[row][3]
        self.statusbar.push(0, text)

def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    Adresslista()
    main()