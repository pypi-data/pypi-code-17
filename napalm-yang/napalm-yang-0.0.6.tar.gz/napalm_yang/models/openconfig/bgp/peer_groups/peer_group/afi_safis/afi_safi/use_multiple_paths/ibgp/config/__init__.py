
from operator import attrgetter
from pyangbind.lib.yangtypes import RestrictedPrecisionDecimalType, RestrictedClassType, TypedListType
from pyangbind.lib.yangtypes import YANGBool, YANGListType, YANGDynClass, ReferenceType
from pyangbind.lib.base import PybindBase
from decimal import Decimal
from bitarray import bitarray
import __builtin__
class config(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp - based on the path /bgp/peer-groups/peer-group/afi-safis/afi-safi/use-multiple-paths/ibgp/config. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Configuration parameters relating to iBGP multipath
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__maximum_paths',)

  _yang_name = 'config'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis', u'afi-safi', u'use-multiple-paths', u'ibgp', u'config']

  def _get_maximum_paths(self):
    """
    Getter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    return self.__maximum_paths
      
  def _set_maximum_paths(self, v, load=False):
    """
    Setter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_maximum_paths is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_maximum_paths() directly.

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """maximum_paths must be of a type compatible with uint32""",
          'defined-type': "uint32",
          'generated-type': """YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)""",
        })

    self.__maximum_paths = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_maximum_paths(self):
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

  maximum_paths = __builtin__.property(_get_maximum_paths, _set_maximum_paths)


  _pyangbind_elements = {'maximum_paths': maximum_paths, }


class config(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-common - based on the path /bgp/peer-groups/peer-group/afi-safis/afi-safi/use-multiple-paths/ibgp/config. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Configuration parameters relating to iBGP multipath
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__maximum_paths',)

  _yang_name = 'config'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis', u'afi-safi', u'use-multiple-paths', u'ibgp', u'config']

  def _get_maximum_paths(self):
    """
    Getter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    return self.__maximum_paths
      
  def _set_maximum_paths(self, v, load=False):
    """
    Setter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_maximum_paths is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_maximum_paths() directly.

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """maximum_paths must be of a type compatible with uint32""",
          'defined-type': "uint32",
          'generated-type': """YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)""",
        })

    self.__maximum_paths = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_maximum_paths(self):
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

  maximum_paths = __builtin__.property(_get_maximum_paths, _set_maximum_paths)


  _pyangbind_elements = {'maximum_paths': maximum_paths, }


class config(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-common-multiprotocol - based on the path /bgp/peer-groups/peer-group/afi-safis/afi-safi/use-multiple-paths/ibgp/config. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Configuration parameters relating to iBGP multipath
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__maximum_paths',)

  _yang_name = 'config'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis', u'afi-safi', u'use-multiple-paths', u'ibgp', u'config']

  def _get_maximum_paths(self):
    """
    Getter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    return self.__maximum_paths
      
  def _set_maximum_paths(self, v, load=False):
    """
    Setter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_maximum_paths is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_maximum_paths() directly.

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """maximum_paths must be of a type compatible with uint32""",
          'defined-type': "uint32",
          'generated-type': """YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)""",
        })

    self.__maximum_paths = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_maximum_paths(self):
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

  maximum_paths = __builtin__.property(_get_maximum_paths, _set_maximum_paths)


  _pyangbind_elements = {'maximum_paths': maximum_paths, }


class config(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-common-structure - based on the path /bgp/peer-groups/peer-group/afi-safis/afi-safi/use-multiple-paths/ibgp/config. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Configuration parameters relating to iBGP multipath
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__maximum_paths',)

  _yang_name = 'config'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis', u'afi-safi', u'use-multiple-paths', u'ibgp', u'config']

  def _get_maximum_paths(self):
    """
    Getter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    return self.__maximum_paths
      
  def _set_maximum_paths(self, v, load=False):
    """
    Setter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_maximum_paths is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_maximum_paths() directly.

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """maximum_paths must be of a type compatible with uint32""",
          'defined-type': "uint32",
          'generated-type': """YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)""",
        })

    self.__maximum_paths = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_maximum_paths(self):
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

  maximum_paths = __builtin__.property(_get_maximum_paths, _set_maximum_paths)


  _pyangbind_elements = {'maximum_paths': maximum_paths, }


