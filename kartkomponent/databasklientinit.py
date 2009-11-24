# client database
# coding:utf-8
# OvanstÃ¥ende rad Ã¤r ISO-kodning fÃ¶r att Ã¥Ã¤Ã¶ ska funka.

from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import *

#skapar databasen
engine = create_engine('sqlite:///dataClient.db', echo=False)
metadata = MetaData()
 
group_table = Table('group', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(20))
	)
	
user_table = Table('users', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(20)),
	Column('clearance', String(40)),
	Column('password', String(40))
	)
	
items_table = Table('items_table', metadata,
	Column('item_id', Integer, primary_key=True),
	Column('name', String(40)),
	Column('count', Integer),
	Column('location', String(40))
	)

user_group = Table('user_group', metadata,
	Column('user_id', None, ForeignKey('users.id'), primary_key=True),
	Column('group_id', None, ForeignKey('group.id'), primary_key=True)
	)
	
mission_table =Table('missions', metadata,
	Column('id', Integer, primary_key=True),
	Column('poi_id', Integer),
	Column('name', String(50)),
	Column('timestamp', Integer),
	Column('contact_person', String(50)),
	Column('contact_number', String(50)),
	Column('type', String(50)),
	Column('subtype', String(50)),
	Column('description', String(200)),
	Column('status', String(50)),
	Column('finishtime', String(50))
	)
poi_table =Table('pois', metadata,
	Column('id', Integer, primary_key=True),
	Column('coordx', Float),
	Column('coordy', Float),
	Column('name', Float),
	Column('timestamp', Float),
	Column('type', String(50)),
	Column('subtype', String(50))
	)
alarm_table =Table('alarms', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(50)),
	Column('timestamp', Float),
	Column('type', String(50)),
	Column('subtype', String(50)),
	Column('contact_number', String(50)),
	Column('contact_person', String(50)),
	Column('extra_info', String(200)),
	)
unit_table = Table('units',metadata,
	Column('id', Integer, primary_key=True),
	Column('coordx', Float),
	Column('coordy', Float),
	Column('name', String(50)),
	Column('timestamp', Float),
	Column('type', String(50))
	)
		
message_table = Table('messages',metadata,
	Column('id', Integer, primary_key=True),
	Column('sender', String(50)),
	Column('reciver', String(50)),
	Column('messagetype', String(50)),
	Column('timestamp', Integer),
	Column('content', String(50)),
	Column('priority', String(50))
	)
mission_group = Table('mission_group', metadata,
	Column('mission_id', None, ForeignKey('missions.id'), primary_key=True),
	Column('group_id', None, ForeignKey('group.id'), primary_key=True)
	)
	
		
#definerar Session och kopplar den till databasen
Session = sessionmaker()
Session.configure(bind=engine)

##############################definerar classer##################################
class Message(object):
	def __init__(self, sender = None, reciver=None, messagetype= None, timestamp=None, content= None, priority= None):
		self.sender=sender
		self.reciver=reciver
		self.messagetype=messagetype
		self.timestamp=timestamp
		self.content=content
		self.priority=priority
		
class User(object):
	def __init__(self, name=None, clearance=None,  password=None):
		self.name=name
		self.clearance=clearance
		self.password=password	
	def __repr__(self):
		return self.name
class Item(object):
	def __init__(self, name=None, count=None, location=None):
		self.name=name
		self.count=count
		self.location=location
	def __repr__(self):
		return "<Item('%s','%s', '%s')>" % (self.name, self.count, self.location)
class Group(object):
	
	def __init__(self, name=None):
		self.name=name
	def __repr__(self):
		return self.name

class Mission(object):
	def __init__(self, poi_id = None, id=None, name= None, timestamp=None, type= None, sub_type= None, description = None, contact_person = None, contact_number = None, status = None, finishtime = None):
		#self.id = generate_id()
		self.poi_id = poi_id
		self.id=id
		self.name = name
		self.timestamp = timestamp
		self.type = type
		self.contact_person = contact_person
		self.contact_number = contact_number
		self.sub_type = sub_type
		self.description = description
		self.status = status
		self.finishtime = finishtime

class Poi(object):
	def __init__(self, coordx= None, coordy= None, id=None, name= None, timestamp=None, type=None, sub_type= None):
		self.coordx = coordx
		self.coordy = coordy
		self.id = id
		self.name = name
		self.timestamp = timestamp
		self.type = type
		self.sub_type = sub_type
	
		
