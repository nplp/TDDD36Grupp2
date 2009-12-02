# client database
# coding:utf-8
# OvanstÃ¥ende rad Ã¤r ISO-kodning fÃ¶r att Ã¥Ã¤Ã¶ ska funka.

from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import *
import os

os.system('rm dataClient.db')
os.system('rm dataClient.db-journal')
#skapar databasen

engine = create_engine('sqlite:///dataClient.db', echo=False)
metadata = MetaData()

def generate_id():
	id_nr=get_last_id()
	id_nr+=1
	add_last_id(id_nr)
	idn=(id_nr*10)+2
	return idn
#######################skapar data tabeller############################33
last_id_table = Table('idnumbers', metadata, 
	Column('id', Integer, primary_key=True),
	Column('idnummer', Integer)
	)

group_table = Table('group', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', Text)
	)
	
user_table = Table('users', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', Text),
	Column('clearance', Text),
	Column('password', Text)
	)
	
items_table = Table('items_table', metadata,
	Column('item_id', Integer, primary_key=True),
	Column('name', Text),
	Column('count', Integer),
	Column('location', Text)
	)

user_group = Table('user_group', metadata,
	Column('user_id', None, ForeignKey('users.id'), primary_key=True),
	Column('group_id', None, ForeignKey('group.id'), primary_key=True)
	)
	
mission_table =Table('missions', metadata,
	Column('poi_ids', Integer),
	Column('unit_ids', Integer),
	Column('id', Integer, primary_key=True),
	Column('name', Text),
	Column('time_created', Integer),
	Column('time_changed', Integer),
	Column('status', Text),
	Column('desc', Text),
	Column('contact_person', Text),
	Column('contact_number', Text)
	)
poi_table =Table('pois', metadata,
	Column('coordx', Float),
	Column('coordy', Float),
	Column('id', Integer, primary_key=True),
	Column('name', Text),
	Column('time_created', Integer),
	Column('time_changed', Integer),
	Column('type', Text),
	Column('subtype', Text)
	)

unit_table = Table('units',metadata,
	Column('coordx', Float),
	Column('coordy', Float),
	Column('id', Integer, primary_key=True),
	Column('name', Text),
	Column('time_changed', Integer),
	Column('type', Text)
	)
		
message_table = Table('messages',metadata,
	Column('id', Integer, primary_key=True),
	Column('sender', Text),
	Column('receiver', Text),
	Column('type', Text),
	Column('subtype', Text),
	Column('time_created', Integer),
	Column('subject', Text),
	Column('message', Text),
	Column('response_to', Integer)
	)
mission_group = Table('mission_group', metadata,
	Column('mission_id', None, ForeignKey('missions.id'), primary_key=True),
	Column('group_id', None, ForeignKey('group.id'), primary_key=True)
	)
mission_poi = Table ('mission_poi', metadata,
	Column('mission_id', None, ForeignKey('missions.id'), primary_key=True),
	Column('poi_id', None, ForeignKey('pois.id'), primary_key=True)
	)
mission_unit = Table ('mission_unit', metadata,
	Column('mission_id', None, ForeignKey('missions.id'), primary_key=True),
	Column('unit_id', None, ForeignKey('units.id'), primary_key=True)
	)

#############################################################################

#definerar Session och kopplar den till databasen
Session = sessionmaker()
Session.configure(bind=engine)

##############################definerar classer##################################
class Idnumber(object):
	def __init__(self, idnummer=None):
		self.idnummer = idnummer

class Message(object):
	def __init__(self, id=None, sender=None, receiver=None, type=None, subtype=None, time_created=None, subject=None, message=None, response_to=None):
		self.id=generate_id()
		self.sender=sender
		self.receiver=receiver
		self.type=type
		self.subtype=subtype
		self.time_created=time_created
		self.subject=subject
		self.message=message
		self.response_to=response_to

