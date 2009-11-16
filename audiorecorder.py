import appuifw
import e32
import audio

audiofile= "e:\audio.wav"

sound=None

def recording():
	global S
	S=audio.Sound.open(audiofile)
	S.record()
	print "Recording"	
def playing():
	global S
	try:
		S=audio.Sound.open(audiofile)
		S.play()
		print "playing"
	except:
		print "record first"
	
def closing():
	global S
	S.stop()
	s.close()
	print "stopped"
	
def quit():
	script_lock.signal()
	appuifw.app.set_exit()
	
appuifw.app.menu =[(u"play",playing), (u"record",recording),(u"stop",closing)]
appuifw.app.exit_key_handler=quit
script_lock =e32.Ao_lock()
script_lock.wait()