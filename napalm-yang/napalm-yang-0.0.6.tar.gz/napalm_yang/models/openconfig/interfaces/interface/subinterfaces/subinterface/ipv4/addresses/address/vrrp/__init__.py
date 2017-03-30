
from operator import attrgetter
from pyangbind.lib.yangtypes import RestrictedPrecisionDecimalType, RestrictedClassType, TypedListType
from pyangbind.lib.yangtypes import YANGBool, YANGListType, YANGDynClass, ReferenceType
from pyangbind.lib.base import PybindBase
from decimal import Decimal
from bitarray import bitarray
import __builtin__
import vrrp_group
class vrrp(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-interfaces - based on the path /interfaces/interface/subinterfaces/subinterface/ipv4/addresses/address/vrrp. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Enclosing container for VRRP groups handled by this
IP interface
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__vrrp_group',)

  _yang_name = 'vrrp'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__vrrp_group = YANGDynClass(base=YANGListType("virtual_router_id",vrrp_group.vrrp_group, yang_name="vrrp-group", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='virtual-router-id', extensions=None), is_container='list', yang_name="vrrp-group", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/interfaces/ip', defining_module='openconfig-if-ip', yang_type='list', is_config=True)

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
      return [u'interfaces', u'interface', u'subinterfaces', u'subinterface', u'ipv4', u'addresses', u'address', u'vrrp']

  def _get_vrrp_group(self):
    """
    Getter method for vrrp_group, mapped from YANG variable /interfaces/interface/subinterfaces/subinterface/ipv4/addresses/address/vrrp/vrrp_group (list)

    YANG Description: List of VRRP groups, keyed by virtual router id
    """
    return self.__vrrp_group
      
  def _set_vrrp_group(self, v, load=False):
    """
    Setter method for vrrp_group, mapped from YANG variable /interfaces/interface/subinterfaces/subinterface/ipv4/addresses/address/vrrp/vrrp_group (list)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_vrrp_group is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_vrrp_group() directly.

    YANG Description: List of VRRP groups, keyed by virtual router id
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=YANGListType("virtual_router_id",vrrp_group.vrrp_group, yang_name="vrrp-group", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='virtual-router-id', extensions=None), is_container='list', yang_name="vrrp-group", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/interfaces/ip', defining_module='openconfig-if-ip', yang_type='list', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """vrrp_group must be of a type compatible with list""",
          'defined-type': "list",
          'generated-type': """YANGDynClass(base=YANGListType("virtual_router_id",vrrp_group.vrrp_group, yang_name="vrrp-group", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='virtual-router-id', extensions=None), is_container='list', yang_name="vrrp-group", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/interfaces/ip', defining_module='openconfig-if-ip', yang_type='list', is_config=True)""",
        })

    self.__vrrp_group = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_vrrp_group(self):
    self.__vrrp_group = YANGDynClass(base=YANGListType("virtual_router_id",vrrp_group.vrrp_group, yang_name="vrrp-group", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='virtual-router-id', extensions=None), is_container='list', yang_name="vrrp-group", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/interfaces/ip', defining_module='openconfig-if-ip', yang_type='list', is_config=True)

  vrrp_group = __builtin__.property(_get_vrrp_group, _set_vrrp_group)


  _pyangbind_elements = {'vrrp_group': vrrp_group, }


