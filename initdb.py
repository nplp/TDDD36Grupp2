# coding:utf-8
#from sqlalchemy.orm import mapper
#from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.orm import *
import os
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
	
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
	
class User(object):
	
	#def _get_password(self):
		#return self.password
	#def _set_password(self, value):
		#self.password= sha.new(value).hexdigest()
		#password=property(_get_password, _set_password)
	#def password_matches(self, password):
		#return sha.new(password).hexdigest()==self.password


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

metadata.create_all(engine)
mapper(Group, group_table)

mapper(User, user_table, properties=dict(
	_password=user_table.c.password,
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

#user2.groups.append(group2)

#skapar niklas
user_niklas=User()
user_niklas.name='Niklas'
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

user_mathias= User(name='Mathias', clearance='normal', password='123')
user_mathias.groups.append(pro)
user_mathias.groups.append(go)


user_thor= User('Thor', 'normal', 'gobject')
user_thor.groups.append(g)
user_thor.groups.append(go)


user_christopher=User('Christopher', 'normal', '123')
user_christopher.groups.append(g)


user_hanna= User('Hanna', 'normal', '123')
user_hanna.groups.append(g)


user_manuela=User('Manuela', 'normal', '123')
user_manuela.groups.append(g)


user_kj=User('KJ', 'normal', '123')
user_kj.groups.append(g)
user_kj.groups.append(pro)


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
#print get_user_groups('Niklas')
#print "skriver ut grupper som Mathias är med i"
#print get_user_groups('Mathias')
#print "skriver ut grupp som inte finns"
#print get_group('finns inte')