class Alarm(object):
	def __init__(self, id=None, name= None, timestamp=None, type= None, poi_id=None, contact_person= None, contact_number= None, extrainfo = None):
		self.id=id
		self.name = name
		self.timestamp = timestamp
		self.type = type
		self.poi_id=poi_id
		self.contact_person = contact_person
		self.contact_number = contact_number
		self.extrainfo = extrainfo

class Unit(object):
	def __init__(self, coordx= None, coordy= None, id=None, name= None, timestamp=None, type= None):
		self.coordx = coordx
		self.coordy = coordy
		self.id = id
		self.name = name
		self.timestamp = timestamp
		self.type = type
				
		
metadata.create_all(engine)

#länkar classobject till datatabeller
mapper(Message, message_table)
mapper(Group, group_table)
mapper(Poi, poi_table)
mapper(Alarm, alarm_table)
mapper(Unit, unit_table)

#many to many relationer för att kunna länka grupper till uppdrag
mapper(Mission, mission_table, properties=dict(
	groups=relation(Group, secondary= mission_group, backref='missions'))
	)
	
#many to many relation för att kunna länka användarkonton till grupper
mapper(User, user_table, properties=dict(
	groups=relation(Group, secondary= user_group, backref='users'))
	)

mapper(Item, items_table)



############################Metoder###########################

#retunerar alla användare
def get_user_all():
	return session.query(User).all()

#retunerar lösenord hos en användare
def get_password(namn):
	try:
		p=session.query(User).filter_by(name=namn).first()
		return p.password
	except:
		return None

#retunerar True eller False beroende om en användare finns i databasen eller inte
def is_user(clientname):
	user= session.query(User).filter_by(name =clientname).first()
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
	return session.query(Group).all()

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
	return session.query(Item).all()
	
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
		return m.name, m.timestamp, m.type, m.description, m.contact_person, m.contact_number, m.status, m.finishtime
	except:
		return None
#Lägger in ett uppdrag
#obs! lägg inte in ett uppdrag med samma namn om du vill söka med namn!
def addMission(name1, timestamp1, type1, description1, contact_person1, contact_number1,status1,finishtime1):
	session.save(Mission(name=name1, timestamp=timestamp1, type=type1, description=description1, contact_person=contact_person1, contact_number=contact_number1, status=status1, finishtime=finishtime1))	
	
#retunerar all uppdragsdata	
def get_mission_all(namn):
	try:
		m= get_mission_object_by_name(namn)
		return m.name, m.timestamp, m.type, m.description, m.contact_person, m.contact_number, m.status, m.finishtime
	except:
		return None

#lägger in ett medelande i databasen
def addMessage(sender1, reciver1, messagetype1, timestamp1, content1, priority1):
	session.save(Message(sender=sender1, reciver=reciver1, messagetype=messagetype1, timestamp=timestamp1, content=content1, priority=priority1))
#######################################################	
session = Session()
USERS = session.query(User).all() # radera kj?
session.close()

def getMessage(id_nr):
	try:
		m= session.query(Message).filter_by(id=id_nr).first()
		return m.sender, m.reciver, m.messagetype, m.timestamp, m.content, m.priority
	except:
		return None
def removeMessage(id_nr):
	m=session.query(Message).filter_by(id=id_nr).first()
	session.delete(m)
###########################Spårutskrifter############################	

#skapar en session för att kunna komma åt databasen
session = Session()
addMission("Bombdad", datetime.now(),"Rescue","en cyckelparkering ar sprangd bygg en ny cyckelparkering", "Cyckelpappan", "1234534237678","Ongoing","10 hours")

addMission("Save the cat",datetime.now(),"Rescue","Go and save a cat from a burning tree.", "Moma Cat", "123457678","Ongoing","4 hours")

session.save(Item('Pansarvagn', 10, 'Linkoping'))
session.save(Item('Pansarvagn', 70, 'Linkoping'))
session.save(Item('EMP', 1, 'Linkoping'))
session.save(Item('Stege', 10, 'Linkoping'))
session.save(Item('El-Verk', 50, 'Linkoping'))
session.save(Item('Sjukhustalt', 15, 'Linkoping'))
session.save(Item('Tjugomannartalt', 210, 'Linkoping'))
session.save(Item('Sovsackar', 130, 'Linkoping'))
session.save(Item('Lastbilar', 37, 'Linkoping'))
session.save(Item('Diselvarmare', 59, 'Linkoping'))
session.save(Item('Sprinterbuss', 5, 'Linkoping'))
session.commit()









