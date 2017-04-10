"""
F2 Database Interface
---------------------

Definition of class    F 2 _ O b j e c t, 

root of all python classes (meta or not meta, this distinction does not
hold really in F2, that's the secret !!)
Subclasses are F2_Class, F2_Attribute, F2_Keys, 
... and all user-defined subclasses.

Th. Estier
version 1.2 - june 2005
   --
   written after the original Ada version from 1989-1990, Th. Estier, CUI Geneva.
"""
from F2 import OFF
from F2 import metadict
F2_NULL = OFF.NULL_MARK

################   F 2 _ O b j e c t   #####################

class F2_Object:
    "a full F2 oid: (klass_oid, obj_oid)"

    def __init__(self, klass_oid, obj_oid):
        "an F2 Object is a pair (k,o) with o being an object of class k." 
        self._klass = klass_oid
        self._rank = obj_oid

    def __str__(self):
        "a nicely readable representation of an F2_Object (uses keys of classes whenever they exist)."
        try:
            return '<%s.%s>' % (OFF.className[self._klass], find_IDValue_of_object(self))
        except ClassKeyError:
            try:
                return '<%s.%s>' % (OFF.className[self._klass], self._rank)
            except:
                return '<?.?>'
        except:
            return '<?.?>'
    
    def __repr__(self):
        "same representation as str(), a variant below was tried for REST api."
        return str(self)
        
