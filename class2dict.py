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
	    if(str(dict[elem]).startswith('<')):#bugg: man far inte borja ett meddelande med <
		    dict[elem] = class2dict(o.__dict__[elem])
    return dict