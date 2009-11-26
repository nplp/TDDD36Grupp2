# Read database
# coding:utf-8
# OvanstÃ¥ende rad Ã¤r ISO-kodning fÃ¶r att Ã¥Ã¤Ã¶ ska funka.

from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import *

#skapar databasen
engine = create_engine('sqlite:///data.db', echo=False)
metadata = MetaData()


#######################skapar data tabeller############################33
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
	Column('time_changed', Float),
	Column('type', Text)
	)
		
message_table = Table('messages',metadata,
	Column('id', Integer, primary_key=True),
	Column('sender', Text),
	Column('reciver', Text),
	Column('type', Text),
	Column('time_created', Integer),
	Column('content', Text),
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

#############################################################################

#definerar Session och kopplar den till databasen
Session = sessionmaker()
Session.configure(bind=engine)

##############################definerar classer##################################
class Message(object):
	def __init__(self, sender=None, reciver=None, type=None, time_created=None, content=None, response_to=None):
		self.sender=sender
		self.reciver=reciver
		self.type=type
		self.time_created=time_created
		self.content=content
		self.response_to=response_to

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
		return self.name, self.count, self.location
class Group(object):
	
	def __init__(self, name=None):
		self.name=name
	def __repr__(self):
		return self.name

class Mission(object):
	def __init__(self, poi_id = None, unit_id=None, id=None, name= None, time_created=None, time_changed=None, status = None, desc=None, contact_person = None, contact_number = None):
		#self.id = generate_id()
		self.poi_id = poi_id
		self.unit_id=unit_id
		self.id=id
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
		self.id = id
		self.name = name
		self.time_created = time_created
		self.type = type
		self.sub_type = sub_type
	
class Unit(object):
	def __init__(self, coordx= None, coordy= None, id=None, name= None, time_changed=None, type= None):
		self.coordx = coordx
		self.coordy = coordy
		self.id = id
		self.name = name
		self.time_changed = time_changed
		self.type = type
		
def fillOutList(arg, roof, fill):
	diff = roof-len(arg)
	if(diff > 0):
		for i in range(diff):
			arg.append(fill)

	return arg
		
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
mapper(Message, message_table)
mapper(Group, group_table)
mapper(Poi, poi_table)

mapper(Unit, unit_table)

#many to many relationer för att kunna länka grupper till uppdrag & pois
mapper(Mission, mission_table, properties=dict(
	groups=relation(Group, secondary= mission_group, backref='missions'),
	pois=relation(Poi, secondary= mission_poi, backref='missions')
	)
	)
	
#many to many relation för att kunna länka användarkonton till grupper
mapper(User, user_table, properties=dict(
	groups=relation(Group, secondary= user_group, backref='users'))
	)

mapper(Item, items_table)



############################Metoder###########################

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
def addMessage(sender1, reciver1, type1, time_created1, content1, response_to1):
	session.save(Message(sender=sender1, reciver=reciver1, type=type1, time_created=time_created1, content=content1, response_to=response_to1))
#######################################################	
session = Session()
USERS = session.query(User).all() # radera kj?
session.close()

def getMessage(id_nr):
	#try:
		m= session.query(Message).filter_by(id=id_nr).first()
		return m.sender, m.reciver, m.type, m.time_created, m.content, m.response_to
	#except:
		#return None
def removeMessage(id_nr):
	m=session.query(Message).filter_by(id=id_nr).first()
	session.delete(m)
	
	
	
def addUnit(coordx1,coordy1,id1,name1,timestamp1,type1):
	pass

def removeUnit():
	pass

def getUnit():
	pass
###########################Spårutskrifter############################	

#skapar en session för att kunna komma åt databasen
session = Session()
print getMessage(1)
#get_mission_by_id

#sparar ändringar i databasen
session.commit()

#####################################################################






