#     def __repr__(self):
#         "a canonical representation of an F2_Object"
#         try:
#             return '<%s.%s>' % (OFF.className[self._klass], self._rank)
#         except:
#             return '<?.?>'

    def __bool__(self):
        "tells that an F2 object is null or not, allows expressions like [if my_object: ]"
        return (self._klass != F2_NULL) and (self._rank != F2_NULL)

    def __eq__(self, other):
        "true if self and other denote the same object"
        if isinstance(other, str) and other == F2_NULL:
            return (self._rank == F2_NULL)
        elif self._rank == other._rank :
            return self._same_class_hierarchy(self._klass, other._klass)
        else:
            return False
            
    def __ne__(self, other):
        "not __eq__() , useful only for python2."
        return not self.__eq__(other)
        
    def __lt__(self, other):
        "true if rank is smaller, used to sort objects in a list, NULL is greater than any."
        if isinstance(other, str) and other == F2_NULL:
            return True
        elif self._same_class_hierarchy(self._klass, other._klass):
            return (self._rank < other._rank)
        else:
            return (self._klass < other._klass)

    def __hash__(self):
        "how to hash this things... well hash the tuple!"
        return hash((self._klass, self._rank))

    def __getattr__(self, name):
        "evaluates an attribute on an object, called when evaluating ' my_obj.name ' "
        if name[0] == '_':
            if name in ('_klass', '_rank'):
                return self.__dict__[name]
            elif name[1] == '_':
                # special methods and attributes starting with __ , and lookup failed.
                raise AttributeError
            else:
                return self._flat_getattr(name[1:])
        else:
            return self._getattr(name)

    def _flat_getattr(self, name):
        "like _getattr but flattens result (makes a difference for multi-valued attributes only)"
        res = list(set(self._getattr(name)))    # you know a shorter way ? pls tell me.
        if len(res) == 0:
            return []
        else:
            if isinstance(res[0], F2_Object):
                return F2_Object_list(res)
            else:
                return res

    def _getattr(self, name):
        "evaluates an attribute on an object, called when evaluating ' my_obj.name ' "
        attr = self._attribute_of(name, self._klass)
        domain = OFF.domainClass[attr]
        stateAttr = OFF.classStateAttr[domain]
        if OFF.db_root[stateAttr][self._rank] != F2_NULL:
            rangeC = OFF.rangeClass[attr]
            range_is_tupleClass = (OFF.stateTupleClass[rangeC] != F2_NULL)
            value = OFF.db_root[attr][self._rank]
            if range_is_tupleClass:
                if type(value) is list:
                    return F2_Object_list([theObject(rangeC, x) for x in value])
                else:
                    return theObject(rangeC, value)
            else:
                return value
        else:
            raise F2AttributeError('F2 attribute %s not applicable to this object (%s)' %(name, self))

    def __setattr__(self, name, value):
        "sets the value of an attribute"
        if name in ('_klass', '_rank'):
            # allow setting of python variable attributes (_klass and _rank)
            self.__dict__[name] = value
        else:
            previous_value = self._getattr(name)
            # Keys: this check is done only once bootstrap is over (during bootstrap, Keys do not exist yet)
            keyList = []
            if not OFF.db_root['F2_Signature']['bootstrap_is_ongoing']:
                from . import f2_key
                this_attr_F2 = theObject(metadict.Attribute, self._attribute_of(name, self._klass))
                keyList = f2_key.keysWithThisAttribute(this_attr_F2)
                for k in keyList:
                    objConflict = k.objectWithKeyConflict(self, this_attr_F2, value)
                    assert objConflict == self or objConflict == F2_NULL, \
                    "F2 ValueError: value %s for attribute %s would cause duplicate key." % (value, name)                   
            self.pre_assign(name, previous_value, value)
            self._assign(name, value, previous_value)
            self.post_assign(name, previous_value, value)
            # if keys are involved, update key index with this insertable_value (keyStore)
            if keyList:
                for k in keyList:
                    k.updateKeyTupleValue(self, this_attr_F2, value)

    def _assign(self, name, value, previous):
        "install in place a value for an object's attribute"
        this_attr = self._attribute_of(name, self._klass)
        rangeC = theObject(metadict.CLASS, OFF.rangeClass[this_attr])
        if isinstance(value, list):
            insertable_value = [self._validate(v, rangeC) for v in value]
            minCard = OFF.minCard[this_attr]
            if minCard != F2_NULL:
                assert minCard <= len(insertable_value), \
                "F2ValueError: value %s lower than minimum cardinality (=%d) of attribute %s." % (value, minCard, name)
            maxCard = OFF.maxCard[this_attr]
            if maxCard != F2_NULL :
                assert len(insertable_value) <= maxCard, \
                "F2ValueError: value %s greater than maximum cardinality (=%d) of attribute %s." % (value, maxCard, name)
        else:
            insertable_value = self._validate(value, rangeC)            
        # now do the update.
        if rangeC.is_TupleClass():
            if isinstance(previous, list):
                for v in previous:
                    if v: v.remove_reference()
            else:
                if previous and previous != F2_NULL: previous.remove_reference()
            if isinstance(insertable_value, list):
                for v in insertable_value:
                    if v != F2_NULL: F2_Object(rangeC._rank, v).add_reference()
            else:
                if insertable_value != F2_NULL: F2_Object(rangeC._rank, insertable_value).add_reference()
        attr_storage = OFF.db_root[this_attr]
        attr_storage[self._rank] = insertable_value
        OFF.db_root[this_attr] = attr_storage

    def _validate(self, value, in_range):
        "validate and transform value for class in_range"
        if in_range.is_AtomClass():
            if value == F2_NULL: return value # valid for any range.
            bType = OFF.baseType[in_range._rank]
            infVal = OFF.infValue[in_range._rank]
            supVal = OFF.supValue[in_range._rank]
            correct_range = ( bType==metadict.intType    and type(value) is int ) or \
                            ( bType==metadict.realType   and type(value) is float ) or \
                            ( bType==metadict.timeType   and type(value) is float ) or \
                            ( bType==metadict.stringType and type(value) is str )
            if correct_range:
                bounded = True
                if infVal != F2_NULL: bounded = infVal <= value
                if supVal != F2_NULL: bounded = bounded and (value <= supVal)
                if bounded:
                    return value
        else: # TupleClass
            if isinstance(value, F2_Object):
                value_range = theObject(metadict.CLASS, value._klass)
                if value_range.root() == in_range.root() and (value.exist_in(in_range)):
                    return value._rank
            elif value == F2_NULL:
                return value
        raise F2ValueError('F2_object.__setattr__(): illegal value %s for range %s.' % (value, in_range.className))

    def _root_of(self, c):
        "a short equivalent of F2_Class.root(), returns only rank, no consistency check."
        root_c = c
        while OFF.stateSubClass[root_c] != F2_NULL:
            root_c = OFF.superClass[root_c]
        return root_c

    def _same_class_hierarchy(self, left, right):
        "are left and right in same class hierarchy"
        return (left == right) or \
               (self._root_of(left) == self._root_of(right))

    def _is_a_class(self):
        "utility to check an object against class CLASS"
        return self._root_of(self._klass) == metadict.CLASS

    def _is_an_attribute(self):
        "utility to check an object against class CLASS"
        return self._klass == metadict.Attribute

    def _attribute_of(self, attrName, of_class):
        "utility: the attribute name resolution algorithm."
        attr_list = OFF.attributeName.find(attrName)                     # all attributes carrying this name
        attr_list = [(a, OFF.domainClass[a]) for a in attr_list]           # attrs with their domain class,
        attr_list = [(a, dom, self._root_of(dom))
                                           for a,dom in attr_list]     # attrs, with their root class.
        root_of_context = self._root_of(of_class)
        attr_list = [(a, orig, root) for a, orig, root in attr_list
                                     if root == root_of_context ]        # only those in same class tree.
        if attr_list:
            if len(attr_list) == 1: # not ambiguous, happens most of the time...
                return attr_list[0][0]
            else:
                # ambiguous: several candidates with same name in class tree, lets try to
                # solve ambiguity (standard overriding approach).
                lookup_class = of_class
                while True:
                    candidates = [a for a, orig, root in attr_list if orig == lookup_class]
                    if candidates:
                        if len(candidates) == 1:
                            return candidates[0]  # that's it.
                        else:
                            raise F2AttributeError('several attributes %s in class %s' % (attrName, OFF.className[lookup_class]))
                    if lookup_class == root_of_context: break # root reached, exit the loop
                    lookup_class = OFF.superClass[lookup_class]
                # no candidates were direct or inherited in this context. If some candidates remain, they
                # belong to the same class tree but not to the context (not to the direct line of inheritance)
                # and we know there are at least two of them: so there is no way to solve name ambiguity.
                raise F2AttributeError( 'attribute %s is ambiguous in class %s' % (attrName, OFF.className[of_class]))
        else:
            raise F2AttributeError('no F2 attribute %s in class %s' % (attrName, OFF.className[of_class]))

    def exist_in(self, in_class):
        """check object existence in class 'in_class'. (i.e. state != F2_NULL)
           in_class: checks existence in this (tuple-)class.
               In some rare cases, this parameter is directly the state
               attribute of class (used for optimization of safe cases
               in meta-level, internal usage only)"""
        assert isinstance(in_class, F2_Object), "f2_object.exist_in(): in_class must be a F2 object."
        if in_class._is_a_class():
            state_attr_rank = OFF.classStateAttr[in_class._rank]
        elif in_class._is_an_attribute():
            state_attr_rank = in_class._rank
        else:
            raise F2TypeError("can't determine object existence in context %s" % in_class)
        return (state_attr_rank != F2_NULL) and \
               (OFF.db_root[state_attr_rank][self._rank] != F2_NULL)

    def exist_object(self):
        """check object existence: whether its state value is non nul (i.e. != F2_NULL),
           existence is checked in the class designated by the 'klass' part of the object_oid"""
        state_attr_rank = OFF.classStateAttr[self._klass]
        return (state_attr_rank != F2_NULL) and \
               (OFF.db_root[state_attr_rank][self._rank] != F2_NULL)

    def add_reference(self, state_attribute=None):
        """increments object reference counter, for optional state_attribute see exist_object() """
        if isinstance(state_attribute, F2_Object) and state_attribute._is_an_attribute():
            state_attr_rank = state_attribute._rank
        else:
            state_attr_rank = OFF.classStateAttr[self._klass]
        state_function = OFF.db_root[state_attr_rank]
        state_function[self._rank] += 1

    def remove_reference(self, state_attribute=None):
        """decrements object reference counter, for optional state_attribute see exist_object() """
        if isinstance(state_attribute, F2_Object) and state_attribute._is_an_attribute():
            state_attr_rank = state_attribute._rank
        else:
            state_attr_rank = OFF.classStateAttr[self._klass]
        state_function = OFF.db_root[state_attr_rank]
        state = state_function[self._rank]
        if isinstance(state, int) and state > 0:   # state may be F2_NULL
            state_function[self._rank] = state - 1

    def current_reference(self, state_attribute=None):
        """returns current value of reference counter"""
        if isinstance(state_attribute, F2_Object) and state_attribute._is_an_attribute():
            state_attr_rank = state_attribute._rank
        else:
            state_attr_rank = OFF.classStateAttr[self._klass]
        return OFF.db_root[state_attr_rank][self._rank]

    ### Triggers - redefined in subclasses to handle pre et post conditions on F2 primitives.
    ### to be trigged, redefined triggers must belong to a registered python subclass of F2_Object.
    ### (see __RegisterPythonClass() )

    def pre_create(self, **attr_values):
        "redefinable trigger, called immediately BEFORE a new object is definitively created"
        pass

    def post_create(self, **attr_values):
        "redefinable trigger, called immediately AFTER a new object has been definitively created"
        pass

    def pre_enter(self, **attr_values):
        "redefinable trigger, called immediately BEFORE an object enters a sub_class"
        pass

    def post_enter(self, **attr_values):
        "redefinable trigger, called immediately AFTER an object enters a sub_class"
        pass

    def pre_leave(self):
        "redefinable trigger, called immediately BEFORE an object leaves a sub-class (or a class)"
        pass

    def post_leave(self, **old_attr_values):
        """redefinable trigger, called immediately AFTER an object leaves a sub-class (or a class).
           old_attr_values gives the dict of values it posessed just before being deleted.
           CAUTION: these values may have been affected by exit algorithm (cascades) since evaluated."""
        pass

    def pre_assign(self, name, old_val, new_val):
        "redefinable trigger, called immediately BEFORE an attribute assignment (update)"
        pass

    def post_assign(self, name, old_val, new_val):
        "redefinable trigger, called immediately AFTER an attribute assignment (update)"
        pass

