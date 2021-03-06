import gtk
import simplejson as json
import osso
from databasmethod import *

class Inlogg():
    
    USER = ""
    osso_c = osso.Context("login", "0.0.1", False)
    osso_rpc = osso.Rpc(osso_c)
    
    def send(self, widget, event, data=None):
	global USER
	anvandare = self.entry.get_text()
	losen = self.entry1.get_text()
	USER = anvandare
	dict = {"id": 1, "sender": anvandare , "receiver": "" ,"type": 'login' , "subtype": "", "time_created": 34, 'content' : {'subject' : '', 'message' : losen}, 'response_to' : ''}
	self.args = (json.dumps(dict),)
    
    def release(self, widget, event, data=None):
	self.osso_rpc.rpc_run("thor.client", "/thor/client", "thor.client", "sendfunction", self.args)
	#idstr = ""
	#print getAllMessageID()
	#for item in getAllMessageID():
		#idstr += " " + str(item)
	#print idstr
	#self.args = ('/sync' + idstr,)
	#print self.args
	#self.osso_rpc.rpc_run("thor.client", "/thor/client", "thor.client", "sendfunction", self.args)
        self.popup.destroy()
	
    def __init__(self):

	#window = gtk.Window()
	#window.connect("delete_event", self.delete_event)
	#window.connect("destroy", self.destroy
	
	#Vbox for innehall
	self.vbox = gtk.VBox(False,5)
	self.vbox.set_border_width(50)	
	
	self.hbox = gtk.HBox(False,35)
	
	#Skriv in en anvandare
        self.anvandare = gtk.Label("Anvandarnamn")
        self.anvandare.set_alignment(0, 0)
	self.anvandare.show()
	self.vbox.pack_start(self.anvandare, False, False, 0)
	
	self.entry = gtk.Entry()
        #self.entry.set_max_length(250)
	self.entry.show()	
	self.vbox.pack_start(self.entry, False, False, 0)
	
	#Skriv in ditt losen
        self.losen = gtk.Label("Losenord")
        self.losen.set_alignment(0, 0)
	self.losen.show()
	self.vbox.pack_start(self.losen, False, False, 0)
	
	self.entry1 = gtk.Entry()
        #self.entry1.set_max_length(250)
	self.entry1.show()	
	self.vbox.pack_start(self.entry1, False, False, 0)
	
	self.loggin = gtk.Button("Logga in")
        self.loggin.connect("clicked", self.send, "Logga in")
	self.loggin.connect("released", self.release, "Skicka") 
	self.loggin.set_size_request(130,50)
	self.loggin.show()
	self.hbox.pack_start(self.loggin,False,False,2)
	
	self.avsluta = gtk.Button("Avsluta")
        self.avsluta.connect("clicked", self.avs, "Avsluta")
	self.avsluta.set_size_request(130,50)
	self.avsluta.show()
	self.hbox.pack_start(self.avsluta,False,False,0)
	self.vbox.pack_start(self.hbox,False,False,20)
	self.hbox.show()
	
	#popup fran login
	self.popup = gtk.Window()
        self.popup.set_title( "Login" )
	self.popup.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("lightgray"))
	self.popup.set_size_request(400,300)
        self.popup.add(self.vbox)
	#adress.vbox.show()	
        self.popup.set_modal(True)
        #popup.set_transient_for(self)
        self.popup.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_DIALOG )
	
	
	self.vbox.show()
	#window.add(self.vbox)
	#window.show()
    
    def avs(self, widget, event, data=None):
	self.popup.destroy()

    def get_user(self):
    	global USER
	return USER
	
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    Inlogg()
    main()