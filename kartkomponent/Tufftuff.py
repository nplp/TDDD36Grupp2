# -*- coding: utf-8 -*-
import time
import thread
import osso
import gtk


class GPS(object):

	def __init__(self):
		print "nu e jag startad vettu /tufftuff"
		self.coord = (0,0)
		self.update = False
		self.x = 58.4035
		self.y = 15.5726
		self.osso_c = osso.Context("tufftuff", "0.0.1", False)
		self.osso_rpc = osso.Rpc(self.osso_c)
		self.osso_rpc.set_rpc_callback("thor.gps","/thor/gps","thor.gps", self.updatecoord)

	def to_string(self, tupel):
		stringen = ""
		for part in tupel:
			stringen += str(part) + " "
		return stringen
		
	
	# Uppdaterar din kordinat
	def updatecoord(self, interface, method, arguments, user_data):
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
	
	def run(self):
		# Vantar pa en gps koordinat
		print "Waiting baby"
		self.waiting_for_a_fix()


def main():
    gtk.main()

if __name__ == "__main__":
    GPS().run()
    main()


