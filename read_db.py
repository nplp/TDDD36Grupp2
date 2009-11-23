# Read database
# coding:utf-8
# Ovanst√•ende rad √§r ISO-kodning f√∂r att √•√§√∂ ska funka.

from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine('sqlite:///data.db', echo=False)
metadata = MetaData()

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



############################Metoder###########################

def get_user_groups(namn):
	try:
		snubbe=session.query(User).filter_by(name=namn).first()
		return snubbe.groups
	except:
		return None
def get_group_users(namn):
	try:	
		s=session.query(Group).filter_by(name=namn).first()
		return s.users
	except:
		return None
def get_group(namn):
	try:
		g=session.query(Group).filter_by(name=namn).first()
		return g
	except:
		return None
def getCount(namn):
	try:
		return session.query(Item).filter_by(name=namn).first().count
	except:
		return None
# Retunerar totala antalet av ett object
def getTotal(namn):	
	try:	
		temp=0
		for item in session.query(Item).filter_by(name=namn):
			temp = item.count + temp
		return temp
	except:
		return None
def get_mission_object_by_name(namn):
	try:
		m=session.query(mission).filter_by(name=namn).first()
		return m
	except:
		return None

def get_mission_by_id(id_nr):
	try:
		m=session.query(mission).filter_by(id=id_nr).first()
		return m
	except:
		return None

def delete_group(namn):
	try:
		session.delete(get_group(namn))
	except:
		pass
	
def delete_group_user(group,namn):
	try:
		session.delete(get_group(group).filter_by(name=namn))
	except:
		pass
	
def get_password(namn):
	try:
		p=session.query(User).filter_by(name=namn).first()
		return p.password
	except:
		return None
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
	
def addMission(name1, timestamp1, type1, description1, contact_person1, contact_number1,status1,finishtime1):
	session.save(mission(name=name1, timestamp=timestamp1, type=type1, description=description1, contact_person=contact_person1, contact_number=contact_number1, status=status1, finishtime=finishtime1))	
	
def get_mission_all(namn):
	m= get_mission_object_by_name(namn)
	return m.name, m.timestamp, m.type, m.description, m.contact_person, m.contact_number, m.status, m.finishtime
#######################################################	
session = Session()
USERS = session.query(User).all()
session.close()


###########################SpÂrutskrifter############################	

session = Session()



#skriver ut valda delar av ett uppdrag
m= get_mission_object_by_name('Save the cat')
print "get_mission_by_name:"
print m.name
print m.description
print m.id
print m.type
print is_user('mathias')
m = get_mission_by_id(2)
print m.name
print m.description
print m.id
print m.type
# skriver ut allt som finns i ett uppdrag
print get_mission_all('Save the cat')
	

print "anv‰ndare som ‰r i: team2 ", get_group_users('team2')
print "anv‰ndare som ‰r i: teamgobject", get_group_users('teamgobject')
print "grupper som niklas ‰r med i", get_user_groups('niklas')
print "grupper som Mathias ‰r med i", get_user_groups('mathias')
print "grupp som inte finns:", get_group('finns inte')
print "mathias losen", get_password('mathias')
print "alla anvandare", session.query(User).all()

print 'antalet EMP', getCount('EMP')
print "totalt antal EMP",getTotal('EMP')
#query.filter(User.name.in_(session.query(User.name).filter(User.name.like('%ed%')))) 
print "item Pansarvagn: ",session.query(Item).filter_by(name='Pansarvagn').first()
print "en anvandare som inte finns: ", session.query(User).filter_by(name ='m').first()
user= session.query(User).filter_by(name ='matas').first()
try:
	print user.name
except Exception,e :
	pass
session.commit()


print "Skriver ut team2 ", get_group('team2')
print "skriver ut anvandare i team2",get_group_users('team2')
delete_group('team2')
print "skriver ut team2 efter borttagning ",get_group('team2')
print "skriver ut anvandare i team2",get_group_users('team2')

session.commit()

#####################################################################






















