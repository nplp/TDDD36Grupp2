# client database
# coding:utf-8
# Ovanstående rad är ISO-kodning för att åäö ska funka.

from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import *
import os

os.system('rm data.db')
os.system('rm data.db-journal')
#skapar databasen
from databasmethod import *

#genererings init
generate_init()

#skapa anvnandare
create_users()

addMission("Save the cat",datetime.now(), datetime.now(), "active", "Go and save the cat from the burning tree.","moma Cat", "1987654321")
addMission("Kill the cat",datetime.now(), datetime.now(), "active", "Go and kill the cat in the burning tree.","Popa Cat", "1987654321")

#addPoi(55,55,"Pastavagnen", datetime.now(), "structure", "other")
#addPoi(55,55,"zenit", datetime.now(), "structure", "other")
#addPoi(55,55,"skogsbrynet", datetime.now(), "structure", "other")

add_mission_poi(122,152)

add_mission_poi(122,162)


#addMessage('mathias1','hanna','text',"change",datetime.now(),"hej",'jason.dums() sak ska vara har tex Unit', 1)

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