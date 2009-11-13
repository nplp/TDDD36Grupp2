# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui
import time
import gpsbt
import thread

coord = (0,0)
hej = True
'''
# Spec enbart för testing
def trixy():
	print "inside da trixy one"
	latitude,longitude = (58.4120,15.5762)
	map.add_object("Shape2", data_storage.MapObject({"longitude":longitude,
				                             "latitude":latitude},
				                             "arc(x - 10, y - 10, 20, 0, 2 * math.pi)",
				                             "set_source_rgb(0, 0, 0)"))	
	latitude,longitude = (58.3021,15.5531)
	map.add_object("Shape2", data_storage.MapObject({"longitude":longitude,
			                             "latitude":latitude},
			                             "arc(x - 8, y - 8, 16, 0, 2 * math.pi)",
			                             "set_source_rgb(0, 0, 0)"))	
'''
# Uppdaterar din kordinat
def updatecoord():	
	print "uppdaterar"
	coord = gps.get_position()

# Väntar på att gpsen ska hitta en kordinat
def waiting_for_a_fix():
	i = 0
	print "Vi vantar pa en koordinat"
	global coord
	while (coord == (0,0)):
		#latitude,longitude = gps.get_position()
		coord = gps.get_position()
    		print "Waiting: "+ str(i)
		i+=1
    		time.sleep(3)
	print coord

# En loop som uppdaterar kartan med jämna mellanrum
def updatemap():
        global coord
	while(hej == True):
		print "lägg till objekt"
                updatecoord()
		print coord[0]
		print coord[1]
		time.sleep(5.0)
		map.add_object("Shape2", data_storage.MapObject({"longitude":coord[1],
				                             "latitude":coord[0]},
				                             "arc(x - 6, y - 6, 12, 0, 2 * math.pi)",
				                             "set_source_rgb(0, 0, 0)"))	
		print "Sov din javel"
		time.sleep(10.0)
		
		# Uppdaterar dina kordinater
		print "going to update"
		updatecoord()





# Startar GPSEN
con = gpsbt.start()
time.sleep(2.0) # wait for gps to come up

#Getting GPS coordinats
gps = gpsbt.gps()

#Vantar pa en gps koordinat
print "Waiting baby"
waiting_for_a_fix()

# Turning of GPS
#gpsbt.stop(con)


# Kartan
print "Läser in kartinformation från kartdata/map.xml"
mapxml = map_xml_reader.MapXML("kartdata/map.xml")
map = data_storage.MapData(mapxml.get_name(),mapxml.get_levels())

# Ställer in vad kartkomponenten ska fokusera på (visa)
# (blir mittenpunkten på skärmen, dvs 50% x-led, 50% y-lyd.
map.set_focus(coord[1], coord[0])

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
print "Innan updatemap"
updatemap()


