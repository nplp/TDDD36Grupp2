# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui_map
import guitest

class Start(object):

	def __init__(self):
		self.hej = 5		

	def runmap(self):
		self.mapxml = map_xml_reader.MapXML("./kartdata/map.xml")
		self.map = data_storage.MapData(self.mapxml.get_name(),
		                   self.mapxml.get_levels())
		self.map.set_focus(15.5726, 58.4035)

		self.map.add_object("Ambulans1", data_storage.MapObject({"longitude":15.57796,
			                                            "latitude":58.40479},
			                                           "ikoner/ambulans.png"))
		self.map.add_object("Brandbil1", data_storage.MapObject({"longitude":15.5729,
			                                            "latitude":58.40193},
			                                           "ikoner/brandbil.png"))
		self.map.add_object("Sjukhus1", data_storage.MapObject({"longitude":15.5629,
			                                           "latitude":58.4093},
			                                          "ikoner/sjukhus.png"))
		self.map.add_object("Tank", data_storage.MapObject({"longitude":(15.5726),
								"latitude":(58.4035)},
							        "ikoner/tank.png"))
	

		self.app = guitest.Gui(self.map)
		self.app.run()

	def run(self):
		print 'hej'
		self.runmap()

def main():
    gtk.main()

if __name__ == "__main__":
    Start().run()
    main()
