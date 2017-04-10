"""
F2 Database API
---------------

Definition of   F 2 _ H e l p e r s, 

several functions that a F2 connection provides. 

Th. Estier

version 1.2 - june 2005
   --
   written after the original Ada version from 1989-1990, Th. Estier, CUI Geneva.
"""
from sys import maxsize as sys_maxsize

from .f2_object import F2_Object, F2_Object_list, F2_NULL
from .f2_class  import theClass
from .f2_attribute import theAttribute

####################  F 2 _ H e l p e r  ####################

class F2_Helper:
    "an object provinding services to a F2 connection."

    def __init__(self, f2c):
        """constructor: remember on which F2 connection we work."""
        self.f2c = f2c
        
    def class_create(self, className, superClass=None, schema={}, database=None):
        """A syntactic shortcut for declaring classes. Example:
           db.class_create(className='Person', database=Mybase,
                           schema={'firstname': db.String,
                                   'lastname' : db.String,
                                   'work_in'  : db.Department})
           schema is a dictionary interpreted as a list of attributes for the class.
           If argument superClass is given, a sub-class is created.
           If argument database is given, the new created class is attached to db 'database',.
           For each attribute, cardinalities (min & max) may be precised in a tuple
           with the range (or rangeClass)
        """ 
        newC = theClass('TupleClass').create(className = className)
        if superClass:
            theClass('SubClass').enter(newC, superClass = superClass)
        if database:
            if isinstance(database, str):
                db_name = database
                database = self.f2c.Database(name=db_name)
                if not database:
                    database = self.f2c.Database.create(name=db_name)
                else:
                    database = database[0]
            newC.db = database
        else:
            newC.db = self.f2c.Kernel
        Attribute = theClass('Attribute')
        for attr_name, attr_vals in list(schema.items()):
            if isinstance(attr_vals, tuple):
                rangeC = attr_vals[0]
                if len(attr_vals) >= 2:
                    minCard = 0
                    maxCard = attr_vals[1]
                if len(attr_vals) >= 3:
                    minCard = maxCard
                    maxCard = attr_vals[2]
                if maxCard in ('n', 'N', '*'):
                    maxCard = sys_maxsize
            else:
                rangeC = attr_vals
                minCard = None
                maxCard = None
            n = Attribute.create(attributeName = attr_name,
                                 domainClass = newC,
                                 rangeClass = rangeC,
                                 visibility = 1)
            if minCard is not None:
                n.minCard = minCard
                n.maxCard = maxCard
        return newC
    
    def add_key(self, ofClass, *attributeNames):
        """A syntactic shortcut for adding a key to a CLASS, equivalent
           to creating an object in class Key. """
        assert ofClass.is_TupleClass(), "F2.add_key(): cannot add a key in class %s." % ofClass
        allClassAttributes = ofClass.all_attributes().attributeName
        keyAttrs = []
        for a in attributeNames:
            assert a in allClassAttributes, "F2.add_key(): bad attribute name: %s." % a
            keyAttrs.append(theAttribute(a, ofClass))
        newK = self.f2c.Key.create(ofClass=ofClass, keyAttrs=keyAttrs)
        return newK
    
    def json_repr(self, some_value, visited_objs=None, using=None, depth=1):
        """produce a JSON representation of some_value, which may
           be either a single F2_Object, or a F2_Object_list
           By default, render null values as empty strings '', to avoid '?'-clutters. """
        if not visited_objs:
            visited_objs = []
        if isinstance(some_value, list):
            res = [self.json_repr(o, visited_objs, using = using, depth = depth) for o in some_value]
            return '[' + ','.join(res) + ']'
        elif isinstance(some_value, F2_Object):
            if depth <= 0 or some_value in visited_objs or not some_value:
                if some_value:
                    return '"'+str(some_value)+'"'
                else:
                    return 'null'
            else:
                if using is None: using = []
                o_class = theClass(some_value)
                attr_list = [a.attributeName
                             for a in o_class.all_attributes()
                             if a.visibility == 1 and (a.attributeName in using or not using)]
                res = ['"'+aName+'":' + self.json_repr(getattr(some_value, aName), 
                                                           visited_objs+[some_value], 
                                                           using = using, 
                                                           depth = depth-1) for aName in attr_list]
                return '{' + ','.join(res) + '}'
        else: # some_value is an atomic (python) value: a string, an int, ... or '?'.
            if some_value != F2_NULL:
                if isinstance(some_value, str):
                    return '"' + some_value + '"'
                else:
                    return str(some_value)
            else:
                return 'null'
           

    def html_repr(self, some_value, visited_objs=None, using=None, depth=1):
        """produce a html representation of some_value, which may
           be either a single F2_Object, or a F2_Object_list
           By default, render null values as blanks, to avoid '?'-clutters. """
        if not visited_objs:
            visited_objs = []
        if isinstance(some_value, list):
            if len(some_value) == 0:
                return '[]'
            elif isinstance(some_value[0], F2_Object) and depth > 0:
                return self.html_table_repr(some_value, visited_objs+some_value, using, depth-1)
            else:
                res = '<table class="table table-striped table-hover">\n'
                for o in some_value:
                    res = res + '<tr><td>%s</td></tr>\n' % self.html_repr(o, 
                                                                          visited_objs+some_value,
                                                                          using = using,
                                                                          depth = depth-1)
                return res + '</table>\n'
        elif isinstance(some_value, F2_Object):
            if depth <= 0 or some_value in visited_objs or not some_value:
                if some_value:
                    return html_encode(str(some_value))
                else:
                    return " "
            else:
                return self.html_table_repr(F2_Object_list([some_value]), 
                                            visited_objs+[some_value], 
                                            using, 
                                            depth-1)
        else: # some_value is an atomic (python) value: a string, an int, ... or '?'.
            if some_value != '?':
                return html_encode(str(some_value))
            else:
                return " "
            
    def html_table_repr(self, value_list, visited_objs=None, using=None, depth=1):
        """produce a table representation of an (F2) object list. """
        if using is None: using = []
        o_class = theClass(value_list[0])
        attr_list = [(a.attributeName, a.rangeClass.className) 
                      for a in o_class.all_attributes() 
                      if a.visibility == 1 and (a.attributeName in using or not using)]
        res='<table class="table table-bordered">\n<tr>'
        for a,c in attr_list:
            res = res + '<th title="%s">%s</th>' % (c,a)
        for obj in value_list:
            res = res + '</tr>\n<tr>'
            for a,c in attr_list:
                res = res + '<td>%s</td>' % self.html_repr(getattr(obj, a),
                                                           visited_objs+[obj],
                                                           using = using,
                                                           depth = depth-1)
        return res + '</tr></table>\n'
        
# a common utility - could be replaced by a genuine python lib function
def html_encode(s):
    "html encodes strings with simple entities"
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

    