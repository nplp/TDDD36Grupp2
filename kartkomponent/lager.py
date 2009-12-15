from databasklient import *
import gtk
import visameddelande
from login import *

class Lager():
	
    def callback(self, widget, data=None):
	print "Inkorg - %s was pressed" % data

    def __init__(self):
	    
	self.one = ""
	self.two = None
	self.three = None
	self.four = None
	self.args = {}
	self.temp = get_item_all()
	
	self.osso_c = osso.Context("lager", "0.0.1", False)
	self.osso_rpc = osso.Rpc(self.osso_c)
    
        self.lagerboxen = gtk.VBox(False, 0)
	self.lagerboxen.show()
	
	hbox = gtk.HBox(True,0)
	self.lagerboxen.pack_start(hbox, False, False, 0)
	hbox.show()

        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	self.scrolled_window.show()
        
        self.lagerboxen.pack_start(self.scrolled_window, True, True, 0)
        store = self.create_model()

        self.treeView = gtk.TreeView(store)
        self.treeView.connect("row-activated", self.on_activated)
        self.treeView.set_rules_hint(True)
        self.scrolled_window.add(self.treeView)
	self.treeView.show()
	
        self.create_columns(self.treeView)
        self.statusbar = gtk.Statusbar()
	self.statusbar.show()
	
	
	#button = gtk.Button("Oppna")
	#button.set_size_request(70,30)
	#button.connect("clicked", self.show_popup)
	#self.vbox.pack_start(button, False, False, 0)
	#button.show()
        self.lagerboxen.pack_start(self.statusbar, False, False, 0)
        self.lagerboxen.show_all()
	
	
    def update_messages(self):
	store = self.create_model()
	self.treeView.set_model(store)
	
		
    ##Tar in en lista med meddelanden, returnerar den som e filtrerad pa anvandare, EJ implementerad (tenkt som skydd mot flera pa 1 enhet)
    #def filter_messages(self, unfiltered_list):
	    #filtered_list = []
	    #print "HAR KOMMET DET; BANG!"
	    #l = Inlogg()
	    #for item in unfiltered_list:
		    #if(item[0] == 'niklas'):
			    #print item[0]#filtered_list.append(item[0])
    	    #print "KLARTKLARTKLARTKLART"


	    
    def get_messages(self):
	self.meddelanden = []
	
	for n in self.temp:
		self.meddelanden.append((n.item_id, n.name, n.count, n.location))
	#for n in getAllMessages():
		#self.meddelanden.append((n.sender, n.receiver, n.type, n.subtype, n.time_created, n.subject, n.message , n.response_to))
		
	
	
	#self.filter_messages(self.meddelanden)
	return self.meddelanden

    def create_model(self):
	#idstr = ""
	#print getAllMessageID()
	#for item in getAllMessageID():
		#idstr += " " + str(item)
	#print idstr
	#self.argsy = ('/sync' + idstr,)
	#print self.argsy
	#self.osso_rpc.rpc_run("thor.client", "/thor/client", "thor.client", "sendfunction", self.argsy)
	
        store = gtk.ListStore(str, str, str, str)
	meddelanden = self.get_messages()
        for act in meddelanden:
            store.append((act[0], act[1], act[2], act[3]))
        return store

    def create_columns(self, treeView):
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("ItemID", rendererText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Name", rendererText, text=1)
        column.set_sort_column_id(1)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Count", rendererText, text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)
	
	rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Location", rendererText, text=3)
        column.set_sort_column_id(3)
        treeView.append_column(column)
	

    def on_activated(self, widget, row, col):
        model = widget.get_model()
        text = model[row][1]+ ", " + model[row][2]+ ", " + model[row][3]
        self.statusbar.push(0, text)
	self.one = model[row][0]
	self.two = model[row][1]
	self.three = model[row][2]
	self.four = model[row][3]
	print self.one
	print self.two
	print self.three
	print self.four
	print model
	self.args = {"item_id":self.one,"name":self.two,"count":self.three,"location":self.four}

	print self.args["name"]

    #def show_popup(self, button):
	#visa = visameddelande.VisaMeddelande(self.args)
        #visa.popup.show()

	
def main():
	gtk.main()
	return 0
	
if __name__ == "__main__":
    Lager()
    main()