################   F 2 _ O b j e c t _ l i s t   #####################

class F2_Object_list(list):
    """a list of F2_object's having exactly the same properties as standard lists
      + the ability to evaluate an attribute on all objects of the list.
    """
    def __getattr__(self, name):
        "evaluate attribute 'name' on each F2_Object of this list"
        if name in self.__dict__:
            return self.__dict__[name]
        elif name[0] == '_':
            return self._flat_getattr(name[1:])    # simulates the ._ pseudo operator...
        res = [item._getattr(name) for item in self if item != F2_NULL]
        if len(res) == 0:
            return []
        else:
            if isinstance(res[0], F2_Object):
                return F2_Object_list(res)
            else:
                return res

    def _flat_getattr(self, name):
        "like __getattr__ but flattens result (makes a difference for multi-valued attributes only)"
        raw_res = [item._getattr(name) for item in self]
        res = []
        for item in raw_res:
            if isinstance(item, list):
                res.extend(item)
            else:
                res.append(item)
        res = list(set(res))    # you know a shorter way ? pls tell me.
        if len(res) == 0:
            return []
        else:
            if isinstance(res[0], F2_Object):
                return F2_Object_list(res)
            else:
                return res


##################  F 2 _ E x c e p t i o n s #############################

class F2Error(Exception):
    "root of F2 exceptions"
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return repr(self.message)

