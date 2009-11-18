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

class Gui(hildon.Program):
    __map = None
    __map_change_zoom = None

    def on_key_press(self, widget, event, *args):
        # Zoom -
        if event.keyval == 65361:#65477:
            self.__map_change_zoom("-")
        # Zoom +
        elif event.keyval == 65476:
            self.__map_change_zoom("+")
    #########################TESTING123 skapar alla funktioner############################
    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data
	
    def send(self, widget, data=None):
        print "Hello again - %s was pressed" % data
	
	
	#Tillbaka
    def tbaka(self,widget,event,data=None):
	self.verktyg.set_active(False)
	self.filer.set_active(False)
	self.kommunikation.set_active(False)
	self.vbox2.hide()
	
    def ring(self, widget, event, data=None):
	self.ringa.vbox.show()
	self.label.hide()
	
	#Uppdrag
    def upp(self, widget, event, data=None):
	self.kommunikation.set_active(False)
	self.filer.set_active(False)
	self.verktyg.set_active(False)
	self.vbox2.hide()
	self.map.hide()
	self.meddela.vbox.hide()
        self.scrolled_window.hide()
        self.scroll_window.show()
	
	#Rapport
    def rapp(self, widget, event, data=None):
	self.kommunikation.set_active(False)
	self.filer.set_active(False)
	self.verktyg.set_active(False)
	self.vbox2.hide()
	self.map.hide()
	self.meddela.vbox.hide()
	self.scroll_window.hide()
	self.ringa.vbox.hide()
        self.scrolled_window.show()	
	
	
	#Kommunikation
    def komm(self, widget, event, data=None):
	if widget.get_active():
		self.kommunikation.set_active(True)
		self.verktyg.set_active(False)
		self.filer.set_active(False)
		self.vbox2.show()
          	self.text.show()
		self.samtal.show()
		self.video.show()
		self.uppdragsmall.hide()
		self.karta.hide()
		self.uppdrag.hide()
		self.rapport.hide()
		self.lager.hide()
		self.tillbaka.show()
      	else:
          	self.tbaka(widget, data)		
		
	#Vektyg	
    def verk(self, widget, event, data=None):
	if widget.get_active():
		self.verktyg.set_active(True)
		self.kommunikation.set_active(False)
		self.filer.set_active(False)
		self.vbox2.show()
		self.text.hide()
		self.samtal.hide()
		self.video.hide()
		self.uppdragsmall.show()
		self.karta.show()
		self.uppdrag.hide()
		self.rapport.hide()
		self.lager.hide()
		self.tillbaka.show()
	else:
          	self.tbaka(widget, data)
	    
	#Filer
    def fil(self,widget,event,data=None):
	 if widget.get_active():
		self.filer.set_active(True)
		self.kommunikation.set_active(False)
		self.verktyg.set_active(False)
		self.vbox2.show()
		self.text.hide()
		self.samtal.hide()
		self.video.hide()
		self.uppdragsmall.hide()
		self.karta.hide()
		self.uppdrag.show()
		self.rapport.show()
		self.lager.show()
		self.tillbaka.show()
	 else:
          	self.tbaka(widget, data)
	
	#Visa kartan
    def kartan(self, widget, event, data=None):
	self.verktyg.set_active(False)
	self.vbox2.hide()
	self.scrolled_window.hide()
	self.meddela.vbox.hide()
	self.ringa.vbox.hide()
        self.scroll_window.hide()
	self.map.show()
	 
    def textmedd(self, widget, event, data=None):
	self.kommunikation.set_active(False)
	self.filer.set_active(False)
	self.verktyg.set_active(False)
	self.vbox2.hide()
	self.map.hide()
	self.scrolled_window.hide()	
	self.meddela.vbox.show()
	self.ringa.vbox.hide()	
	
        #Avsluta programmet
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False
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

        # Avslutaknapp
        self.avsluta= gtk.Button("Avsluta")
        self.avsluta.connect("clicked", lambda w: gtk.main_quit())
	self.avsluta.show()
	self.vbox.pack_start(self.avsluta, True, True,0)

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
        self.samtal.connect("clicked", self.ring, "Samtal")
	self.vbox2.pack_start(self.samtal, True, True, 0)
	
	# Video
	self.video = gtk.Button("Video")
        self.video.connect("clicked", self.callback, "Video")
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
	
	# Tillbaka
	self.tillbaka = gtk.Button("Tillbaka")
        self.tillbaka.connect("clicked", self.tbaka, "Tillbaka")
	self.vbox2.pack_start(self.tillbaka, True, True, 0)
	
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
	self.lager.connect("clicked", self.callback, "Lager")
	self.vbox2.pack_start(self.lager, True, True,0)
	
	# Tillbaka
	self.tillbaka = gtk.Button("Tillbaka")
        self.tillbaka.connect("clicked", self.tbaka, "Tillbaka")
	self.vbox2.pack_start(self.tillbaka, True, True, 0)
	self.hbox.pack_start(self.vbox2, False, False, 0)
	self.tbaka("clicked", "hej")

	#self.startakarta = tupeltest.StartMap()
	self.rapportera = rapport.Mall()
	self.meddela = meddelande.Meddelande()
	self.uppdraget = uppdrag.Uppdrag()
	self.ringa = detringer.Ring()
	
	self.vbox3 = gtk.VBox(False, 0)
        self.vbox3.show()
	
	self.scrolled_window=gtk.ScrolledWindow()
	self.scrolled_window.set_border_width(10)
	self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
	
	self.scroll_window=gtk.ScrolledWindow()
	self.scroll_window.set_border_width(10)
	self.scroll_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)	
		
		
	#create a new label.
        self.label = gtk.Label("Anvandare	symbol	datum tid")
        self.label.set_alignment(0, 0)
        self.label.show()	
        self.vbox3.pack_start(self.label, False, False, 0)
	
	#Packning
	self.scrolled_window.add_with_viewport(self.rapportera.vbox4)	
	self.scroll_window.add_with_viewport(self.uppdraget.vbox4)
	self.vbox3.pack_start(self.ringa.vbox,False,False,0)
	self.vbox3.pack_start(self.map,True,True,0)
	self.vbox3.pack_start(self.scrolled_window, True, True, 0)
	self.vbox3.pack_start(self.scroll_window,True,True,0)
	self.vbox3.pack_start(self.meddela.vbox,True,True,0)
	self.hbox.pack_start(self.vbox3, True, True, 0)
    	self.hbox.show()
	self.window.add(self.hbox)
	self.window.show()


    def __init__(self, map):
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


    def run(self):
        #self.window.show_all()
        gtk.main()
