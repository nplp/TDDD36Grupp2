
# -*- coding: ISO-8859-1 -*-
# Ovanstï¿ï¾¥ende rad ï¿ï¾¤r ISO-kodning fï¿ï¾¶r att ï¿ï¾¥ï¿ï¾¤ï¿ï¾¶ ska funka.

import os
import re
import sys

Host = '130.236.218.21' 
Host2 = '192.160.200.1'
# \d matchar antales received paket
lifeline = re.compile(r"(\d) received")

#pingar given ip ger sammafattning av försök
ping = os.popen("chroot /mnt/initfs ping -q -c2 " +Host,"r")

sys.stdout.flush()

#Kollar igenom hela "filen" man får av ping.readline()
while 1:
   line = ping.readline()
   if not line: break
   igot = re.findall(lifeline,line)
   if igot:
    if(int(igot[0])==0):
        print "server down"
    else:
        print "go ahead bitches"
