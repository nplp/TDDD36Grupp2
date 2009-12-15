# -*- coding: utf-8 -*-
#from sqlalchemy.orm import mapper
#from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.orm import *
import os
from datetime import *
os.system('rm data.db')
os.system('rm data.db-journal')

from kartkomponent.databasmethod import *

#genererings init
generate_init()

#skapa anvnandare
create_users()

addMission("Save the cat",datetime.now(), datetime.now(), "active", "Go and save the cat from the burning tree.","moma Cat", "1987654321")
addMission("Kill the cat",datetime.now(), datetime.now(), "active", "Go and kill the cat in the burning tree.","Popa Cat", "1987654321")

addPoi(55,55,"Pastavagnen", datetime.now(), "structure", "other")
addPoi(55,55,"zenit", datetime.now(), "structure", "other")
addPoi(55,55,"skogsbrynet", datetime.now(), "structure", "other")

add_mission_poi(122,152)

add_mission_poi(122,162)

addUnit(55, 55, "Fallskarmsjagare", datetime.now(), "army")
addUnit(55, 55, "Sjukhus", datetime.now(), "army")
addUnit(55, 55, "Fallskarmsjagare", datetime.now(), "army")

addMessage('mathias','hanna','text',"change",datetime.now(),"Uppdrag",'Hej hanna, hur mar du. Har du det bra dar ute pa falt, halsa baevrarna', 1)

#addMessage('mathias','kj','text',"change",datetime.now(),"hej",'hejejehejejkheje', 1)


add_item('Pansarvagn', 10, 'Linkoping')
add_item('Pansarvagn', 70, 'Linkoping')
add_item('EMP', 1, 'Linkoping')
add_item('Stege', 10, 'Linkoping')
add_item('El-Verk', 50, 'Linkoping')
add_item('Sjukhustalt', 15, 'Linkoping')
add_item('Tjugomannartalt', 210, 'Linkoping')
add_item('Sovsackar', 130, 'Linkoping')
add_item('Lastbilar', 37, 'Linkoping')
add_item('Diselvarmare', 59, 'Linkoping')
add_item('Sprinterbuss', 5, 'Linkoping')




#USERS = get_user_all() # radera kj?




#print m
#m= class2dict(m)
#print m
#print generate_id()


#print get_mission_object_by_name('Save the cat')
#print class2dict(get_mission_object_by_name('Save the cat'))


#m= get_mission_by_id(1).pois
#print m[0].name
#print m[1].name
#m=get_mission_by_id(1)
#print m.units[0].name

#user2.groups.append(group2)





#print "skriver ut användare som är i: team2"
#print get_group_users('team2')
#print "skriver ut användare som är i: teamgobject"
#print get_group_users('teamgobject')
#print "skriver ut grupper som niklas är med i"
#print get_user_groups('niklas')
#print "skriver ut grupper som Mathias är med i"
#print get_user_groups('mathias')
#print "skriver ut grupp som inte finns"
#print get_group('finns inte')