class F2ValueError(F2Error):
    pass

class F2AttributeError(F2Error):
    pass

class F2TypeError(F2Error):
    pass

class NotUniqueError(F2Error):
    "Exception for F2 classes lookups, raised when ID_value is not unique."
    pass

class ClassDesignationError(F2Error):
    "Exception for class naming in expressions, raised mostly"
    pass

class ClassLookupError(F2Error):
    "Exception for key lookups, raised when lookup"
    pass

class ClassKeyError(F2Error):
    "Exception for keys usage in F2, raised when no applicable Key exists."
    pass

###################  F 2 _ C a s t e r  #########################
#
# 'caster' contains references to python classes which represents
# specific F2 classes. Any F2 object is always represented in python
# by class F2_Object(), or by a suitable subclass of F2_Object() if
# it exists. "suitable" means "determined by algorithm theObject()".
#
python_caster = { }

def _RegisterPythonClass(f2_class, Python_Klass):
    """f2_class may be either a class rank (int), or a class name (string),
       class names will be converted to class ranks immediately after db startup."""
    python_caster[f2_class] = Python_Klass

def theObject(klass_oid, obj_oid):    
    # F2 cast: fixes the correct python class, according to dictionary python_caster
    lookup_klass = klass_oid
    while True:
        if lookup_klass in python_caster:
            return python_caster[lookup_klass](klass_oid, obj_oid)
            break
        if OFF.stateSubClass[lookup_klass] == F2_NULL:
            break
        lookup_klass = OFF.superClass[lookup_klass]
    # by default, it will be an F2_Object
    return F2_Object(klass_oid, obj_oid)


