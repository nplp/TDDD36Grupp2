# -*- coding: utf-8 -*-
import data_storage
import map_xml_reader
import gui_map
import guitest
import Tufftuff
import time
import thread
import osso
import gtk
import subprocess

class Start(object):

	def __init__(self):
		self.coord = None
		self.gpsrun = True
		self.stringcoord = None
		
	def to_tuple(self, stringen):
		tupeln = tuple(stringen.split())
		tupeln = (float(temp[0]), float(temp[1]))
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
		self.map.add_object("Tank", data_storage.MapObject({"longitude":(15.5726),
								"latitude":(58.4035)},
							        "ikoner/tank.png"))

	def init_tufftuff(self):
		try:
			print "kor den andra except"
			subprocess.call('python Tufftuff2.py &', shell=True)

		except Error, e:
			print "kor den forsta try"
			subprocess.call('/scratchbox/login | dbus-uuidgen --ensure | /usr/bin/af-sb-init.sh start | python2.5 Tufftuff2.py &', shell=True)
		

	
	def getcoords(self):
		print "Efter subprocess"		
		#os.system('python Tufftuff.py')		
		#self.instans = Tufftuff.GPS()
		#self.instans.run()
		self.osso_c = osso.Context("start", "0.0.1", False)
		self.osso_rpc = osso.Rpc(self.osso_c)
		while(self.gpsrun == True):		
			time.sleep(3)
			print "powernap booya!"
			while(self.stringcoord == None):
				self.stringcoord = self.osso_rpc.rpc_run("thor.tufftuff", "/thor/tufftuff", "thor.tufftuff", "updatecoord", (), wait_reply = True)
				self.coord = self.to_tuple(self.stringcoord)
				time.sleep(1)
			#self.coord = self.instans.updatecoord()
			print self.coord[0]
			print self.coord[1]
	
	def startgui(self):
		self.gui = guitest.Gui(self.map)
		thread.start_new_thread(self.gui.run, ())

	def run(self):
		self.createmap()
		self.init_tufftuff()
		self.startgui()
		print "Going to coords"
		self.getcoords()
		

def main():
    gtk.main()

if __name__ == "__main__":
    Start().run()
    main()
