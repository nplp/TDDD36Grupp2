# Message
# -*- coding: ISO-8859-1 -*-
# Ovanstående rad är ISO-kodning för att åäö ska funka.

cmdArray = ("/exit", "/list", "/quit", "/status", "/whisper")

class Message:
	text = ""
	def __init__(self, _text):
		self.text = _text

	def isCommand(self):
		if(len(self.text)>0):
			if(self.text[0] == '/'):
				return 1
		return 0

def finishCMD(msg):
	if(len(msg.text)>1):
		cat = str.split(msg.text,' ',1)
		
		for cmd in cmdArray:
			if cmd.startswith(cat[0]):
				if(len(cat)>1):
					return cmd + " " + cat[1]
				else:	return cmd
	return msg.text


