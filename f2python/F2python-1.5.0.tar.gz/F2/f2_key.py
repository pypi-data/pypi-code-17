"""
F2 Database Interface
---------------------

Definition of class    F 2 _ K e y , 

Th. Estier
version 1.4 - jan 2017
   --
   written after the original Ada version from 1989-1990, Th. Estier, CUI Geneva.
"""
from . import f2_object
F2_Object = f2_object.F2_Object
F2_Object_list = f2_object.F2_Object_list
theObject = f2_object.theObject
F2_NULL = f2_object.F2_NULL
_RegisterPythonClass = f2_object._RegisterPythonClass
from . import f2_class
theClass = f2_class.theClass
from . import f2_attribute
theAttribute = f2_attribute.theAttribute
from . import f2_database
theDatabase = f2_database.theDatabase

from . import OFF
from persistent import Persistent
from BTrees.OOBTree import OOBTree

class F2_Key(F2_Object):
    "an F2 oid for a 'Kernel.Key' object."
    
    def keyStore(self):
        "get my persistent keystore"
        return OFF.db_root[self._rank]
    
    def checkAttrValInKey(self, attr_values):
        "check that this combination of attribute values is not already used for this key"
        f2K, keyAttrs, ofClass = currentClassKeySchema()
        allKeyAttrs = OFF.db_root[keyAttrs._rank][self._rank]
        ks = self.keyStore()
        if not isinstance(allKeyAttrs, list):
            # cool, its a simple key
            attrName = OFF.attributeName[allKeyAttrs]
            if attrName in attr_values:
                nv = nakedValue(attr_values[attrName])
                rankWithThisKeyVal = ks[(nv,)]
            else:
                rankWithThisKeyVal = None
        else:
            # well, a composite key, a bit more complicated...
            values = []
            for ka in allKeyAttrs:
                attrName = OFF.attributeName[ka]
                if attrName in attr_values:
                    nv = nakedValue(attr_values[attrName])
                    values.append(nv)
            rankWithThisKeyVal = ks[tuple(values)]
        return rankWithThisKeyVal is None
    
    def pushValuesInKey(self, attr_values, obj):
        "store a tuple values in this key keystore"
        f2K, keyAttrs, ofClass = currentClassKeySchema()
        allKeyAttrs = OFF.db_root[keyAttrs._rank][self._rank]
        ks = self.keyStore()
        if not isinstance(allKeyAttrs, list):
            # cool, its a simple key
            attrName = OFF.attributeName[allKeyAttrs]
            if attrName in attr_values:
                ks[(attr_values[attrName],)] = obj._rank
        else:
            # well, a composite key, a bit more complicated...
            values = []
            for ka in allKeyAttrs:
                attrName = OFF.attributeName[ka]
                if attrName in attr_values:
                    values.append(nakedValue(attr_values[attrName]))
            if len(values) == len(allKeyAttrs):
                # cool: we have all values for this key
                ks[tuple(values)] = obj._rank
        OFF.db_root[self._rank] = ks
        
    def objectWithKeyConflict(self, obj, attr, value):
        "find objects o with keys having attr with o.attr = insertable_value"
        insertable_value = nakedValue(value)
        f2K, keyAttrs, ofClass = currentClassKeySchema()
        allKeyAttrs = OFF.db_root[keyAttrs._rank][self._rank]
        ks = self.keyStore()
        if not isinstance(allKeyAttrs, list):
            # cool, its a simple key
            rankWithThisKeyVal = ks[(insertable_value,)]
        else:
            # well, a composite key, its a bit more complicated...
            values = []
            for ka in allKeyAttrs:
                if ka == attr._rank:
                    values.append(insertable_value)
                else:
                    values.append(OFF.db_root[ka][obj._rank])
            rankWithThisKeyVal = ks[tuple(values)]
        if rankWithThisKeyVal:
            return theObject(obj._klass, rankWithThisKeyVal)
        else:
            return F2_NULL
    
    def updateKeyTupleValue(self, obj, attr, value):
        "store an updated key value. we know its ok, conflict have been detected before"
        insertable_value = nakedValue(value)
        f2K, keyAttrs, ofClass = currentClassKeySchema()
        allKeyAttrs = OFF.db_root[keyAttrs._rank][self._rank]
        ks = self.keyStore()
        if not isinstance(allKeyAttrs, list):
            # cool, its a simple key
            ks[(insertable_value,)] = obj._rank
        else:
            # well, a composite key, its a bit more complicated...
            values = []
            for ka in allKeyAttrs:
                if ka == attr._rank:
                    values.append(insertable_value)
                else:
                    values.append(OFF.db_root[ka][obj._rank])
            ks[tuple(values)] = obj._rank
        OFF.db_root[self._rank] = ks

    def post_create(self, **attr_values):
        "Ensure the set of attributes of this key owns an index"
        ks = KeyStorage(self._rank)
        # rebuild this keyStore using existing objects
        ofClass = attr_values['ofClass']
        keyAttrs = attr_values['keyAttrs']
        for obj in ofClass():
            if isinstance(keyAttrs, list):
                keyStoreTuple = tuple([nakedValue(getattr(obj, a.attributeName, F2_NULL))
                                       for a in keyAttrs])
            else:
                keyStoreTuple = (nakedValue(getattr(obj, keyAttrs.attributeName)), )
            ks[keyStoreTuple] = obj._rank
        OFF.db_root[self._rank] = ks
        
        
        
classKey = None
attrKeyAttrs = None
attrOfClass = None

def currentClassKeySchema():
    global classKey, attrKeyAttrs, attrOfClass
    if not classKey:
        classKey = theClass('Key', theDatabase('Kernel'))
        attrKeyAttrs = theAttribute('keyAttrs', classKey)
        attrOfClass = theAttribute('ofClass', classKey)
    return (classKey, attrKeyAttrs, attrOfClass)

def keysWithThisAttribute(attr):
    "return keys with attr participating (or being that) key"
    f2K, keyAttrs, ofClass = currentClassKeySchema()
    candidate_keys = [theObject(f2K._rank, k) for k in OFF.db_root[keyAttrs._rank].find(attr._rank)]
    return [k for k in candidate_keys if k.exist_in(f2K)]

def keysOfThisClass(cl):
    "return keys of this class"
    f2K, keyAttrs, ofClass = currentClassKeySchema()
    candidate_keys = [theObject(f2K._rank, k) for k in OFF.db_root[ofClass._rank].find(cl._rank)]
    return [k for k in candidate_keys if k.exist_in(f2K)]
    
def nakedValue(value):
    "from an arbitrary list of F2 values, make a simple value (keyable)"
    if isinstance(value, F2_Object_list):
        return [v._rank for v in value]
    elif isinstance(value, F2_Object):
        return value._rank
    else:
        return value

class KeyStorage(Persistent):
    "a storage for the index added to a key"
    def __init__(self, key_id):
        self.key_id = key_id
        self.keystore = OOBTree()
        OFF.db_root[key_id] = self
    
    def __getitem__(self, key):
        try:
            return self.keystore[key]
        except:
            return
    
    def __setitem__(self, key, value):
        self.keystore[key] = value
    
_RegisterPythonClass('Key', F2_Key)
