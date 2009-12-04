# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui_map
import guitest
import time
import thread
import osso
import gtk
import subprocess
import sys
import gobject

class Start(object):

	def __init__(self):
		self.coord = None
		self.gpsrun = True
		self.stringcoord = 0
		self.tank_added = False
		
	def to_tuple(self, stringen):
		tupeln = tuple(stringen.split())
		tupeln = (float(tupeln[0]), float(tupeln[1]))
		return tupeln

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

	def getcoords(self):
		print "Efter subprocess"		
		self.osso_c = osso.Context("start", "0.0.1", False)
		self.osso_rpc = osso.Rpc(self.osso_c)
		time.sleep(3)
		while(self.gpsrun == True):		
			self.stringcoord = self.osso_rpc.rpc_run("thor.gps", "/thor/gps", "thor.gps", "updatecoord", (), wait_reply = True)
			print self.stringcoord
			time.sleep(4)
			
			if(self.stringcoord != 0):
				print "ritar ut tanken nu"
				self.coord = self.to_tuple(self.stringcoord)
				if(self.tank_added == True):
					self.map.delete_object("Tank")
				self.map.add_object("Tank", data_storage.MapObject({"longitude":(self.coord[1]-0.0016),
									"latitude":(self.coord[0]+0.00075)},
									"ikoner/tank.png"))
				self.tank_added = True
			
	def startgui(self):
		self.gui = guitest.Gui(self.map)
		thread.start_new_thread(self.gui.run, ())

	def run(self):
		self.createmap()
		if(len(sys.argv) > 1):
			if(sys.argv[1] == 'gps'):
				self.startgui()
				print "Going to coords"
				self.getcoords() #nu måste man ha startat gps processen innan detta steg och fått en lock
			#### Skickar fejk koordinater till clienten ####
			if(sys.argv[1] == 'tuff'):
				print 'Tuffe tuffe tuff då tåget går'
				self.startgui()
				subprocess.call('python2.5 Tufftuff.py' + ' &', shell=True)
				self.getcoords()
			else:
				print "gps av"
				PORT = sys.argv[1]
				subprocess.call('python2.5 ../client2.py'+ PORT + ' &', shell=True)
				subprocess.call('python2.5 ../client2.py &', shell=True)
				guitest.Gui(self.map).run()

		else:
			print "gps av"
			subprocess.call('python2.5 ../client2.py &', shell=True)
			guitest.Gui(self.map).run()
				

		

if __name__ == "__main__":
    gobject.threads_init()
    Start().run()

