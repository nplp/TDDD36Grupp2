# -*- coding: utf-8 -*-
import gtk
import math
import time
import simplejson as json
import osso
import data_storage
import thread
import gobject
from databasklient import*

class Map(gtk.DrawingArea):
    __bounds = {"min_latitude":0,
                "max_latitude":0,
                "min_longitude":0,
                "max_longitude":0}

    def __init__(self, map):
        gtk.DrawingArea.__init__(self)
	gobject.threads_init()        
        # Variabler
        self.__map = map
	self.koordinat = ()
        self.__pos = {"x":0, "y":0}
        self.__origin_position = None
        self.__cols = 0
        self.__rows = 0
        self.__gps_data = None
        self.__movement_from = {"x": 0, "y":0}
        self.__allow_movement = False
        self.__last_movement_timestamp = 0.0
        self.__zoom_level = 1
	
	self.osso_c = osso.Context("meddelande", "0.0.1", False)
    	self.osso_rpc = osso.Rpc(self.osso_c)
        
        # queue_draw() ärvs från klassen gtk.DrawingArea
        map.set_redraw_function(self.queue_draw)
      
        self.connect("expose_event", self.handle_expose_event)
        self.connect("button_press_event", self.handle_button_press_event)
        self.connect("button_release_event", self.handle_button_release_event)
	#self.connect("button_release_event", self.show_popup)
        self.connect("motion_notify_event", self.handle_motion_notify_event)
        self.set_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.EXPOSURE_MASK |
                        gtk.gdk.LEAVE_NOTIFY_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK)

	thread.start_new_thread(self.refresh, ())

    def refresh(self):
	while 1:
		self.poi_list = []
		for n in getAllPois():
			self.poi_list.append((n.coordx, n.coordy, n.name, n.time_created, n.type, n.sub_type))		
		time.sleep(5)

	
    def check_objects(self, _coord):
	self.map_objects = self.__map.get_objects()
	self.object_coordinates = []
	self.object_nr = 0
	self.hit = False
	self.clickpixlar = self.gps_to_pixel(_coord[0],_coord[1])
	## H�mtar ut kordinaterna p� alla object p� kartan
	for n in self.map_objects:
		self.object_coordinates.append(n["object"].get_coordinate())

	for n in self.object_coordinates:
		object_pixlar = self.gps_to_pixel(n["longitude"],n["latitude"])
		if(object_pixlar[0] <= self.clickpixlar[0] and (object_pixlar[0]+32) >= self.clickpixlar[0] and object_pixlar[1] <= self.clickpixlar[1] 		and (object_pixlar[1]+32) >= self.clickpixlar[1]):
			self.hit = True
			return self.map_objects[self.object_nr]		
		self.object_nr += 1
				

    def on_click_popup(self, _coord):
	### Anropar metod som kollar om det finns ett objekt p� platsen man clickat
	self.focus_target = self.check_objects(_coord)
	
	if(self.hit):
		
		self.vbox = gtk.VBox(False, 0)
		self.vbox.set_border_width(20)	
		self.vbox.show()

		self.hbox = gtk.HBox(False, 0)
		self.hbox.set_border_width(5)
		self.hbox.show()

		self.bild = gtk.Image()
		self.bild.set_from_file("ikoner/tank.png")
		self.bild.show()
		self.hbox.pack_start(self.bild, expand = False, fill = False, padding = 2)
	
		self.enhet = gtk.Label("  " + str(self.focus_target['id']))
		self.enhet.set_alignment(0, 0)
		self.enhet.show()
		self.hbox.pack_start(self.enhet, False, False, 0)

		self.vbox.pack_start(self.hbox, False, False, 2)
	
		self.x_coord = gtk.Label("X-kordinat: ")
		self.x_coord.set_alignment(0, 0)
		self.x_coord.show()
		self.vbox.pack_start(self.x_coord, False, False, 2)
	
		self.xentry = gtk.Entry()
		self.xentry.set_text(str(_coord[0]))
		self.xentry.show()	
		self.vbox.pack_start(self.xentry, False, False, 2)

		self.y_coord = gtk.Label("Y-kordinat: ")
		self.y_coord.set_alignment(0, 0)
		self.y_coord.show()
		self.vbox.pack_start(self.y_coord, False, False, 2)
	
		self.yentry = gtk.Entry()
		self.yentry.set_text(str(_coord[1]))
		self.yentry.show()	
		self.vbox.pack_start(self.yentry, False, False, 2)

		self.beskrivning = gtk.Label("Beskrivning: ")
		self.beskrivning.set_alignment(0, 0)
		self.beskrivning.show()
		self.vbox.pack_start(self.beskrivning, False, False, 3)

		self.beskriv = gtk.TextView()
		self.beskriv.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		self.beskriv.set_size_request(300, 100)	
		self.beskriv.show()
		self.vbox.pack_start(self.beskriv, False, False, 2)
	
		self.stang = gtk.Button("Stang")
		self.stang.connect("clicked", self.avs, "Stang")
		self.stang.show()
		self.vbox.pack_start(self.stang,True,True,0)

		self.popup = gtk.Window()
		self.popup.set_title(" ")
		self.popup.set_size_request(300,500)
		self.popup.add(self.vbox)
		self.popup.set_modal(True)
		self.popup.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_DIALOG )	
	
		self.popup.show()

	else:
		self.vbox = gtk.VBox(False, 0)
		self.vbox.set_border_width(10)	
		self.vbox.show()
	
		combobox = gtk.combo_box_new_text()
		combobox.append_text("Poi")
		combobox.append_text("Mission")
		combobox.append_text("Unit")
		combobox.set_active(0)
		combobox.show()	
		self.vbox.pack_start(combobox, False, False, 3)
	
		self.x_coord = gtk.Label("X-kordinat: ")
		self.x_coord.set_alignment(0, 0)
		self.x_coord.show()
		self.vbox.pack_start(self.x_coord, False, False, 2)
	
		self.xentry = gtk.Entry()
		self.xentry.set_text(str(_coord[0]))
		self.xentry.show()	
		self.vbox.pack_start(self.xentry, False, False, 2)

		self.y_coord = gtk.Label("Y-kordinat: ")
		self.y_coord.set_alignment(0, 0)
		self.y_coord.show()
		self.vbox.pack_start(self.y_coord, False, False, 2)
	
		self.yentry = gtk.Entry()
		self.yentry.set_text(str(_coord[1]))
		self.yentry.show()
		self.vbox.pack_start(self.yentry, False, False, 2)

		self.beskrivning = gtk.Label("Beskrivning")
		self.beskrivning.set_alignment(0, 0)
		self.beskrivning.show()
		self.vbox.pack_start(self.beskrivning, False, False, 3)

		self.beskriv = gtk.TextView()
		self.beskriv.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		#self.beskriv.set_size_request(200, 50)
		self.beskriv.show()
		self.vbox.pack_start(self.beskriv, False, False, 2)
	
		self.hbox = gtk.HBox(False, 0)
		self.hbox.set_size_request(198, 95)
		self.hbox.show()
	
		self.skapa = gtk.Button("Skapa")
		self.skapa.connect("clicked", self.clicked, "Skapa", _coord)
		self.skapa.show()
		self.hbox.pack_start(self.skapa,False,False,0)
	
		self.avbryt = gtk.Button("Avbryt")
		self.avbryt.connect("clicked", self.avs, "Avbryt")
		self.avbryt.show()
		self.hbox.pack_start(self.avbryt,False,False,2)
		self.vbox.pack_start(self.hbox,True,True,2)
	
		self.popup = gtk.Window()
		self.popup.set_title(" ")
		self.popup.set_size_request(250,350)
		self.popup.add(self.vbox)
		self.popup.set_modal(True)
		self.popup.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_DIALOG )	
	
		self.popup.show()
	
    def clicked(self, widget, event, __coord):
	tbuffer = self.beskriv.get_buffer()
	text = tbuffer.get_text(tbuffer.get_start_iter(), tbuffer.get_end_iter())
	temp = {"coordx": __coord[0], "coordy": __coord[1], "name": text, "time_created": time.time(), "type": "poi", "subtype": "struct"}
	print temp
	self.add_object(__coord)
	args = (json.dumps(temp),)
	self.osso_rpc.rpc_run("thor.client", "/thor/client", "thor.client", "method1", args)
	self.popup.destroy()
	
    def avs(self, widget, event, data=None):
	self.popup.destroy()

    def change_zoom(self, change):
        # Frigör minnet genom att ladda ur alla tiles för föregående nivå
        level = self.__map.get_level(self.__zoom_level)
        level.unload_tiles("all")
      
        if change == "+":
            if self.__zoom_level < 3:
                self.__zoom_level += 1
        else:
            if self.__zoom_level > 1:
                self.__zoom_level -= 1

        # Ritar ny nivå
        self.queue_draw()

    # Hanterar rörelse av kartbilden
    def handle_button_press_event(self, widget, event):
        self.__movement_from["x"] = event.x
        self.__movement_from["y"] = event.y
        self.__origin_position = self.__map.get_focus()
        self.__last_movement_timestamp = time.time()
        self.__allow_movement = True
        
	return True

    def handle_button_release_event(self, widget, event):
        self.__allow_movement = False
	if time.time() < self.__last_movement_timestamp + 0.1:
		lon, lat =  self.pixel_to_gps(self.__movement_from["x"]-self._width/2, self.__movement_from["y"]-self._height/2)
		lon = self.__origin_position["longitude"] + lon
		lat = self.__origin_position["latitude"] - lat
	
		#Har borde vi skicka till en label som visar vara koordinater"
		self.koordinat = (lon,lat)
		self.on_click_popup(self.koordinat)
		
        return True
	
    def add_object(self, _coord):
		# tjuppski
	    self.coord = (float(_coord[0]),float(_coord[1]))
	    self.__map.add_object("Tannnk", data_storage.MapObject({"longitude":(self.coord[0]-0.0016),
			                                            "latitude":(self.coord[1]+0.00075)},
			                                           "ikoner/tank.png"), time.time(), None, 'hej', 'poi', 'struct')
								   
	
    def handle_motion_notify_event(self, widget, event):
        if self.__allow_movement:
            if event.is_hint:
                x, y, state = event.window.get_pointer()
            else:
                x = event.x
                y = event.y
                state = event.state

            # Genom tidskontroll undviker vi oavsiktlig rörelse av kartan,
            # t ex ifall någon råkar nudda skärmen med ett finger eller liknande.
            if time.time() > self.__last_movement_timestamp + 0.1:
                lon, lat = self.pixel_to_gps(self.__movement_from["x"] - x,
                                             self.__movement_from["y"] - y)
                self.__map.set_focus(self.__origin_position["longitude"] + lon,
                                     self.__origin_position["latitude"] - lat)
                self.__movement_from["x"] = x
                self.__movement_from["y"] = y
            
                # Ritar om kartan
                self.queue_draw()

        return True

    def handle_expose_event(self, widget, event):
        self.context = widget.window.cairo_create()

        # Regionen vi ska rita på
        self.context.rectangle(event.area.x,
                               event.area.y,
                               event.area.width,
                               event.area.height)
	self._height = event.area.height
	self._width = event.area.width
        self.context.clip()
        self.draw()

        return False

    def set_gps_data(self, gps_data):
        self.__gps_data =  gps_data
        self.queue_draw()

    def draw(self):
        # Hämtar alla tiles för en nivå
        level = self.__map.get_level(self.__zoom_level)
        # Plockar ur de tiles vi söker från nivån
        tiles, cols, rows = level.get_tiles(self.__map.get_focus())
        self.__cols = cols
        self.__rows = rows

        self.__bounds["min_longitude"] = tiles[0].get_bounds()["min_longitude"]
        self.__bounds["min_latitude"] = tiles[0].get_bounds()["min_latitude"]
        self.__bounds["max_longitude"] = tiles[-1].get_bounds()["max_longitude"]
        self.__bounds["max_latitude"] = tiles[-1].get_bounds()["max_latitude"]

        # Ritar kartan
        for tile in tiles:
            #img = tile.get_picture()
            x, y = self.gps_to_pixel(tile.get_bounds()["min_longitude"],
                                     tile.get_bounds()["min_latitude"])
            tile.draw(self.context, x, y)

        # Ritar ut eventuella objekt
        objects = self.__map.get_objects()
        for item in objects:
            x, y = self.gps_to_pixel(item["object"].get_coordinate()["longitude"],
                                     item["object"].get_coordinate()["latitude"])

            if x != 0 and y != 0:
                item["object"].draw(self.context, x, y)
	self.queue_draw()	###### Test #######

   
    def gps_to_pixel(self, lon, lat):
        cols = self.__cols
        rows = self.__rows
        width = self.__bounds["max_longitude"] - self.__bounds["min_longitude"]
        height = self.__bounds["min_latitude"] - self.__bounds["max_latitude"]
      
        # Ger i procent var vi befinner oss på width och height
        where_lon = (lon - self.__bounds["min_longitude"]) / width
        where_lat = (self.__bounds["min_latitude"] - lat) / height
      
        # Ger i procent var focus befinner sig på width och height
        where_focus_lon = (self.__map.get_focus()["longitude"] - \
                           self.__bounds["min_longitude"]) / width
        where_focus_lat = (self.__bounds["min_latitude"] - \
                           self.__map.get_focus()["latitude"]) / height
      
        # Placerar origo i skärmens centrum
        rect = self.get_allocation()
        x = rect.width / 2.0
        y = rect.height / 2.0
      
        # Räknar ut position:
        x += (where_lon - where_focus_lon) * (cols * 300.0)
        y += (where_lat - where_focus_lat) * (rows * 160.0)
	
        return [round(x), round(y)]
   
    def pixel_to_gps(self, movement_x, movement_y):
        # Hämtar alla tiles för en nivå
        level = self.__map.get_level(self.__zoom_level)
        # Plockar ur de tiles vi söker från nivån
        tiles, cols, rows = level.get_tiles(self.__map.get_focus())
      
        # Gps per pixlar
        width = self.__bounds["max_longitude"] - self.__bounds["min_longitude"]
        height = self.__bounds["min_latitude"] - self.__bounds["max_latitude"]
        gps_per_pix_width = width / (cols * 300)
        gps_per_pix_height = height / (rows * 160)
	
      
        # Observera att kartans GPS-koordinatsystem börjar i vänstra nedre
        # hörnet, medan cairo börjar i vänstra övre hörnet! På grund av detta
        # inverterar vi värdet vi räknar fram så båda koordinatsystemen
        # överensstämmer.

	return [gps_per_pix_width * movement_x, gps_per_pix_height * movement_y]
		
