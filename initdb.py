# -*- coding: utf-8 -*-
#from sqlalchemy.orm import mapper
#from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.orm import *
import os
from datetime import *
os.system('rm data.db')
os.system('rm data.db-journal')
engine = create_engine('sqlite:///data.db', echo=False)
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
	
mission_group = Table('mission_group', metadata,
	Column('mission_id', None, ForeignKey('missions.id'), primary_key=True),
	Column('group_id', None, ForeignKey('group.id'), primary_key=True)
	)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
	
class User(object):
	def __init__(self, name=None, clearance=None,  password=None):
		self.name=name
		self.clearance=clearance
		self.password=password	
	def __repr__(self):
		return (self.name)
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
#class Mission(object):
	#def __init__(self, title=None, body=None, time=None, location=None):
		#self.title=title
		#self.body=body
		#self.time=time
		#self.location=location
class mission(object):
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
class poi(object):
	def __init__(self, coordx= None, coordy= None, id=None, name= None, timestamp=None, type=None, sub_type= None):
		self.coordx = coordx
		self.coordy = coordy
		self.id = id
		self.name = name
		self.timestamp = timestamp
		self.type = type
		self.sub_type = sub_type
	
		
class alarm(object):
	def __init__(self, id=None, name= None, timestamp=None, type= None, poi_id=None, contact_person= None, contact_number= None, extrainfo = None):
		self.id=id
		self.name = name
		self.timestamp = timestamp
		self.type = type
		self.poi_id=poi_id
		self.contact_person = contact_person
		self.contact_number = contact_number
		self.extrainfo = extrainfo

class unit(object):
	def __init__(self, coordx= None, coordy= None, id=None, name= None, timestamp=None, type= None):
		self.coordx = coordx
		self.coordy = coordy
		self.id = id
		self.name = name
		self.timestamp = timestamp
		self.type = type
		
metadata.create_all(engine)
mapper(Group, group_table)
mapper(poi, poi_table)
mapper(alarm, alarm_table)
mapper(unit, unit_table)

mapper(mission, mission_table, properties=dict(
	groups=relation(Group, secondary= mission_group, backref='missions'))
	)
mapper(User, user_table, properties=dict(
	groups=relation(Group, secondary= user_group, backref='users'))
	)

mapper(Item, items_table)

def generate_id():
	id+=1
	return id

def get_user_groups(namn):
	snubbe=session.query(User).filter_by(name=namn).first()
	return snubbe.groups
def get_group_users(namn):
	s=session.query(Group).filter_by(name=namn).first()
	return s.users
def get_group(namn):
	g=session.query(Group).filter_by(name=namn).first()
	return g

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


user_thor= User('thor', 'normal', 'gobject')
user_thor.groups.append(g)
user_thor.groups.append(go)


user_christopher=User('christopher', 'normal', '123')
user_christopher.groups.append(g)


user_hanna= User('hanna', 'normal', '123')
user_hanna.groups.append(g)


user_manuela=User('manuela', 'normal', '123')
user_manuela.groups.append(g)


user_kj=User('kj', 'normal', '123')
user_kj.groups.append(g)
user_kj.groups.append(pro)


def addMission(name1, timestamp1, type1, description1, contact_person1, contact_number1,status1,finishtime1):
	session.save(mission(name=name1, timestamp=timestamp1, type=type1, description=description1, contact_person=contact_person1, contact_number=contact_number1, status=status1, finishtime=finishtime1))


#mission_temp=mission(name=name, timestamp=datetime.now(), type="Rescue", description="Go and save a cat from a burning tree.", contact_person="Moma Cat", contact_number="123457678", status="Ongoing", finishtime= "4 hours")

addMission("Save the cat",datetime.now(),"Rescue","Go and save a cat from a burning tree.", "Moma Cat", "123457678","Ongoing","4 hours")	
	
	
def addMission_object(Object):
	session.save(Object)

addMission_object( mission(name="Save the chearleader", timestamp=datetime.now(), type="Assasinate", description="Go and save the chearleader, and assasinate Sylar.", status="Ongoing", finishtime= "30 min"))


##session.save(mission_1)
#session.save(mission_2)
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
