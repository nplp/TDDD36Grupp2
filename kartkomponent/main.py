# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui
import time
import gpsbt
import thread

# Tupel dar dina kordinater sparas 
coord = (0,0)
# Ful haxx
hej = True
	
# Uppdaterar din kordinat
def updatecoord():
	global coord
	#print "uppdaterar"
	coord = gps.get_position()

# Vantar pa att gpsen ska hitta en kordinat
def waiting_for_a_fix():
	i = 0
	#print "Vi vantar pa en koordinat"
	global coord
	while (coord == (0,0)):
		coord = gps.get_position()
		print "Waiting: "+ str(i)
		i+=1
		time.sleep(2)

# En loop som uppdaterar kartan med jamna mellanrum
def updatemap():
	global coord
	while(hej == True):
		#print "lagg till objekt"
		map.add_object("Tank", data_storage.MapObject({"longitude":(coord[1]-0.0016),
								"latitude":(coord[0]+0.00075)},
								"ikoner/tank.png"))

		time.sleep(7.0)

		# Uppdaterar dina kordinater
		updatecoord()
		
		# Tar bort ditt objekt
		map.delete_object("Tank")
	
class StartMap:	
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
	mapxml = map_xml_reader.MapXML("kartdata/map.xml")
	map = data_storage.MapData(mapxml.get_name(),mapxml.get_levels())
	
	# Staller in vad kartkomponenten ska fokusera pa (visa)
	# (blir mittenpunkten pa skarmen, dvs 50% x-led, 50% y-lyd.
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
	# Print "Skapar programmets GUI."
	app = gui.Gui(map)
	
	# Kor programmet
	thread.start_new_thread(app.run, ())
	# Vantar en snabbis for att vara saker pa att alla bindningar har gjorts
	time.sleep(5.0)
	# Gar in i en loop som hela tiden uppdaterar kartan med dina nya kondinater
	updatemap()
	
def main():
    main()

if __name__ == "__main__":
    StartMap()
    main()
