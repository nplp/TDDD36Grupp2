# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui_map
import guitest
import Tufftuff
import time
import thread

class Start(object):

	def __init__(self):
		self.coord = (0,0)		

	def createmap(self):
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

	def getcoords(self):
		Tufftuff.GPS.run()
		time.sleep(2)
		self.coord = Tufftuff.updatecoord()
		print self.coord[0]
		print self.coord[1]
	
	def startgui(self):
		self.app = guitest.Gui(self.map)
		self.app.run()

	def run(self):
		self.createmap()
		self.startgui()
		thread.start_new_thread(self.getcoords, ())
		#self.getcoords()
		

def main():
    gtk.main()

if __name__ == "__main__":
    Start().run()
    main()
