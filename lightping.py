import os
import re
import sys

ping = os.popen("chroot /mnt/initfs ping 130.236.218.195")

sys.stdout.flush()

while 1:
   line = ping.readline()
   print line
   if not line: break

os.sys("ping -q -c2 " +"130.236.218.195","r")