##################  I D _ V a l u e s    #############################

# some helping Kernel objects (F2 classes and attributes) which we will define
# during their first usage.
classKey_rank = None
attrOfClass_rank = None
attrKeyAttrs_rank = None

def find_objects_by_IDValue( value_tuple, inClass ):
    """Returns object list from inClass designated by the given value_tuple.
       Dummy function redefined when class Key and module F2_Key elaborate."""
    return F2_Object_list([])

def find_IDValue_of_object( obj ):
    """Finds the value (or tuple of values) which may designate uniquely an object in its class.
       Dummy function redefined when class Key and module F2_Key elaborate."""
    global classKey_rank, attrOfClass_rank, attrKeyAttrs_rank

    if OFF.db_root['F2_Signature']['bootstrap_is_ongoing']:
        raise ClassKeyError("Can't determine this during bootstrap.")
    if not classKey_rank:
        # first time here after bootstrap: elaborate useful F2 values for later.
        classKey_rank = OFF.className.find('Key')[0]
        attrOfClass_rank = [a for a in OFF.attributeName.find('ofClass') if OFF.domainClass[a] == classKey_rank][0]
        attrKeyAttrs_rank = [a for a in OFF.attributeName.find('keyAttrs') if OFF.domainClass[a] == classKey_rank][0]

    c = obj._klass
    candidateKeys = OFF.db_root[attrOfClass_rank].find(c)
    while OFF.stateSubClass[c] != F2_NULL:         # a loop to get inherited keys too.
        c = OFF.superClass[c]
        candidateKeys += OFF.db_root[attrOfClass_rank].find(c)
    if len(candidateKeys) == 0:
        raise ClassKeyError("The class of this F2 object has no key.")
    else:
        firstKey = candidateKeys[0]
        idAttributes = OFF.db_root[attrKeyAttrs_rank][firstKey]
        if type(idAttributes) is list:
            id_value = '_'.join([str(OFF.db_root[a][obj._rank]) for a in idAttributes])
        else:
            id_value = str(OFF.db_root[idAttributes][obj._rank])
        return id_value