class User(object):
	def __init__(self, name=None, id=None, clearance=None,  password=None):
		self.name=name
		self.id=generate_id()
		self.clearance=clearance
		self.password=password	
	def __repr__(self):
		return self.name
class Item(object):
	def __init__(self, name=None, id=None, count=None, location=None):
		self.name=name
		self.id=generate_id()
		self.count=count
		self.location=location
	def __repr__(self):
		return self.name, self.count, self.location
class Group(object):
	
	def __init__(self, name=None, id=None):
		self.name=name
		self.id=generate_id()
	

class Mission(object):
	def __init__(self, poi_id = None, unit_id=None, id=None, name= None, time_created=None, time_changed=None, status = None, desc=None, contact_person = None, contact_number = None):
		#self.id = generate_id()
		self.poi_id = poi_id
		self.unit_id=unit_id
		self.id=generate_id()
		self.name = name
		self.time_created = time_created
		self.time_changed = time_changed
		self.status = status
		self.desc = desc
		self.contact_person = contact_person
		self.contact_number = contact_number

class Poi(object):
	def __init__(self, coordx= None, coordy= None, id=None, name= None, time_created=None, time_changed=None, type=None, sub_type= None):
		self.coordx = coordx
		self.coordy = coordy
		self.id=generate_id()
		self.name = name
		self.time_created = time_created
		self.type = type
		self.sub_type = sub_type
	
class Unit(object):
	def __init__(self, coordx= None, coordy= None, id=None, name= None, time_changed=None, type= None):
		self.coordx = coordx
		self.coordy = coordy
		self.id=generate_id()
		self.name = name
		self.time_changed = time_changed
		self.type = type
		
		
def dbClass(cl):
	if(cl == "message"):
		return Message()

	if(cl == "user"):
		return User()

	if(cl == "item"):
		return Item()

	if(cl == "group"):
		return Group()

	if(cl == "mission"):
		return Mission()

	if(cl == "poi"):
		return Poi()

	if(cl == "unit"):
		return Unit()

	return None

metadata.create_all(engine)

#länkar classobject till datatabeller
mapper(Message, message_table, properties=dict())
mapper(Group, group_table, properties=dict())
mapper(Poi, poi_table, properties=dict())
mapper(Unit, unit_table, properties=dict())
mapper(Idnumber, last_id_table)
#many to many relationer för att kunna länka grupper till uppdrag
mapper(Mission, mission_table, properties={
	'groups': relation(Group, secondary= mission_group, backref='missions'),
	'pois': relation(Poi, secondary= mission_poi, backref='missions'),
	'units': relation(Unit, secondary= mission_unit, backref='missions')
	}
	)
	
#many to many relation för att kunna länka användarkonton till grupper
mapper(User, user_table, properties={
	'groups': relation(Group, secondary= user_group, backref='users')}
	)

mapper(Item, items_table, properties=dict())



############################Metoder###########################

def get_last_id():
	try:
		hej=session.query(Idnumber).first()
		return hej.idnummer
	
	except:
		return None

def add_last_id(idnummer1):
	i=session.query(Idnumber).first()
	i.idnummer=idnummer1
	session.add(i)
	


#retunerar alla användare
def get_user_all():
	try:
		return session.query(User).all()
	except:
		return None
#retunerar lösenord hos en användare
def get_password(namn):
	try:
		p=session.query(User).filter_by(name=namn).first()
		return p.password
	except:
		return None

#retunerar True eller False beroende om en användare finns i databasen eller inte
def is_user(clientname):

	user= loginSession.query(User).filter_by(name =clientname).first()

	def get_name(user):
		try:
			return user.name
		except Exception,e :
			return user
	
	user= get_name(user)
	if (user == clientname):
	
		return True
	else:
		return False

#retunerar grupper som en användare tillhör
def get_user_groups(namn):
	try:
		snubbe=session.query(User).filter_by(name=namn).first()
		return snubbe.groups
	except:
		return None

