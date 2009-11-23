# -*- coding: utf-8 -*-
import time
import thread
import osso
import gtk


class GPS(object):

	def to_string(self, tupel):
		stringen = ""
		for part in tupel:
			stringen += str(part) + " "
		return stringen
		
	def __init__(self):
		print "nu e jag startad vettu /tufftuff"
		self.coord = (0,0)
		self.update = False
		self.x = 58.4035
		self.y = 15.5726
		self.osso_c = osso.Context("tufftuff", "0.0.1", False)
		self.osso_rpc = osso.Rpc(self.osso_c)
		self.osso_rpc.set_rpc_callback("thor.tufftuff","/thor/tufftuff","thor.tufftuff",self.updatecoord)


	
	# Uppdaterar din kordinat
	def updatecoord(self, interface, method, arguments, user_data):
		#print "uppdaterar"
		print "nu e vi inne i updatecoord som e callbacken"
		self.coord = (self.x,self.y)
		self.x += 0.0001
		self.y += 0.0001
		return self.to_string(self.coord)
		
	 
	# Väntar på att gpsen ska hitta en kordinat
	def waiting_for_a_fix(self):
		i = 0
		print "Vi vantar pa en koordinat"
		self.coord = (5,10)
		print "Waiting: "+ str(i)
		
	def send_coordinates(self):
		self.update = True
		while (self.update == True):
			#print self.coord[0]
			#print self.coord[1]
			time.sleep(5)
			#try:
			self.updatecoord()
			#except:
			#gpsbt.stop(self.con)
	
	def run(self):
		# Vantar pa en gps koordinat
		print "Waiting baby"
		self.waiting_for_a_fix()

		#self.send_coordinates()


def main():
    gtk.main()

if __name__ == "__main__":
    GPS().run()
    main()


