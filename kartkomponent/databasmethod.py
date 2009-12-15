# client database
# coding:utf-8
# OvanstÃ¥ende rad Ã¤r ISO-kodning fÃ¶r att Ã¥Ã¤Ã¶ ska funka.

from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import *
import os

#skapar databasen
engine = create_engine('sqlite:///data.db', echo=False)
metadata = MetaData()


def generate_id():
	id_nr=get_last_id()
	id_nr+=1
	add_last_id(id_nr)
	idn=(id_nr*10)+2
	#print id_nr
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
		self.id=id
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
	session_get_last_id=Session()
	try:
		
		hej=session_get_last_id.query(Idnumber).first()
		
		return hej.idnummer
	
	except:
		return None
	session_get_last_id.close()

def add_last_id(idnummer1):
	idSession=Session()
	i=idSession.query(Idnumber).first()
	i.idnummer=idnummer1
	idSession.add(i)
	idSession.commit()

	


#retunerar alla användare
def get_user_all():
	session_getuser= Session()
	try:
		
		return session_getuser.query(User).all()
		
	except:
		return None
	session_getuser.close()
	
#retunerar lösenord hos en användare
def get_password(namn):
	session_getpw= Session()
	try:
		
		p=session_getpw.query(User).filter_by(name=namn).first()
		
		return p.password
	
	except:
		return None
	session_getpw.close()

#retunerar True eller False beroende om en användare finns i databasen eller inte
def is_user(clientname):
	loginSession=Session()
	try:
		user= loginSession.query(User).filter_by(name =clientname).first()
	except:
		return False

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
	loginSession.close()

#retunerar grupper som en användare tillhör
def get_user_groups(namn):
	session_user_g = Session()
	try:
		
		snubbe=session_user_g.query(User).filter_by(name=namn).first()
		
		return snubbe.groups
	except:
		return None
	session_user_g.close()
	
#retunerar retunerar användare som finns i en grupp
def get_group_users(namn):
	session_get_gropu_user= Session()
	try:	
		
		s=session.query(Group).filter_by(name=namn).first()
		
		return s.users
	except:
		return None
	session_get_gropu_user.close()

#raderar en grupp (obs! raderar inte användare)
def delete_group(namn):
	session_delete_group=Session()
	try:
		
		session_delete_group.delete(get_group(namn))
		
	except:
		pass
	session_delete_group.close()
	
#raderar enskilda användare i en grupp
def delete_group_user(groupname,username):
	session_delete_group_user = Session()
	try:
		
		u=session_delete_group_user.query(User).filter_by(name=username).first()
		g=session_delete_group_user.query(Group).filter_by(name=groupname).first()
		u.groups.remove(g)
		
		
	except:
		pass
	session_delete_group_user.close()

#lägger in användare i en grupp	
def add_group_user(groupname,username):
	session_add_group_user=Session()
	try:
		
		u=add_group_user.query(User).filter_by(name=username).first()
		g=add_group_user.query(Group).filter_by(name=groupname).first()
		u.groups.append(g)
		
		
	except:
		pass
	add_group_user.close()
	
#retunerar alla grupper
def get_group_all():
	session_get_group_all=Session()
	try:	
		
		g=session_get_group_all.query(Group).all()
		
		return g
	except:
		return None
	session_get_group_all.close()
#retunerar namnet på en grupp 
def get_group(namn):
	session_get_group=Session()
	try:
		
		g=session_get_group.query(Group).filter_by(name=namn).first()
		
		return g
	except:
		return None
	session_get_group.close()
	
#retunerar antalet items som finns (obs! endast första träffen)
def getCount(namn):
	session_getCount=Session()
	try:
		
		c=session_getCount.query(Item).filter_by(name=namn).first().count
		
		return c
	except:
		return None
	session_getCount.close()
	
#lägger in ett item
def add_item(name1,count1,location1):
	session_add_item=Session()
	session_add_item.add(Item(name=name1,count=count1,location=location1))
	session_add_item.commit()
	
def get_item_all():
	session_get_item_all=Session()
	try:
		
		i=session_get_item_all.query(Item).all()
		
		return i
	except:
		return None
	session_get_item_all.close()

