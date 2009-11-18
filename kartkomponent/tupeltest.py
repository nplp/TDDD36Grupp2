# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui_map
import guitest
#import gui1

class StartMap:

	coord = (15.5726,58.4035)

	# Kartan
	#print "Läser in kartinformation från kartdata/map.xml"
	mapxml = map_xml_reader.MapXML("./kartdata/map.xml")

	map = data_storage.MapData(mapxml.get_name(),
		                   mapxml.get_levels())

	# Ställer in vad kartkomponenten ska fokusera på (visa)
	# (blir mittenpunkten på skärmen, dvs 50% x-led, 50% y-lyd.
	map.set_focus(15.5726, 58.4035)

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
	map.add_object("Shape1", data_storage.MapObject({"longitude":coord[0],
		                                         "latitude":coord[1]},
		                                        "arc(x - 5, y - 5, 10, 0, 2 * math.pi)",
		                                        "set_source_rgb(0, 0, 0)"))
	map.add_object("Tank", data_storage.MapObject({"longitude":((coord[0]-0.0016)),
							"latitude":(coord[1]+0.00075)},
						        "ikoner/tank.png"))

	app = guitest.Gui(map)
 	app.run()
	
	

