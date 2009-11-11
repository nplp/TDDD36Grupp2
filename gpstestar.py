import e32, appuifw, positioning
 
 
def gps_init():
	#This function will start the updating of global variable (dictionary) 'gps_data' every 0.2 sec.
	#0.2 sec comes form 'interval = 200000' set according to your needs
	#This function uses callback funtion gps
	global gps_data
	#First this fills the gps_data with 0.0 so that there is something before the first gps update
	gps_data = {
	'satellites': {'horizontal_dop': 0.0, 'used_satellites': 0, 'vertical_dop': 0.0, 'time': 0.0,'satellites': 0, 'time_dop':0.0}, 
	'position': {'latitude': 0.0, 'altitude': 0.0, 'vertical_accuracy': 0.0, 'longitude': 0.0, 'horizontal_accuracy': 0.0}, 
	'course': {'speed': 0.0, 'heading': 0.0, 'heading_accuracy': 0.0, 'speed_accuracy': 0.0}
	}
	try:
		positioning.select_module(positioning.default_module())
		positioning.set_requestors([{"type":"service","format":"application","data":"gps_app"}])
		positioning.position(course=1,satellites=1,callback=gps, interval=200000,partial=0)
		e32.ao_sleep(3)
	except:
		appuifw.note(u'Problem with GPS','error')
 
def gps(event):
	global gps_data
	gps_data = event
 
def gps_stop():
	#This function stops GPS
	try:
		positioning.stop_position()
	except:
		appuifw.note(u'Problem with GPS','error')
 
 
#Testing
gps_init()
count = 0
while True:
	count = count + 1
	sat = gps_data['satellites']['used_satellites']
	pos_lat = gps_data['position']['latitude']
	pos_long = gps_data['position']['longitude']
	speed = gps_data['course']['speed']
	print count, sat, pos_lat, pos_long,speed
	e32.ao_sleep(1) 
