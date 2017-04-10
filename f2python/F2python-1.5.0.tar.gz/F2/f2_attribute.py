"""
F2 Database Interface
---------------------

Definition of class    F 2 _ A t t r i b u t e, 

Th. Estier
version 1.2 - june 2005
   --
   written after the original Ada version from 1989-1990, Th. Estier, CUI Geneva.
"""
from . import OFF, metadict
from . import f2_object, f2_class
F2_Object = f2_object.F2_Object
F2_Class = f2_class.F2_Class
theClass = f2_class.theClass


class F2_Attribute(F2_Object):
    "an F2 object belonging to class ATTRIBUTE hierarchy"

    def __str__(self):
        return '<%s.%s>' % (OFF.className[self._klass], OFF.attributeName[self._rank])

    def set_reverse_function(self):
        "force OFF storage to manage also the reverse function mapping of this attribute"
        OFF.db_root[self._rank].set_reverse()

    def post_create(self, **attr_values):
        "action trigged directly after creation of a new F2 Attribute: allocate an OFF storage."
        a = OFF.AttributeStorage( self._rank )

    def post_leave(self, **old_attr_values):
        "action trigged directly after deletion of an F2 Attribute: release OFF storage."
        OFF.db_root[self._rank].__release__()

    def pre_assign(self, name, old_val, new_val):
        "called immediately BEFORE an update on an Attribute"
        if name == 'attributeName':
            # normally a benign change, except if this is on an attribute of the Kernel.
            if self.domainClass.db and self.domainClass.db.name == 'Kernel':
                raise f2_object.F2AttributeError( "Cannot change the name of a Kernel's attribute, bootstrap needed.")
        elif name == 'rangeClass':
            self.rangeClass_change_check(from_rangeClass=old_val, to_rangeClass=new_val)
        elif name == 'domainClass':
            raise f2_object.F2AttributeError( "Cannot change the (domain)class of an attribute.")

    def post_assign(self, name, old_val, new_val):
        "called immediately AFTER an update on an Attribute"
        if name == 'rangeClass':
            self.rangeClass_change_apply(from_rangeClass=old_val, to_rangeClass=new_val)

    def rangeClass_change_check(self, from_rangeClass, to_rangeClass):
        "about to change the rangeClass of an attribute, check this is possible."
        # 1) check the change remain in the same class tree.
        pass

    def rangeClass_change_apply(self, from_rangeClass, to_rangeClass):
        "the rangeClass of an attribute changed, apply change on data."
        pass

############## theAttribute ############
def theAttribute(attr_designator, of_class=None):
	"""F2_Attribute maker takes 2 forms:"""
	if type(attr_designator) is str:
		if of_class:
			if not isinstance(of_class, F2_Object):
				of_class = theClass(of_class)
			this_attr = of_class._attribute_of(attr_designator, of_class._rank)
			return F2_Attribute(metadict.Attribute, this_attr)
		else:
			raise f2_object.F2AttributeError('no class specified for attribute %s.' % attr_designator)
	elif type(attr_designator) is int:
		return F2_Attribute(metadict.Attribute, attr_designator)
	else:
		raise f2_object.F2TypeError('no F2 Attribute designated by type %s.' % type(attr_designator))


f2_object._RegisterPythonClass(metadict.Attribute, F2_Attribute)

