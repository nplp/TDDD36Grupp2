

def generate_id():
	id_nr=get_last_id()
	id_nr+=1
	add_last_id(id_nr)
	idn=(id_nr*10)+2
	return idn 
 
#for att genereringsfunktionen ska fungera
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
	sessionTemp = Session()
	sessionTemp.save(Message(sender=sender1, receiver=receiver1, type=type1, subtype=subtype1, time_created=time_created1, subject=subject1, message=message1, response_to=response_to1))
	sessionTemp.commit()
	
	
	

def getMessage(id_nr):
	try:
		m=session.query(Message).filter_by(id=id_nr).first()
		return m
	except:
		return None
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