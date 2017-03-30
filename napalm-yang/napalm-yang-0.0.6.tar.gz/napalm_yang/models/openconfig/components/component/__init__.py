
from operator import attrgetter
from pyangbind.lib.yangtypes import RestrictedPrecisionDecimalType, RestrictedClassType, TypedListType
from pyangbind.lib.yangtypes import YANGBool, YANGListType, YANGDynClass, ReferenceType
from pyangbind.lib.base import PybindBase
from decimal import Decimal
from bitarray import bitarray
import __builtin__
import config
import state
import properties
import subcomponents
import transceiver
class component(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-platform - based on the path /components/component. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: List of components, keyed by component name.
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__name','__config','__state','__properties','__subcomponents','__transceiver',)

  _yang_name = 'component'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__name = YANGDynClass(base=unicode, is_leaf=True, yang_name="name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, is_keyval=True, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='leafref', is_config=True)
    self.__subcomponents = YANGDynClass(base=subcomponents.subcomponents, is_container='container', yang_name="subcomponents", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)
    self.__transceiver = YANGDynClass(base=transceiver.transceiver, is_container='container', yang_name="transceiver", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform/transceiver', defining_module='openconfig-platform-transceiver', yang_type='container', is_config=True)
    self.__state = YANGDynClass(base=state.state, is_container='container', yang_name="state", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)
    self.__config = YANGDynClass(base=config.config, is_container='container', yang_name="config", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)
    self.__properties = YANGDynClass(base=properties.properties, is_container='container', yang_name="properties", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)

    load = kwargs.pop("load", None)
    if args:
      if len(args) > 1:
        raise TypeError("cannot create a YANG container with >1 argument")
      all_attr = True
      for e in self._pyangbind_elements:
        if not hasattr(args[0], e):
          all_attr = False
          break
      if not all_attr:
        raise ValueError("Supplied object did not have the correct attributes")
      for e in self._pyangbind_elements:
        nobj = getattr(args[0], e)
        if nobj._changed() is False:
          continue
        setmethod = getattr(self, "_set_%s" % e)
        if load is None:
          setmethod(getattr(args[0], e))
        else:
          setmethod(getattr(args[0], e), load=load)

  def _path(self):
    if hasattr(self, "_parent"):
      return self._parent._path()+[self._yang_name]
    else:
      return [u'components', u'component']

  def _get_name(self):
    """
    Getter method for name, mapped from YANG variable /components/component/name (leafref)

    YANG Description: References the component name
    """
    return self.__name
      
  def _set_name(self, v, load=False):
    """
    Setter method for name, mapped from YANG variable /components/component/name (leafref)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_name is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_name() directly.

    YANG Description: References the component name
    """
    parent = getattr(self, "_parent", None)
    if parent is not None and load is False:
      raise AttributeError("Cannot set keys directly when" +
                             " within an instantiated list")

    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=unicode, is_leaf=True, yang_name="name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, is_keyval=True, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='leafref', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """name must be of a type compatible with leafref""",
          'defined-type': "leafref",
          'generated-type': """YANGDynClass(base=unicode, is_leaf=True, yang_name="name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, is_keyval=True, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='leafref', is_config=True)""",
        })

    self.__name = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_name(self):
    self.__name = YANGDynClass(base=unicode, is_leaf=True, yang_name="name", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, is_keyval=True, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='leafref', is_config=True)


  def _get_config(self):
    """
    Getter method for config, mapped from YANG variable /components/component/config (container)

    YANG Description: Configuration data for each component
    """
    return self.__config
      
  def _set_config(self, v, load=False):
    """
    Setter method for config, mapped from YANG variable /components/component/config (container)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_config is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_config() directly.

    YANG Description: Configuration data for each component
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=config.config, is_container='container', yang_name="config", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """config must be of a type compatible with container""",
          'defined-type': "container",
          'generated-type': """YANGDynClass(base=config.config, is_container='container', yang_name="config", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)""",
        })

    self.__config = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_config(self):
    self.__config = YANGDynClass(base=config.config, is_container='container', yang_name="config", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)


  def _get_state(self):
    """
    Getter method for state, mapped from YANG variable /components/component/state (container)

    YANG Description: Operational state data for each component
    """
    return self.__state
      
  def _set_state(self, v, load=False):
    """
    Setter method for state, mapped from YANG variable /components/component/state (container)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_state is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_state() directly.

    YANG Description: Operational state data for each component
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=state.state, is_container='container', yang_name="state", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """state must be of a type compatible with container""",
          'defined-type': "container",
          'generated-type': """YANGDynClass(base=state.state, is_container='container', yang_name="state", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)""",
        })

    self.__state = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_state(self):
    self.__state = YANGDynClass(base=state.state, is_container='container', yang_name="state", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)


  def _get_properties(self):
    """
    Getter method for properties, mapped from YANG variable /components/component/properties (container)

    YANG Description: Enclosing container 
    """
    return self.__properties
      
  def _set_properties(self, v, load=False):
    """
    Setter method for properties, mapped from YANG variable /components/component/properties (container)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_properties is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_properties() directly.

    YANG Description: Enclosing container 
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=properties.properties, is_container='container', yang_name="properties", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """properties must be of a type compatible with container""",
          'defined-type': "container",
          'generated-type': """YANGDynClass(base=properties.properties, is_container='container', yang_name="properties", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)""",
        })

    self.__properties = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_properties(self):
    self.__properties = YANGDynClass(base=properties.properties, is_container='container', yang_name="properties", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)


  def _get_subcomponents(self):
    """
    Getter method for subcomponents, mapped from YANG variable /components/component/subcomponents (container)

    YANG Description: Enclosing container for subcomponent references
    """
    return self.__subcomponents
      
  def _set_subcomponents(self, v, load=False):
    """
    Setter method for subcomponents, mapped from YANG variable /components/component/subcomponents (container)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_subcomponents is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_subcomponents() directly.

    YANG Description: Enclosing container for subcomponent references
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=subcomponents.subcomponents, is_container='container', yang_name="subcomponents", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """subcomponents must be of a type compatible with container""",
          'defined-type': "container",
          'generated-type': """YANGDynClass(base=subcomponents.subcomponents, is_container='container', yang_name="subcomponents", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)""",
        })

    self.__subcomponents = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_subcomponents(self):
    self.__subcomponents = YANGDynClass(base=subcomponents.subcomponents, is_container='container', yang_name="subcomponents", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform', defining_module='openconfig-platform', yang_type='container', is_config=True)


  def _get_transceiver(self):
    """
    Getter method for transceiver, mapped from YANG variable /components/component/transceiver (container)

    YANG Description: Top-level container for client port transceiver data
    """
    return self.__transceiver
      
  def _set_transceiver(self, v, load=False):
    """
    Setter method for transceiver, mapped from YANG variable /components/component/transceiver (container)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_transceiver is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_transceiver() directly.

    YANG Description: Top-level container for client port transceiver data
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=transceiver.transceiver, is_container='container', yang_name="transceiver", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform/transceiver', defining_module='openconfig-platform-transceiver', yang_type='container', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """transceiver must be of a type compatible with container""",
          'defined-type': "container",
          'generated-type': """YANGDynClass(base=transceiver.transceiver, is_container='container', yang_name="transceiver", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform/transceiver', defining_module='openconfig-platform-transceiver', yang_type='container', is_config=True)""",
        })

    self.__transceiver = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_transceiver(self):
    self.__transceiver = YANGDynClass(base=transceiver.transceiver, is_container='container', yang_name="transceiver", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/platform/transceiver', defining_module='openconfig-platform-transceiver', yang_type='container', is_config=True)

  name = __builtin__.property(_get_name, _set_name)
  config = __builtin__.property(_get_config, _set_config)
  state = __builtin__.property(_get_state, _set_state)
  properties = __builtin__.property(_get_properties, _set_properties)
  subcomponents = __builtin__.property(_get_subcomponents, _set_subcomponents)
  transceiver = __builtin__.property(_get_transceiver, _set_transceiver)


  _pyangbind_elements = {'name': name, 'config': config, 'state': state, 'properties': properties, 'subcomponents': subcomponents, 'transceiver': transceiver, }


