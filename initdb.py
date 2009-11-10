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

users_table = Table('users_table', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(40)),
	Column('clearance', String(40)),
	Column('group', String(20)),
	Column('password', String(20))
	)
items_table = Table('items_table', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(40)),
	Column('count', Integer),
	Column('location', String(40))
	)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
class User(object):
	def __init__(self, name=None, clearance=None, group=None, password=None):
		self.name=name
		self.clearance=clearance
		self.group=group
		self.password=password
	def __repr__(self):
		return "<User('%s','%s','%s', '%s')>" % (self.name, self.clearance, self.group, self.password)
class Item(object):
	def __init__(self, name=None, count=None, location=None):
		self.name=name
		self.count=count
		self.location=location
	def __repr__(self):
		return "<Item('%s','%s', '%s')>" % (self.name, self.count, self.location)

metadata.create_all(engine)
mapper(User, users_table)
mapper(Item, items_table)

user_niklas = User('niklas', 'normal','stabspluton', '123')
session.save(User('mathias', 'normal','stabspluton', '123'))
session.save(User('thor', 'normal','stabspluton', '123'))
session.save(User('chrille', 'normal','stabspluton', '123'))
session.save(User('hanna', 'normal','stabspluton', '123'))
session.save(User('manuela', 'normal','stabspluton', '123'))
session.save(User('kj', 'normal','stabspluton', '123'))
session.save(User('ADMIN', 'normal','administrator', '123'))
session.save(user_niklas)
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
