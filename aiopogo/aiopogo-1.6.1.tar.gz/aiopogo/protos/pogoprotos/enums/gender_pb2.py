# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/enums/gender.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/enums/gender.proto',
  package='pogoprotos.enums',
  syntax='proto3',
  serialized_pb=_b('\n\x1dpogoprotos/enums/gender.proto\x12\x10pogoprotos.enums*@\n\x06Gender\x12\x10\n\x0cGENDER_UNSET\x10\x00\x12\x08\n\x04MALE\x10\x01\x12\n\n\x06\x46\x45MALE\x10\x02\x12\x0e\n\nGENDERLESS\x10\x03\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_GENDER = _descriptor.EnumDescriptor(
  name='Gender',
  full_name='pogoprotos.enums.Gender',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GENDER_UNSET', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MALE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FEMALE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GENDERLESS', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=51,
  serialized_end=115,
)
_sym_db.RegisterEnumDescriptor(_GENDER)

Gender = enum_type_wrapper.EnumTypeWrapper(_GENDER)
GENDER_UNSET = 0
MALE = 1
FEMALE = 2
GENDERLESS = 3


DESCRIPTOR.enum_types_by_name['Gender'] = _GENDER


# @@protoc_insertion_point(module_scope)