# Retunerar totala antalet av ett item (summerar)
def getTotal(namn):	
	session_getTotal=Session()
	try:	
		
		temp=0
		for item in session_getTotal.query(Item).filter_by(name=namn):
			temp = item.count + temp
		
		return temp
	except:
		return None
	session_getTotal.close()
	
#retunerar ett mission object (sökning med namn)
def get_mission_object_by_name(namn):
	session_get_mission_object_by_name=Session()
	try:
		
		m=session_get_mission_object_by_name.query(Mission).filter_by(name=namn).first()
		
		return m
	except:
		return None
	session_get_mission_object_by_name.close()
	
#retunerar ett mission object (sökning med id)
def get_mission_by_id(id_nr):
	session_get_mission_by_id=Session()
	try:
		
		m=session_get_mission_by_id.query(Mission).filter_by(id=id_nr).first()
		
		return m
	except:
		return None
	session_get_mission_by_id.close()
	
def get_mission_by_id_all(id_nr):
	session_get_mission_by_id_all=Session()
	try:
		
		m=session_get_mission_by_id_all.query(Mission).filter_by(id=id_nr).first()
		return m.name, m.time_created, m.time_changed, m.status, m.desc, m.contact_person, m.contact_number
		
	except:
		return None
	session_get_mission_by_id_all.close()
	
#Lägger in ett uppdrag
#obs! lägg inte in ett uppdrag med samma namn om du vill söka med namn!
def addMission(name1, time_created1, time_changed1, status1, desc1, contact_person1, contact_number1):
	session_addMission=Session()
	session_addMission.add(Mission(name=name1, time_created=time_created1, time_changed=time_changed1, status=status1, desc=desc1, contact_person=contact_person1, contact_number=contact_number1))
	session_addMission.commit()	
	
#retunerar all uppdragsdata	
def get_mission_all(namn):
	
	try:
		m= get_mission_object_by_name(namn)
		return m.name, m.time_created, m.time_changed, m.status, m.desc, m.contact_person, m.contact_number
	except:
		return None
	
def getPoi(namn):
	session_getPoi.Session()
	try:
		m=session_getPoi.query(Poi).filter_by(name=namn).first()
		return m
	except:
		return None
	session_getPoi.close()
	
def addPoi(coordx1, coordy1,name1,time_created1,type1,sub_type1):
	session_addPoi=Session()
	session_addPoi.add(Poi(coordx=coordx1, coordy=coordy1, name=name1, time_created=time_created1, type=type1, sub_type=sub_type1))
	session_addPoi.commit()
	
#lägger in användare i en grupp	
def add_mission_poi(mission_id,poi_id):
	session_add_mission_poi=Session()
	try:
		m=session_add_mission_poi.query(Mission).filter_by(id=mission_id).first()
		p=session_add_mission_poi.query(Poi).filter_by(id=poi_id).first()
		m.pois.append(p)
		
	except:
		pass
	session_add_mission_poi.commit()
	
#lägger in ett medelande i databasen
def addMessage(sender1, receiver1, type1, subtype1, time_created1, subject1, message1,response_to1):
	session_addMessage = Session()
	session_addMessage.add(Message(sender=sender1, receiver=receiver1, id=generate_id(), type=type1, subtype=subtype1, time_created=time_created1, subject=subject1, message=message1, response_to=response_to1))
	session_addMessage.commit()
	
def addMessageClient(sender1, receiver1, id1, type1, subtype1, time_created1, subject1, message1,response_to1):
	session_addMessage = Session()
	session_addMessage.add(Message(sender=sender1, receiver=receiver1, id=id1, type=type1, subtype=subtype1, time_created=time_created1, subject=subject1, message=message1, response_to=response_to1))
	session_addMessage.commit()


def getMessage(id_nr):
	session_getMessage=Session()
	try:
		m=session_getMessage.query(Message).filter_by(id=id_nr).first()
		return m
	except:
		return None
	session_getMessage.close()

def getAllMessages():
	session_getAllMessages=Session()
	try:
		m=session_getAllMessages.query(Message).all()
		return m
	except:
		return None
	session_getAllMessages.close()
	
