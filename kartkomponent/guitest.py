# -*- coding: utf-8 -*-
import gtk
import hildon
import gobject
import gui_map
import rapport
import pango
import meddelande
import uppdrag
import detringer
import battery
import thread
#import time
from time import *
import osso
import ring
import lager
import inkorg
from databasklient import * 
import login

class Gui(hildon.Program):	
    __map = None
    __map_change_zoom = None
    label = "error"

    def on_key_press(self, widget, event, *args):
        # Zoom -
        if event.keyval == 65361:#65477:
            self.__map_change_zoom("-")
        # Zoom +
        elif event.keyval == 65476:
            self.__map_change_zoom("+")
    #########################TESTING123 skapar alla funktioner############################
    
    def listenBattery(self):
	while(1):
		if(self.online == True):
			statusstring = ' ONLINE'
		if(self.online == False):
			"satter jag label till offline?"
			statusstring = ' OFFLINE'
		self.label.set_text(str(self.batt.getbattery()) + statusstring) 
		sleep(8)
		
    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data
	
    def send(self, widget, data=None):
        print "Hello again - %s wa s pressed" % data
	
    def callback_func(self, interface, method, arguments, user_data):
	
	if(method == 'show_popup'):
		self.show_popup(self)
	if(method == 'online_status'):
		self.online = arguments[0]
	
	
	#Tillbaka
    def tbaka(self,widget,event,data=None):
	self.verktyg.set_active(False)
	self.filer.set_active(False)
	self.kommunikation.set_active(False)
	self.vbox2.hide()
	
    #def ring(self, widget, event, data=None):
	#osso_c = osso.Context("ring", "0.0.1", False)
	#osso_rpc = osso.Rpc(osso_c)
	#print "vi sparar!"
	#osso_rpc.rpc_run("thor.voipproc", "/thor/voipproc", "thor.voipproc", "onlyone", (1, "127.0.0.1", 4000, 4001))	
	
	#Kommunikation
    def komm(self, widget, event, data=None):
	if widget.get_active():
		self.kommunikation.set_active(True)
		self.verktyg.set_active(False)
		self.filer.set_active(False)
		self.installningar.set_active(False)
		self.vbox2.show()
          	self.text.show()
		self.samtal.show()
		self.video.show()
		self.uppdragsmall.hide()
		self.karta.hide()
		self.uppdrag.hide()
		self.rapport.hide()
		self.lager.hide()
		self.energi.hide()
		self.natverk.hide()
		self.anvanda.hide()
		self.samtala.vbox.hide()	
		self.tillbaka.show()
      	else:
          	self.tbaka(widget, data)		
		
	#Vektyg	
    def verk(self, widget, event, data=None):
	if widget.get_active():
		self.verktyg.set_active(True)
		self.kommunikation.set_active(False)
		self.filer.set_active(False)
		self.installningar.set_active(False)
		self.vbox2.show()
		self.text.hide()
		self.samtal.hide()
		self.video.hide()
		self.uppdragsmall.show()
		self.karta.show()
		self.uppdrag.hide()
		self.rapport.hide()
		self.lager.hide()
		self.energi.hide()
		self.natverk.hide()
		self.anvanda.hide()
		self.samtala.vbox.hide()	
		self.tillbaka.show()
	else:
          	self.tbaka(widget, data)
	    
	#Filer
    def fil(self,widget,event,data=None):
	 if widget.get_active():
		self.filer.set_active(True)
		self.kommunikation.set_active(False)
		self.verktyg.set_active(False)
		self.installningar.set_active(False)
		self.vbox2.show()
		self.text.hide()
		self.samtal.hide()
		self.video.hide()
		self.uppdragsmall.hide()
		self.karta.hide()
		self.uppdrag.show()
		self.rapport.show()
		self.lager.show()
		self.energi.hide()
		self.natverk.hide()
		self.anvanda.hide()
		self.samtala.vbox.hide()
		self.tillbaka.show()
	 else:
          	self.tbaka(widget, data)
		
    def install(self,widget,event,data=None):
	 if widget.get_active():
		self.filer.set_active(True)
		self.kommunikation.set_active(False)
		self.verktyg.set_active(False)
		self.installningar.set_active(False)
		self.vbox2.show()
		self.text.hide()
		self.samtal.hide()
		self.video.hide()
		self.uppdragsmall.hide()
		self.karta.hide()
		self.uppdrag.hide()
		self.rapport.hide()
		self.lager.hide()
		self.energi.show()
		self.natverk.show()
		self.anvanda.show()
		self.samtala.vbox.hide()		
		self.tillbaka.show()			
	 else:
          	self.tbaka(widget, data)
	
	#Text
    def textmedd(self, widget, event, data=None):
	self.kommunikation.set_active(False)
	self.filer.set_active(False)
	self.verktyg.set_active(False)
	self.vbox2.hide()
	self.map.hide()
	self.scrolled_window.hide()
	self.samtala.vbox.hide()
	self._lager.lagerboxen.hide()	
	self.scwindow.hide()
	self.swindow.show()
	
	#Samtal
    def ringa(self,widget,event,data=None):
	self.verktyg.set_active(False)
	self.filer.set_active(False)
	self.kommunikation.set_active(False)
	self._lager.lagerboxen.hide()
	self.map.hide()
	self.samtala.vbox.show()
	self.scwindow.hide()
	self.scroll_window.hide()
        self.scrolled_window.hide()	
	self.swindow.hide()
	self.vbox2.hide()
	
	#Visa Kartan
    def kartan(self, widget, event, data=None):
	self.verktyg.set_active(False)
	self.filer.set_active(False)
	self.kommunikation.set_active(False)
	self._lager.lagerboxen.hide()
	self.map.show()
	self.samtala.vbox.hide()
	self.scwindow.hide()
	self.scroll_window.hide()
        self.scrolled_window.hide()	
	self.swindow.hide()
	self.vbox2.hide()
	
	#Lager
    def lagret(self,widget,event,data=None):
	self.verktyg.set_active(False)
	self.filer.set_active(False)
	self.kommunikation.set_active(False)
	self._lager.lagerboxen.show()
	self.map.hide()
	self.samtala.vbox.hide()
	self.scwindow.hide()
	self.scroll_window.hide()
        self.scrolled_window.hide()	
	self.swindow.hide()
	self.vbox2.hide()
	
	#Uppdrag
    def upp(self, widget, event, data=None):
	self.verktyg.set_active(False)
	self.filer.set_active(False)
	self.kommunikation.set_active(False)
	self._lager.lagerboxen.hide()
	self.map.hide()
	self.samtala.vbox.hide()
	self.scwindow.hide()
	self.scroll_window.show()
        self.scrolled_window.hide()	
	self.swindow.hide()
	self.vbox2.hide()
	
	#Rapport
    def rapp(self, widget, event, data=None):
	self.verktyg.set_active(False)
	self.filer.set_active(False)
	self.kommunikation.set_active(False)
	self._lager.lagerboxen.hide()
	self.map.hide()
	self.samtala.vbox.hide()
	self.scwindow.hide()
	self.scroll_window.hide()
        self.scrolled_window.show()	
	self.swindow.hide()
	self.vbox2.hide()
		
	#Inbox	
    def inboxen(self, widget, event, data=None):
	self.inbox.update_messages()
	self.verktyg.set_active(False)
	self.filer.set_active(False)
	self.kommunikation.set_active(False)
	self._lager.lagerboxen.hide()
	self.map.hide()
	self.samtala.vbox.hide()
	self.scroll_window.hide()
        self.scrolled_window.hide()	
	self.swindow.hide()
	self.vbox2.hide()
	self.scwindow.show()
	
        #Avsluta programmet
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False
    
    #def batteriniva(self
