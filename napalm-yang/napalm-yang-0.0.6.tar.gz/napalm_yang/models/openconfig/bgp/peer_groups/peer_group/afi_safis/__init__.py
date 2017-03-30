
from operator import attrgetter
from pyangbind.lib.yangtypes import RestrictedPrecisionDecimalType, RestrictedClassType, TypedListType
from pyangbind.lib.yangtypes import YANGBool, YANGListType, YANGDynClass, ReferenceType
from pyangbind.lib.base import PybindBase
from decimal import Decimal
from bitarray import bitarray
import __builtin__
import afi_safi
class afi_safis(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp - based on the path /bgp/peer-groups/peer-group/afi-safis. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Per-address-family configuration parameters associated with
thegroup
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__afi_safi',)

  _yang_name = 'afi-safis'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis']

  def _get_afi_safi(self):
    """
    Getter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    return self.__afi_safi
      
  def _set_afi_safi(self, v, load=False):
    """
    Setter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_afi_safi is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_afi_safi() directly.

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """afi_safi must be of a type compatible with list""",
          'defined-type': "list",
          'generated-type': """YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)""",
        })

    self.__afi_safi = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_afi_safi(self):
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

  afi_safi = __builtin__.property(_get_afi_safi, _set_afi_safi)


  _pyangbind_elements = {'afi_safi': afi_safi, }


import afi_safi
class afi_safis(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-common - based on the path /bgp/peer-groups/peer-group/afi-safis. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Per-address-family configuration parameters associated with
thegroup
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__afi_safi',)

  _yang_name = 'afi-safis'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis']

  def _get_afi_safi(self):
    """
    Getter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    return self.__afi_safi
      
  def _set_afi_safi(self, v, load=False):
    """
    Setter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_afi_safi is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_afi_safi() directly.

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """afi_safi must be of a type compatible with list""",
          'defined-type': "list",
          'generated-type': """YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)""",
        })

    self.__afi_safi = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_afi_safi(self):
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

  afi_safi = __builtin__.property(_get_afi_safi, _set_afi_safi)


  _pyangbind_elements = {'afi_safi': afi_safi, }


import afi_safi
class afi_safis(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-common-multiprotocol - based on the path /bgp/peer-groups/peer-group/afi-safis. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Per-address-family configuration parameters associated with
thegroup
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__afi_safi',)

  _yang_name = 'afi-safis'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis']

  def _get_afi_safi(self):
    """
    Getter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    return self.__afi_safi
      
  def _set_afi_safi(self, v, load=False):
    """
    Setter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_afi_safi is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_afi_safi() directly.

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """afi_safi must be of a type compatible with list""",
          'defined-type': "list",
          'generated-type': """YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)""",
        })

    self.__afi_safi = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_afi_safi(self):
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

  afi_safi = __builtin__.property(_get_afi_safi, _set_afi_safi)


  _pyangbind_elements = {'afi_safi': afi_safi, }


import afi_safi
class afi_safis(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-common-structure - based on the path /bgp/peer-groups/peer-group/afi-safis. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Per-address-family configuration parameters associated with
thegroup
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__afi_safi',)

  _yang_name = 'afi-safis'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis']

  def _get_afi_safi(self):
    """
    Getter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    return self.__afi_safi
      
  def _set_afi_safi(self, v, load=False):
    """
    Setter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_afi_safi is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_afi_safi() directly.

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """afi_safi must be of a type compatible with list""",
          'defined-type': "list",
          'generated-type': """YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)""",
        })

    self.__afi_safi = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_afi_safi(self):
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

  afi_safi = __builtin__.property(_get_afi_safi, _set_afi_safi)


  _pyangbind_elements = {'afi_safi': afi_safi, }


import afi_safi
class afi_safis(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-peer-group - based on the path /bgp/peer-groups/peer-group/afi-safis. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Per-address-family configuration parameters associated with
thegroup
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__afi_safi',)

  _yang_name = 'afi-safis'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis']

  def _get_afi_safi(self):
    """
    Getter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    return self.__afi_safi
      
  def _set_afi_safi(self, v, load=False):
    """
    Setter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_afi_safi is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_afi_safi() directly.

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """afi_safi must be of a type compatible with list""",
          'defined-type': "list",
          'generated-type': """YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)""",
        })

    self.__afi_safi = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_afi_safi(self):
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

  afi_safi = __builtin__.property(_get_afi_safi, _set_afi_safi)


  _pyangbind_elements = {'afi_safi': afi_safi, }


import afi_safi
class afi_safis(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-neighbor - based on the path /bgp/peer-groups/peer-group/afi-safis. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Per-address-family configuration parameters associated with
thegroup
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__afi_safi',)

  _yang_name = 'afi-safis'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis']

  def _get_afi_safi(self):
    """
    Getter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    return self.__afi_safi
      
  def _set_afi_safi(self, v, load=False):
    """
    Setter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_afi_safi is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_afi_safi() directly.

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """afi_safi must be of a type compatible with list""",
          'defined-type': "list",
          'generated-type': """YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)""",
        })

    self.__afi_safi = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_afi_safi(self):
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

  afi_safi = __builtin__.property(_get_afi_safi, _set_afi_safi)


  _pyangbind_elements = {'afi_safi': afi_safi, }


import afi_safi
class afi_safis(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-global - based on the path /bgp/peer-groups/peer-group/afi-safis. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Per-address-family configuration parameters associated with
thegroup
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__afi_safi',)

  _yang_name = 'afi-safis'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis']

  def _get_afi_safi(self):
    """
    Getter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    return self.__afi_safi
      
  def _set_afi_safi(self, v, load=False):
    """
    Setter method for afi_safi, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi (list)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_afi_safi is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_afi_safi() directly.

    YANG Description: AFI,SAFI configuration available for the
neighbour or group
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """afi_safi must be of a type compatible with list""",
          'defined-type': "list",
          'generated-type': """YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)""",
        })

    self.__afi_safi = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_afi_safi(self):
    self.__afi_safi = YANGDynClass(base=YANGListType("afi_safi_name",afi_safi.afi_safi, yang_name="afi-safi", parent=self, is_container='list', user_ordered=False, path_helper=self._path_helper, yang_keys='afi-safi-name', extensions=None), is_container='list', yang_name="afi-safi", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, extensions=None, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='list', is_config=True)

  afi_safi = __builtin__.property(_get_afi_safi, _set_afi_safi)


  _pyangbind_elements = {'afi_safi': afi_safi, }


