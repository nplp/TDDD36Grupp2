# coding:utf-8
import os

#from sqlalchemy.orm import mapper
#from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.orm import *

os.system("rm data.db")
db = create_engine('sqlite:///data.db')
metadata = MetaData(db)

users = Table('users', metadata)
session = create_session()

class User(object):
	def __init__(self, name=None, clearance=None, password=None):
		self.name=name
		self.clearance=clearance
		self.password=password	
	def __repr__(self):
		return self.name

	
user_mapper=mapper(User, users)

left_table = Table('left', metadata,
    Column('id', Integer, primary_key=True))

right_table = Table('right', metadata,
    Column('id', Integer, primary_key=True))

association_table = Table('association', metadata,
    Column('left_id', Integer, ForeignKey('left.id'), primary_key=True),
    Column('right_id', Integer, ForeignKey('right.id'), primary_key=True),
    Column('data', String(50))
    )

mapper(Parent, left_table, properties={
    'children':relation(Association)
})

mapper(Association, association_table, properties={
    'child':relation(Child)
})

mapper(Child, right_table)



mapper(Parent, left_table, properties={
    'children':relation(Association, backref="parent")
})

mapper(Association, association_table, properties={
    'child':relation(Child, backref="parent_assocs")
})

mapper(Child, right_table)



# create parent, append a child via association
p = Parent()
a = Association()
a.child = Child()
p.children.append(a)

# iterate through child objects via association, including association
# attributes
for assoc in p.children:
    print assoc.data
    print assoc.child




#mathias = User('Mathias', 'Normal', '123')
#mathias =session.query(User).selectfirst(user_table.c.name=='Mathias')
#print mathias
#mathias.password ='123'
#session.flush()

#session.save(mathias)
#print "Just called save(). Now flush() will actually do something."
#session.flush()















"""
anvandare = Table('anvandare', metadata,
    Column('anvandar_ID', Integer, primary_key=True),
    Column('namn', String(40)),
    Column('losenord', String(40)),
    Column('position', String(40)),
    Column('behorighet', String(40))
)
anvandare.create()
i=anvandare.insert()
i.execute({'namn': 'Mathias', 'losenord': '123', 'position': 'Norrkoping', 'behorighet': 'secret'},
	  {'namn': 'KJ', 'losenord': '123', 'position': 'Linkoping', 'behorighet': 'classified'},
       	  {'namn': 'Thor', 'losenord': '123', 'position': 'Baljan', 'behorighet': 'secret'},
	  {'namn': 'Niklas', 'losenord': '123', 'position': 'Linkoping', 'behorighet': 'topSecret'},
	  {'namn': 'Christopher', 'losenord': '123', 'position': 'Linkoping', 'behorighet': 'secret'},
	  {'namn': 'Hanna', 'losenord': '123', 'position': 'Linkoping', 'behorighet': 'secret'},
       	  {'namn': 'Manuella', 'losenord': '123', 'position': 'Linkoping', 'behorighet': 'secret'})



def findUser(user):
    for row in anvandare.select(anvandare.c.namn == user).execute():
       return row.namn


def checkPwd(user):
    for row in anvandare.select(anvandare.c.namn == user).execute():
	return row.losenord


	def authentication(self):
		CLIENTNAME = "Player1"
		try:
			while 1:
				self.socket.send("Type a name: ")
				CLIENTNAME = self.socket.recv(BUFF)
				if(search(CLIENTNAME) == -1 and CLIENTNAME == findUser(CLIENTNAME)):
					self.socket.send("Type your password: " + CLIENTNAME)
					if(self.socket.recv(BUFF) + "\n" == checkPwd(CLIENTNAME)):
						self.name = CLIENTNAME
						#kollar att det inte finns någon med namnet CLIENTNAME. Funkar ej.
						if(search(CLIENTNAME) != -1):
							return CLIENTNAME
		except Exception, e:
			print "Client lost"	
		return ""
# This will return more results than you are probably expecting.
"""



"""
items = Table('items', metadata,
    Column('item_ID', Integer, primary_key=True),
    Column('namn', String(40)),
    Column('antal', Integer),
    Column('position', String(40)),
    
)
items.create()
i=items.insert()
i.execute({'namn': 'Pansarvagn', 'antal': 14, 'position': 'Norrkoping'},
	  {'namn': 'El-verk', 'antal': 123, 'position': 'Linkoping'},
       	  {'namn': 'El-verk', 'antal': 2, 'position': 'Valla'},
	  {'namn': 'El-verk', 'antal': 1, 'position': 'Ryd'},
	  {'namn': 'El-verk', 'antal': 13, 'position': 'Motala'},
	  {'namn': 'EMP', 'antal': 1, 'position': 'Linkoping'},
       	  {'namn': 'Fifa 2009', 'antal': 1, 'position': 'Niklas'},)
#s = select([func.count("*")], from_obj=[items])
#s = select([func.count(users.c.user_id)])	
def countTotaltAntal(namnet):
    for row in items.select(items.c.namn == namnet).execute():
	return row.antal

print countTotaltAntal('El-verk')		
"""
"""	
CLIENTNAME = raw_input("Enter name: ")
if(CLIENTNAME == findUser(CLIENTNAME)):
	#self.socket.send("Type your password: " + CLIENTNAME)
	print checkPwd(CLIENTNAME)
	CLIENTPW=raw_input("Enter pw: ")
	if(checkPwd(CLIENTNAME) == CLIENTPW):
"""
		