#retunerar retunerar användare som finns i en grupp
def get_group_users(namn):
	try:	
		s=session.query(Group).filter_by(name=namn).first()
		return s.users
	except:
		return None

#raderar en grupp (obs! raderar inte användare)
def delete_group(namn):
	try:
		session.delete(get_group(namn))
	except:
		pass
	
#raderar enskilda användare i en grupp
def delete_group_user(groupname,username):
	try:
		u=session.query(User).filter_by(name=username).first()
		g=session.query(Group).filter_by(name=groupname).first()
		u.groups.remove(g)
		
	except:
		pass

#lägger in användare i en grupp	
def add_group_user(groupname,username):
	try:
		u=session.query(User).filter_by(name=username).first()
		g=session.query(Group).filter_by(name=groupname).first()
		u.groups.append(g)
		
	except:
		pass

#retunerar alla grupper
def get_group_all():
	try:	
		return session.query(Group).all()
	except:
		return None
#retunerar namnet på en grupp 
def get_group(namn):
	try:
		g=session.query(Group).filter_by(name=namn).first()
		return g
	except:
		return None
#retunerar antalet items som finns (obs! endast första träffen)
def getCount(namn):
	try:
		return session.query(Item).filter_by(name=namn).first().count
	except:
		return None

#lägger in ett item
def add_item(name1,count1,location1):
	session.save(Item(name=name1,count=count1,location=location1))
	
def get_item_all():
	try:
		return session.query(Item).all()	
	except:
		return None

# Retunerar totala antalet av ett item (summerar)
def getTotal(namn):	
	try:	
		temp=0
		for item in session.query(Item).filter_by(name=namn):
			temp = item.count + temp
		return temp
	except:
		return None
	
#retunerar ett mission object (sökning med namn)
def get_mission_object_by_name(namn):
	try:
		m=session.query(Mission).filter_by(name=namn).first()
		return m
	except:
		return None

#retunerar ett mission object (sökning med id)
def get_mission_by_id(id_nr):
	try:
		m=session.query(Mission).filter_by(id=id_nr).first()
		return m
	except:
		return None
def get_mission_by_id_all(id_nr):
	try:
		m=session.query(Mission).filter_by(id=id_nr).first()
		return m.name, m.time_created, m.time_changed, m.status, m.desc, m.contact_person, m.contact_number
	except:
		return None
#Lägger in ett uppdrag
#obs! lägg inte in ett uppdrag med samma namn om du vill söka med namn!
def addMission(name1, time_created1, time_changed1, status1, desc1, contact_person1, contact_number1):
	session.save(Mission(name=name1, time_created=time_created1, time_changed=time_changed1, status=status1, desc=desc1, contact_person=contact_person1, contact_number=contact_number1))	
	
#retunerar all uppdragsdata	
def get_mission_all(namn):
	try:
		m= get_mission_object_by_name(namn)
		return m.name, m.time_created, m.time_changed, m.status, m.desc, m.contact_person, m.contact_number
	except:
		return None

def getPoi(namn):
	try:
		m=session.query(Poi).filter_by(name=namn).first()
		return m
	except:
		return None
def addPoi(coordx1, coordy1,name1,time_created1,type1,sub_type1):
	session.save(Poi(coordx=coordx1, coordy=coordy1, name=name1, time_created=time_created1, type=type1, sub_type=sub_type1))
#lägger in användare i en grupp	
def add_mission_poi(mission_id,poi_id):
	try:
		m=session.query(Mission).filter_by(id=mission_id).first()
		p=session.query(Poi).filter_by(id=poi_id).first()
		m.pois.append(p)
		
	except:
		pass
	
#lägger in ett medelande i databasen
def addMessage(sender1, receiver1, type1, subtype1, time_created1, subject1, message1,response_to1):
	session.save(Message(sender=sender1, receiver=receiver1, type=type1, subtype=subtype1, time_created=time_created1, subject=subject1, message=message1, response_to=response_to1))
	
	
	
	
	