class config(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-peer-group - based on the path /bgp/peer-groups/peer-group/afi-safis/afi-safi/use-multiple-paths/ibgp/config. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Configuration parameters relating to iBGP multipath
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__maximum_paths',)

  _yang_name = 'config'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis', u'afi-safi', u'use-multiple-paths', u'ibgp', u'config']

  def _get_maximum_paths(self):
    """
    Getter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    return self.__maximum_paths
      
  def _set_maximum_paths(self, v, load=False):
    """
    Setter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_maximum_paths is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_maximum_paths() directly.

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """maximum_paths must be of a type compatible with uint32""",
          'defined-type': "uint32",
          'generated-type': """YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)""",
        })

    self.__maximum_paths = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_maximum_paths(self):
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

  maximum_paths = __builtin__.property(_get_maximum_paths, _set_maximum_paths)


  _pyangbind_elements = {'maximum_paths': maximum_paths, }


class config(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-neighbor - based on the path /bgp/peer-groups/peer-group/afi-safis/afi-safi/use-multiple-paths/ibgp/config. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Configuration parameters relating to iBGP multipath
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__maximum_paths',)

  _yang_name = 'config'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis', u'afi-safi', u'use-multiple-paths', u'ibgp', u'config']

  def _get_maximum_paths(self):
    """
    Getter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    return self.__maximum_paths
      
  def _set_maximum_paths(self, v, load=False):
    """
    Setter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_maximum_paths is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_maximum_paths() directly.

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """maximum_paths must be of a type compatible with uint32""",
          'defined-type': "uint32",
          'generated-type': """YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)""",
        })

    self.__maximum_paths = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_maximum_paths(self):
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

  maximum_paths = __builtin__.property(_get_maximum_paths, _set_maximum_paths)


  _pyangbind_elements = {'maximum_paths': maximum_paths, }


class config(PybindBase):
  """
  This class was auto-generated by the PythonClass plugin for PYANG
  from YANG module openconfig-bgp-global - based on the path /bgp/peer-groups/peer-group/afi-safis/afi-safi/use-multiple-paths/ibgp/config. Each member element of
  the container is represented as a class variable - with a specific
  YANG type.

  YANG Description: Configuration parameters relating to iBGP multipath
  """
  __slots__ = ('_pybind_generated_by', '_path_helper', '_yang_name', '_extmethods', '__maximum_paths',)

  _yang_name = 'config'

  _pybind_generated_by = 'container'

  def __init__(self, *args, **kwargs):

    self._path_helper = False

    self._extmethods = False
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

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
      return [u'bgp', u'peer-groups', u'peer-group', u'afi-safis', u'afi-safi', u'use-multiple-paths', u'ibgp', u'config']

  def _get_maximum_paths(self):
    """
    Getter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    return self.__maximum_paths
      
  def _set_maximum_paths(self, v, load=False):
    """
    Setter method for maximum_paths, mapped from YANG variable /bgp/peer_groups/peer_group/afi_safis/afi_safi/use_multiple_paths/ibgp/config/maximum_paths (uint32)
    If this variable is read-only (config: false) in the
    source YANG file, then _set_maximum_paths is considered as a private
    method. Backends looking to populate this variable should
    do so via calling thisObj._set_maximum_paths() directly.

    YANG Description: Maximum number of parallel paths to consider when using
iBGP multipath. The default is to use a single path
    """
    if hasattr(v, "_utype"):
      v = v._utype(v)
    try:
      t = YANGDynClass(v,base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)
    except (TypeError, ValueError):
      raise ValueError({
          'error-string': """maximum_paths must be of a type compatible with uint32""",
          'defined-type': "uint32",
          'generated-type': """YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)""",
        })

    self.__maximum_paths = t
    if hasattr(self, '_set'):
      self._set()

  def _unset_maximum_paths(self):
    self.__maximum_paths = YANGDynClass(base=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32), default=RestrictedClassType(base_type=long, restriction_dict={'range': ['0..4294967295']}, int_size=32)(1), is_leaf=True, yang_name="maximum-paths", parent=self, path_helper=self._path_helper, extmethods=self._extmethods, register_paths=True, namespace='http://openconfig.net/yang/bgp', defining_module='openconfig-bgp', yang_type='uint32', is_config=True)

  maximum_paths = __builtin__.property(_get_maximum_paths, _set_maximum_paths)


  _pyangbind_elements = {'maximum_paths': maximum_paths, }