##############################Har skapat alla funktioner####################################

    def oldbuttonsandwindows(self):
	#Skapa en Vbox som sedan ska in i Hboxen och innehallar huvudknapparna i menyn
        self.vbox = gtk.VBox(False, 0)
	self.vbox.set_size_request(198, 95)
        self.vbox.show()
	
	#Skapa en stor Hbox
	self.hbox = gtk.HBox(False, 0)
  	self.hbox.show()
	self.hbox.pack_start(self.vbox, False, False, 0)

	#Knappar stor meny
        # Kommunikation
        self.kommunikation = gtk.ToggleButton("Kommunikation")
        self.kommunikation.connect("toggled", self.komm, "Kommunikation")
        self.kommunikation.show()
        self.vbox.pack_start(self.kommunikation, True, True, 0)

        # Verktyg
        self.verktyg = gtk.ToggleButton("Verktyg")
        self.verktyg.connect("toggled", self.verk, "Verktyg")
        self.verktyg.show()
	self.vbox.pack_start(self.verktyg, True, True, 0)

    	# Filer
        self.filer= gtk.ToggleButton("Filer")
        self.filer.connect("toggled", self.fil, "Filer")
	self.filer.show()
        self.vbox.pack_start(self.filer, True, True, 0)

        # Inst�llningar
        self.installningar= gtk.ToggleButton("Installningar")
        self.installningar.connect("toggled", self.install, "Installningar")
	self.installningar.show()
	self.vbox.pack_start(self.installningar, True, True,0)

	#Knappar i undermenyer
	#Knappar under kommunikation
	#i en vbox
        self.vbox2 = gtk.VBox(True, 0)
	self.vbox2.set_size_request(198, 95)
	
	# Textmeddelande
	self.text = gtk.Button("Textmeddelande")
        self.text.connect("clicked", self.textmedd, "Textmeddelande")
	self.vbox2.pack_start(self.text, True, True, 0)

	
	# Samtal
	self.samtal = gtk.Button("Samtal")
        self.samtal.connect("clicked", self.ringa, "Samtal")
	self.vbox2.pack_start(self.samtal, True, True, 0)
	
	# Video
	self.video = gtk.Button("Inkorg")
        self.video.connect("clicked", self.inboxen, "Inkorg")
	self.vbox2.pack_start(self.video, True, True, 0)
	
	# Tillbaka
	self.tillbaka = gtk.Button("Tillbaka")
        self.tillbaka.connect("clicked", self.tbaka, "Tillbaka")
	self.vbox2.pack_start(self.tillbaka, True, True, 0)
	
	#Knappar i verktygsmeny
	#Uppdragsmall
	self.uppdragsmall = gtk.Button("   Uppdragsmall  ")
	self.uppdragsmall.connect("clicked", self.callback, "Uppdragsmall")
	self.vbox2.pack_start(self.uppdragsmall, True, True,0)
	
	#Karta
	self.karta = gtk.Button("Karta")
	self.karta.connect("clicked", self.kartan, "Karta")
	self.vbox2.pack_start(self.karta, True, True,0)
	
	#Knappar i filmenyn
	#Uppdrag
	self.uppdrag = gtk.Button("       Uppdrag      ")
	self.uppdrag.connect("clicked", self.upp, "Uppdrag")
	self.vbox2.pack_start(self.uppdrag, True, True,0)
	
	#Rapport
	self.rapport = gtk.Button("Rapport")
	self.rapport.connect("clicked", self.rapp, "Rapport")
	self.vbox2.pack_start(self.rapport, True, True,0)
	
	#Lager
	self.lager = gtk.Button("Lager")
	self.lager.connect("clicked", self.lagret, "Lager")
	self.vbox2.pack_start(self.lager, True, True,0)
	
	#Enerigisparl�ge
	self.energi = gtk.Button("Energi")
	self.energi.connect("clicked", self.callback, "Energi")
	self.vbox2.pack_start(self.energi, True, True,0)
	
	#Natverksinstallningar
	self.natverk = gtk.Button("Natverk")
	self.natverk.connect("clicked", self.callback, "Natverk")
	self.vbox2.pack_start(self.natverk, True, True,0)
	
	#Anvandarinstallningar
	self.anvanda = gtk.Button("Logga in")
	self.anvanda.connect("clicked", self.show_popup)
	self.vbox2.pack_start(self.anvanda, True, True,0)
	
	# Tillbaka
	self.tillbaka = gtk.Button("Tillbaka")
        self.tillbaka.connect("clicked", self.tbaka, "Tillbaka")
	self.vbox2.pack_start(self.tillbaka, True, True, 0)
	self.hbox.pack_start(self.vbox2, False, False, 0)
	self.tbaka("clicked", "hej")
	
	self.rapportera = rapport.Mall()
	self.meddela = meddelande.Meddelande()
	self.uppdraget = uppdrag.Uppdrag()
	self.ringa = detringer.Ring()
	self.samtala = ring.Samtal()
	self._lager = lager.Lager()
	self.inbox = inkorg.Inkorg()

	self.vbox3 = gtk.VBox(False, 0)
        self.vbox3.show()
	
	self.scrolled_window=gtk.ScrolledWindow()
	self.scrolled_window.set_border_width(10)
	self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
	
	self.scroll_window=gtk.ScrolledWindow()
	self.scroll_window.set_border_width(10)
	self.scroll_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
	
	self.swindow=gtk.ScrolledWindow()
	self.swindow.set_border_width(10)
	self.swindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
	
	self.scwindow=gtk.ScrolledWindow()
	self.scwindow.set_border_width(10)
	self.scwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        self.label.show()	
        self.vbox3.pack_start(self.label, False, False, 0)
  
	#Packning
	self.scrolled_window.add_with_viewport(self.rapportera.vbox4)	
	self.scroll_window.add_with_viewport(self.uppdraget.vbox4)
	self.swindow.add_with_viewport(self.meddela.vbox)
	self.scwindow.add_with_viewport(self.inbox.vbox)
	self.vbox3.pack_start(self.samtala.vbox,False,False,0)
	self.vbox3.pack_start(self.ringa.vbox,False,False,0)
	self.vbox3.pack_start(self.map,True,True,0)
	self.vbox3.pack_start(self.scrolled_window, True, True, 0)
	self.vbox3.pack_start(self.scroll_window,True,True,0)
	self.vbox3.pack_start(self.swindow,True,True,0)	
	self.vbox3.pack_start(self.scwindow,True,True,0)		
	self.vbox3.pack_start(self._lager.lagerboxen,True,True,0)
	self.hbox.pack_start(self.vbox3, True, True, 0)
    	self.hbox.show()
	self.window.add(self.hbox)
	self.window.show()


    def __init__(self, map):
	gobject.threads_init()
	self.show_popup(self)
	self.osso_c = osso.Context("guitest", "0.0.1", False)
	self.osso_rpc = osso.Rpc(self.osso_c)
	self.osso_rpc.set_rpc_callback("thor.guitest","/thor/guitest","thor.guitest",self.callback_func)
	self.label = gtk.Label()
	self.batt = battery.Batteri()
	self.online = False
	#thread.start_new_thread(self.batt.run,())
	thread.start_new_thread(self.listenBattery,())
        # Initierar hildon (GUI-biblioteket för N810)
        hildon.Program.__init__(self)
        # Sparar handdatorns karta.
        self.__map = map
	# Skapar programmets fönster
        self.window = hildon.Window()
        # Någon storlek så att PyGTK inte klagar
        self.window.set_size_request(800, 400)
        # Funktion som körs när prorammet ska stängas av
        #self.window.connect("destroy", self.menu_exit)
        self.add_window(self.window)
	
	self.create_map_view()	
	self.oldbuttonsandwindows()

	

        # Möjliggör fullscreen-läge
        #self.window.connect("key-press-event", self.on_key_press)
        #self.window.connect("window-state-event", self.on_window_state_change)
        # Programmet är inte i fullscreen-läge från början.
        #self.window_in_fullscreen = False

        # Skapar en notebook-komponent i vilken vi har olika sidor som fungerar
        # som vyer. En sida är för kartvyn, en sida för uppdragsvyn osv.
        # Mer om hur Notebook fungerar står här:
        # http://www.pygtk.org/pygtk2tutorial/sec-Notebooks.html
        
        #self.create_settings_view()

        # Lägger in vyn i fönstret
        #self.window.add(self.view)

        # Skapar menyn
        #self.window.set_menu(self.create_menu())

    # Skapar vyn för kartan
    def create_map_view(self):
        self.map = gui_map.Map(self.__map)
        self.__map_change_zoom = self.map.change_zoom
	
    

    def get_treeview(self, args):
        if len(args) == 1:
            return args[0]
        else:
            return args[2]

    def get_row_number_from_treeview(self, treeview):
        row = treeview.get_selection().get_selected_rows()
        return row[1][0][0]

    # Denna funktion har skapats eftersom det är aningen omständigt att få ut
    # värden från en markering i en lista. Skicka in listan och kolumnen du
    # vill ha ut värdet ifrån så sköter funktionen resten. Första kolumnen är 0,
    # andra 1 osv. 
    def get_value_from_treeview(self, treeview, column):
        # Läs mer om vad row innehåller här (gtk.TreeSelection.get_selected_row):
        # http://www.pygtk.org/pygtk2reference/class-gtktreeselection.html
        row = treeview.get_selection().get_selected_rows()
      
        if len(row[1]) > 0:
            # row innehåller en tuple med (ListStore(s), path(s))
            # Vi plockar ut första värdet i paths. Eftersom vi enbart tillåter
            # användaren att markera en rad i taget kommer det alltid bara finnas
            # ett värde i paths.
            path = row[1][0]
          
            # Hämtar modellen för treeview
            treemodel = treeview.get_model()
          
            # Returnerar värdet
            return treemodel.get_value(treemodel.get_iter(path), column)
        else:
            return None
	
    def show_popup(self, event):
	logg = login.Inlogg()
        #popup = gtk.Window()
        #popup.set_title( "Login" )
	#popup.set_size_request(500,500)
        #popup.add(logg.vbox)
	##adress.vbox.show()	
        #popup.set_modal(True)
        ##popup.set_transient_for(self)
        #popup.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_DIALOG )
        #popup.connect( "destroy", lambda *w: gtk.main_quit() )
        logg.popup.show()


    def run(self):
        #self.window.show_all()
        gtk.main()