#######################################################	
session = Session()
USERS = session.query(User).all() # radera kj?
session.close()

def getMessage(id_nr):
	#try:
		m=session.query(Message).filter_by(id=id_nr).first()
		return m
	#except:
	#	return None
	
def getAllMessages():
	try:
		m = session.query(Message).all()
		return m
	except Exception, e:
		print e 
		

def removeMessage(id_nr):
	m=session.query(Message).filter_by(id=id_nr).first()
	session.delete(m)
	
def addUnit(coordx1, coordy1, name1, time_changed1, type1):
	session.save(Unit(coordx=coordx1, coordy=coordy1, name=name1, time_changed=time_changed1, type=type1))

def add_mission_unit(mission_id, unit_id):
	try:
		m=session.query(Mission).filter_by(id=mission_id).first()
		u=session.query(Unit).filter_by(id=unit_id).first()
		m.units.append(u)
		
	except:
		pass

def removeUnit():
	pass



def getUnits():
	try:
		m=session.query(Unit).first()
		return m.coordx,m.coordy,m.name,m.time_changed,m.type
	except:
		return None
def getUnit(namn):
	m=session.query(Unit).filter_by(name=namn).first()
	return m
	
def class2dict(o):
    """Return a dictionary from object that has public
       variable -> key pairs
    """    
    dict = {}
    #Joy: all the attributes in a class are already in __dict__
    for elem in o.__dict__.keys():
        if elem.find("_" + o.__class__.__name__) == 0:
            continue
            #We discard private variables, which are automatically
            #named _ClassName__variablename, when we define it in
            #the class as __variablename
        else:
            dict[elem] = o.__dict__[elem]
	    if(str(dict[elem]).startswith('<') and not str(elem.startswith('_'))):#bugg: man far inte borja ett meddelande med <
		   dict[elem] = class2dict(o.__dict__[elem])
    return dict	



#######################################################	


#skapar en session för att kunna komma åt databasen
session = Session()

USERS = session.query(User).all() # radera kj?

idt=Idnumber()
idt.idnummer=0
session.add(idt)
#user2.groups.append(group2)

#skapar niklas
user_niklas=User()
user_niklas.name='niklas'
user_niklas.clearance='normal'
user_niklas.password='123'
session.save(user_niklas)

#skapar grupper
g=Group()
g2=Group()
g.name='team2'
g2.name='team3'
pro=Group()
pro.name='Pro'
go=Group()
go.name='teamgobject'

session.save(g)
session.save(g2)
session.save(pro)
session.save(go)
user_niklas.groups.append(g)
user_niklas.groups.append(g2)
#print session.query(Group).filter_by(name='team2').first()
#print session.query(Group).filter_by(name='team2').all()

user_mathias= User(name='mathias', clearance='normal', password='123')
user_mathias.groups.append(pro)
user_mathias.groups.append(go)


user_thor= User(name='thor', clearance='normal', password='gobject')
user_thor.groups.append(g)
user_thor.groups.append(go)


user_christopher=User(name='christopher', clearance='normal', password='123')
user_christopher.groups.append(g)


user_hanna= User(name='hanna', clearance='normal', password='123')
user_hanna.groups.append(g)


user_manuela=User(name='manuela', clearance='normal', password='123')
user_manuela.groups.append(g)


user_kj=User(name='kj', clearance='normal', password='123')
user_kj.groups.append(g)
user_kj.groups.append(pro)


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

#add_mission_unit(122,172)
#print generate_id()
#addMessage('mathias1','hanna',"change",datetime.now(),'jason.dums() sak ska vara har tex Unit', 1)
addMessage('mathias1','hanna','text',"change",datetime.now(),"hej",'jason.dums() sak ska vara har tex Unit', 1)
#print getMessage(202)
#print class2dict(getMessage(202))

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
#m=getUnits()
session.commit()

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

