import gtk
from databasklient import *
import visameddelande


class Inkorg(gtk.Window): 

    def callback(self, widget, data=None):
	print "Inkorg - %s was pressed" % data

    def __init__(self):
	    
	self.one = ""
	self.two = None
	self.three = None
	self.args = {}
	
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
        store = self.create_model()

        treeView = gtk.TreeView(store)
        treeView.connect("row-activated", self.on_activated)
        treeView.set_rules_hint(True)
        scrolled_window.add(treeView)
	treeView.show()
	
        self.create_columns(treeView)
        self.statusbar = gtk.Statusbar()
	self.statusbar.show()
	
	
	button = gtk.Button("Klar")
	button.set_size_request(70,30)
	button.connect("clicked", self.show_popup)
	self.vbox.pack_start(button, False, False, 0)
	button.show()
        self.vbox.pack_start(self.statusbar, False, False, 0)
        self.vbox.show_all()
	
    def get_messages(self):
	self.anvandare = []
	for n in getAllMessages():
		self.anvandare.append((n.sender, n.receiver, n.type , n.time_created, n.content , n. response_to))
		
	return self.anvandare

    def create_model(self):
        store = gtk.ListStore(str, str, str, str, str, str)
	anvandare = self.get_messages()
        for act in anvandare:
            store.append([act[0], act[1], act[2], act[3], act[4], act[5]])
        return store

    def create_columns(self, treeView):
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
	
    def on_activated(self, widget, row, col):
        model = widget.get_model()
        text = model[row][0] + ", " + model[row][2]+ ", " + model[row][4]
        self.statusbar.push(0, text)
	self.one = model[row][0]
	self.two = model[row][2]
	self.three = model[row][4]
	print self.one
	print self.two
	print self.three
	print model
	self.args = {"sender":self.one,"subject":self.two,"content":self.three}
	
	print self.args["subject"]

    def show_popup(self, button):
	print self.args["sender"]
	visa = visameddelande.VisaMeddelande(self.args)
        self.popup = gtk.Window()
        self.popup.set_title( "Meddelande" )
	self.popup.set_size_request(500,500)
        self.popup.add(visa.vbox)
	self.avsluta.connect("clicked", self.avs, "Avsluta")
        self.popup.set_modal(False)
        self.popup.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_DIALOG )
        self.popup.connect( "destroy", lambda *w: gtk.main_quit() )
        self.popup.show()

    def avs(self, widget, event, data=None):
	self.popup.destroy()

	
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    Inkorg()
    main()