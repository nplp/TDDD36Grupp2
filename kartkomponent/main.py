# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui
import time
import gpsbt
import thread

latitude,longitude = (58.4120,15.5762)
hej = True

# Spec enbart för testing
def trixy():
	print "inside da trixy one"
	latitude,longitude = (58.4021,15.5731)

# Uppdaterar din kordinat
def updatecoord():	
	print "uppdaterar"
	latitude,longitude = gps.get_position()

# Väntar på att gps'en ska hitta en kordinat
def waiting_for_a_fix():
	i = 0
	print "Vi vantar pa en koordinat"
	coord = (0,0)
	while (coord == (0,0)):
		latitude,longitude = gps.get_position()
		coord = gps.get_position()
    		print "Waiting: "+ str(i)
		i+=1
    		time.sleep(3)
	print coord

# En loop som uppdaterar kartan med jämna mellanrum
def updatemap():
	while(hej == True):
		# Kartan
		print "Läser in kartinformation från kartdata/map.xml"
		mapxml = map_xml_reader.MapXML("kartdata/map.xml")

		map = data_storage.MapData(mapxml.get_name(),
				           mapxml.get_levels())

		# Ställer in vad kartkomponenten ska fokusera på (visa)
		# (blir mittenpunkten på skärmen, dvs 50% x-led, 50% y-lyd.
		map.set_focus(longitude, latitude)

		# Ritar ut tre objekt
		map.add_object("Ambulans1", data_storage.MapObject({"longitude":15.57796,
				                                    "latitude":58.40479},
				                                   "ikoner/ambulans.png"))
		map.add_object("Brandbil1", data_storage.MapObject({"longitude":15.5729,
				                                    "latitude":58.40193},
				                                   "ikoner/brandbil.png"))
		map.add_object("Sjukhus1", data_storage.MapObject({"longitude":15.5629,
				                                   "latitude":58.4093},
				                                  "ikoner/sjukhus.png"))

		# Andra exempel på kommandon finns här:
		#   http://www.tortall.net/mu/wiki/CairoTutorial
		#   http://www.tortall.net/mu/wiki/PyGTKCairoTutorial

		map.add_object("Shape1", data_storage.MapObject({"longitude":15.5829,
				                                 "latitude":58.4093},
				                                "arc(x - 5, y - 5, 10, 0, 2 * math.pi)",
				                                "set_source_rgb(0, 0, 0)"))

		map.add_object("Shape2", data_storage.MapObject({"longitude":longitude,
				                             "latitude":latitude},
				                             "arc(x - 6, y - 6, 12, 0, 2 * math.pi)",
				                             "set_source_rgb(0, 0, 0)"))	
	
		print "Sov din javel"
		time.sleep(10.0)

		# Uppdaterar dina kordinater
		print "going to trixy"
		trixy()

		map.gui_queue_draw()



'''
# Startar GPSEN
con = gpsbt.start()
time.sleep(5.0) # wait for gps to come up

#Getting GPS coordinats
gps = gpsbt.gps()

#Vantar pa en gps koordinat
print "Waiting baby"
waiting_for_a_fix()

# Turning of GPS
#gpsbt.stop(con)
'''

# Kartan
print "Läser in kartinformation från kartdata/map.xml"
mapxml = map_xml_reader.MapXML("kartdata/map.xml")
map = data_storage.MapData(mapxml.get_name(),mapxml.get_levels())

# Ställer in vad kartkomponenten ska fokusera på (visa)
# (blir mittenpunkten på skärmen, dvs 50% x-led, 50% y-lyd.
map.set_focus(longitude, latitude)

# Ritar ut tre objekt
map.add_object("Ambulans1", data_storage.MapObject({"longitude":15.57796,
		                                    "latitude":58.40479},
		                                   "ikoner/ambulans.png"))
map.add_object("Brandbil1", data_storage.MapObject({"longitude":15.5729,
		                                    "latitude":58.40193},
		                                   "ikoner/brandbil.png"))
map.add_object("Sjukhus1", data_storage.MapObject({"longitude":15.5629,
		                                   "latitude":58.4093},
		                                  "ikoner/sjukhus.png"))

# Skapar grafiska interfacet.
print "Skapar programmets GUI."
app = gui.Gui(map)

# Kör programmet
print "Kör programmet."
thread.start_new_thread(app.run, ())

thread.start_new_thread(updatemap, ())


