#!/usr/bin/python

import gtk
from databasklient import *

m = getMessage(1)
n = getMessage(2)
#m=m
#n=n
print m.sender
print n.sender
anvandare = [(m.sender, m.reciver, m.type , m.time_created, m.content , m. response_to), (n.sender, n.reciver, n.type , n.time_created, n.content , n. response_to), ('Christoffer', '66.249.65.85 ', 'offline', 'online', '66.249.65.81 ', 'offline'), ('Thor', '66.249.65.90 ', 'offline', 'online', '66.249.65.81 ', 'offline'), ('Niklas', '66.249.65.88 ', 'online', 'online', '66.249.65.81 ', 'offline'),('Mathias', '66.249.65.00 ', 'online', 'online', '66.249.65.81 ', 'offline')]

#('mathias1','hanna','text',"change",'jason.dums() sak ska vara har tex Unit', 1)
class Inkorg(gtk.Window): 

    def callback(self, widget, data=None):
	print "Inkorg - %s was pressed" % data

    def __init__(self):
	print "kor"
        #super(Inkorg, self).__init__()
        
        #self.set_size_request(350, 250)
        #self.set_position(gtk.WIN_POS_CENTER)
        
        #self.connect("destroy", gtk.main_quit)
        #self.set_title("Inkorg")
	#self.show()

        self.vbox = gtk.VBox(False, 0)
	self.vbox.show()
	
	hbox = gtk.HBox(True,0)
	self.vbox.pack_start(hbox, False, False, 0)
	hbox.show()

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	scrolled_window.show()
        
        self.vbox.pack_start(scrolled_window, True, True, 0)
	#hbox.pack_start(scrolled_window, True, True,0)

        store = self.create_model()

        treeView = gtk.TreeView(store)
        treeView.connect("row-activated", self.on_activated)
        treeView.set_rules_hint(True)
        scrolled_window.add(treeView)
	treeView.show()
	
        self.create_columns(treeView)
	#self.create_columns.show()
        self.statusbar = gtk.Statusbar()
	self.statusbar.show()
	
	#button1 = create_arrow_button(gtk.ARROW_UP, gtk.SHADOW_IN)
	#hbox.pack_start(button1, False, False, 3)
   	
   	#button1 = create_arrow_button(gtk.ARROW_DOWN, gtk.SHADOW_OUT)
   	#hbox.pack_start(button1, False, False, 3)
	#hbox.show()

	
	button = gtk.Button("Klar")
	button.set_size_request(70,30)
	button.connect("clicked", self.callback, "Klar")
	#button.add(hbox)
	self.vbox.pack_start(button, False, False, 0)
	button.show()
	
        self.vbox.pack_start(self.statusbar, False, False, 0)
	print "slut"

        #self.add(self.vbox)
	##self.add(hbox)
        self.vbox.show_all()


    def create_model(self):
        store = gtk.ListStore(str, str, str, str, str, str)
	print "create_model"

        for act in anvandare:
            store.append([act[0], act[1], act[2], act[3], act[4], act[5]])
        return store
	

    def create_columns(self, treeView):
	print "create_columns"
	
    	#
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Sender", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Reciver", rendererText, text=1)
        column.set_sort_column_id(1)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Type", rendererText, text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)
	
	rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Time", rendererText, text=3)
        column.set_sort_column_id(3)
        treeView.append_column(column)
	
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Content", rendererText, text=4)
        column.set_sort_column_id(4)
        treeView.append_column(column)
	
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Response", rendererText, text=5)
        column.set_sort_column_id(5)
        treeView.append_column(column)
	
	#Toggle Check
	rendererCheck = gtk.CellRendererToggle()
	rendererCheck.set_property('activatable', True)
	#rendererCheck.connect('toggled', self.rendererText, treeView )
	
	column = gtk.TreeViewColumn("Check", rendererCheck)
	column.add_attribute(rendererCheck, "active",6)
	column.set_sort_column_id(6)
	treeView.append_column(column)
	
    #def desc_edited(self, caller, path, new_text, treeView):
	#model[path][0] = new_text
	#DEBUG("Desc %s changed to %s"%(path,new_text))
	
    #def desc_toggled(self, caller, path, treeView):
		#model[path][6] = not model[path][6]
		#DEBUG("Done %s changed to %s"%(path, model[path][6]))

	

    def on_activated(self, widget, row, col):
	print "on_activated"
        
        model = widget.get_model()
        text = model[row][0] + ", " + model[row][1] + ", " + model[row][2] + ", " + model[row][3] + "," + model[row][4] + ", " + model[row][5] 
        self.statusbar.push(0, text)
	
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    Inkorg()
    main()