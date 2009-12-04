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
		#self.x = 58.4035
		#self.y = 15.5726
		self.listspot = 0
		self.osso_c = osso.Context("tufftuff", "0.0.1", False)
		self.osso_rpc = osso.Rpc(self.osso_c)
		self.osso_rpc.set_rpc_callback("thor.gps","/thor/gps","thor.gps", self.updatecoord)
		self.going_to_da_balja = [(15.575778600000001, 58.397780400000023), (15.576193200000002, 58.397563200000022), (15.576538700000002, 58.397563200000022), (15.577160600000001, 58.397563200000022), (15.577506100000001, 58.397563200000022), (15.577575200000002, 58.397852800000024), (15.577644300000001, 58.397889000000021), (15.577644300000001, 58.398070000000025), (15.577644300000001, 58.398251000000023), (15.577644300000001, 58.398323400000024), (15.577575200000002, 58.398576800000022), (15.577575200000002, 58.398902600000021), (15.577644300000001, 58.399047400000022), (15.577713400000002, 58.399192200000023), (15.577644300000001, 58.399445600000021), (15.577644300000001, 58.399445600000021), (15.577713400000002, 58.399735200000023), (15.577713400000002, 58.39977140000002), (15.577644300000001, 58.399988600000022), (15.577644300000001, 58.400169600000027), (15.577575200000002, 58.400386800000021), (15.577644300000001, 58.400423000000025), (15.577644300000001, 58.400567800000026), (15.577644300000001, 58.400712600000027), (15.577575200000002, 58.400857400000021), (15.577644300000001, 58.401038400000026), (15.577644300000001, 58.401291800000024), (15.577713400000002, 58.401436600000025), (15.577644300000001, 58.401509000000026), (15.577644300000001, 58.401581400000026), (15.577851600000002, 58.401509000000026), (15.578128000000001, 58.401472800000022)]
		
	def to_string(self, tupel):
		stringen = ""
		for part in tupel:
			stringen += str(part) + " "
		return stringen
		
	
	# Uppdaterar din kordinat
	def updatecoord(self, interface, method, arguments, user_data):
		if(self.listspot == 32):
			self.listspot = 0
		temptupel = self.going_to_da_balja[self.listspot]
		self.listspot += 1
		#print temptupel
		self.coord = (temptupel[1],temptupel[0])
		return self.to_string(self.coord)
		
	 
	# Väntar på att gpsen ska hitta en kordinat
	def waiting_for_a_fix(self):
		#i = 0
		print "Vi vantar pa en koordinat"
		#self.coord = (5,10)
		#print "Waiting: "+ str(i)
	
	def run(self):
		# Vantar pa en gps koordinat
		print "Waiting baby"
		self.waiting_for_a_fix()


def main():
    gtk.main()

if __name__ == "__main__":
    GPS().run()
    main()