def getAllPois():
	session_getAllPois=Session()
	try:
		m=session_getAllPois.query(Poi).all()
		return m
	except:
		return None
	session_getAllMPois.close()
	
def getAllMessageID():
	idList=[]
	for item in getAllMessages():
		idList.append(item.id)
	return idList
	
def getAllPoiID():
	idList=[]
	for item in getAllPois():
		idList.append(item.id)
	return idList
	
def removeMessage(id_nr):
	session_removeMessage=Session()
	try:
		m=session_removeMessage.query(Message).filter_by(id=id_nr).first()
		session_removeMessage.delete(m)
	except:
		pass
	session_removeMessage.commit()
	
def addUnit(coordx1, coordy1, name1, time_changed1, type1):
	session_addUnit=Session()
	session_addUnit.add(Unit(coordx=coordx1, coordy=coordy1, name=name1, time_changed=time_changed1, type=type1))
	session_addUnit.commit()
	
def add_mission_unit(mission_id, unit_id):
	session_add_mission_unit=Session()
	try:
		m=session.query(Mission).filter_by(id=mission_id).first()
		u=session.query(Unit).filter_by(id=unit_id).first()
		m.units.append(u)
		
	except:
		pass
	session_add_mission_unit.commit()
	
def removeUnit():
	pass



def getUnits():
	session_getUnits=Session()
	try:
		m=session_getUnits.query(Unit).first()
		return m.coordx,m.coordy,m.name,m.time_changed,m.type
	except:
		return None
	session_getUnits.close()
	
def getUnit(namn):
	session_getUnit=Session()
	m=session_getUnit.query(Unit).filter_by(name=namn).first()
	return m
	session_getUnit.close()
	
def class2dict(o):
    """Return a dictionary from object that has public
       variable -> key pairs
    """    
    dict = {}
    #Joy: all the attributes in a class are already in __dict__
    for elem in o.__dict__.keys():
        if elem.find("_" + o.__class__.__name__) == 0:
            continue
        elif(elem.startswith('_')):
            pass
            #We discard private variables, which are automatically
            #named _ClassName__variablename, when we define it in
            #the class as __variablename
        else:
            dict[elem] = o.__dict__[elem]
	    if(str(dict[elem]).startswith('<')):#bugg: man far inte borja ett meddelande med <
		   dict[elem] = class2dict(o.__dict__[elem])
    return dict	
def generate_init():
	session_id = Session()
	idt=Idnumber()
	idt.idnummer=0
	session_id.add(idt)
	session_id.commit()
	
def create_users():
	session_user=Session()
	#skapar niklas
	user_niklas=User()
	user_niklas.name='niklas'
	user_niklas.clearance='normal'
	user_niklas.password='123'
	session_user.add(user_niklas)
	
	#skapar grupper
	g=Group()
	g2=Group()
	g.name='team2'
	g2.name='team3'
	pro=Group()
	pro.name='Pro'
	go=Group()
	go.name='teamgobject'
	
	session_user.add(g)
	session_user.add(g2)
	session_user.add(pro)
	session_user.add(go)
	user_niklas.groups.append(g)
	user_niklas.groups.append(g2)
	
	
	user_mathias= User(name='mathias', clearance='normal', password='123')
	user_mathias.groups.append(pro)
	user_mathias.groups.append(go)
	
	
	user_thor= User(name='thor', clearance='normal', password='gobject')
	user_thor.groups.append(g)
	user_thor.groups.append(go)
	
	
	user_christopher=User(name='christoffer', clearance='normal', password='123')
	user_christopher.groups.append(g)
	
	
	user_hanna= User(name='hanna', clearance='normal', password='123')
	user_hanna.groups.append(g)
	
	
	user_manuela=User(name='manuela', clearance='normal', password='123')
	user_manuela.groups.append(g)
	
	
	user_kj=User(name='kj', clearance='normal', password='123')
	user_kj.groups.append(g)
	user_kj.groups.append(pro)
	
	user_secret=User(name='secret', clearance='normal', password='321')
	user_secret.groups.append(pro)
	#commitar alla users
	session_user.commit()
	
