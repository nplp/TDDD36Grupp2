# coding:utf-8
#from sqlalchemy.orm import mapper
#from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.orm import *
import os
from datetime import *
engine = create_engine('sqlite:///data.db', echo=False)
metadata = MetaData()
#genererar ett unikt id åt varje objekt (mission, alarm, poi, unit)
def generate_id():
	id+=1
	return id

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
	Column('timestamp', Float),
	Column('contact_person', String(50)),
	Column('contact_number', String(50)),
	Column('type', String(50)),
	Column('subtype', String(50)),
	Column('description', Text()),
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

def get_user_groups(namn):
	snubbe=session.query(User).filter_by(name=namn).first()
	return snubbe.groups
def get_group_users(namn):
	s=session.query(Group).filter_by(name=namn).first()
	return s.users
def get_group(namn):
	g=session.query(Group).filter_by(name=namn).first()
	return g
def getCount(namn):
	return session.query(Item).filter_by(name=namn).first().count

# Retunerar totala antalet av ett object
def getTotal(namn):	
	temp=0
	for item in session.query(Item).filter_by(name=namn):
		temp = item.count + temp
	return temp
#user2.groups.append(group2)
m= mission()
m.title = 'Bombdad'
m.body= 'en cyckel parkering ar sprangd bygg en ny cyckel parkering'
m.time='kl 15:00 den 11 november 2009'
m.location ='Linkoping'

g=get_group('team2')

#print get_group_users('team2')
m.groups.append(g)

#print get_group_users(m.groups[0])
print m.groups[0]

print m.title
print m.body
print m.time
print m.location

print "skriver ut användare som är i: team2 "
print get_group_users('team2')
print "skriver ut användare som är i: teamgobject"
print get_group_users('teamgobject')
print "skriver ut grupper som niklas är med i"
print get_user_groups('Niklas')
print "skriver ut grupper som Mathias är med i"
print get_user_groups('Mathias')
print "skriver ut grupp som inte finns"
print get_group('finns inte')




print getCount('EMP')
print getTotal('EMP')

print session.query(Item).filter_by(name='Pansarvagn').first()












