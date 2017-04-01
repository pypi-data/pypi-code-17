# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/recycle_inventory_item_response.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/networking/responses/recycle_inventory_item_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\nEpogoprotos/networking/responses/recycle_inventory_item_response.proto\x12\x1fpogoprotos.networking.responses\"\xeb\x01\n\x1cRecycleInventoryItemResponse\x12T\n\x06result\x18\x01 \x01(\x0e\x32\x44.pogoprotos.networking.responses.RecycleInventoryItemResponse.Result\x12\x11\n\tnew_count\x18\x02 \x01(\x05\"b\n\x06Result\x12\t\n\x05UNSET\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\x1b\n\x17\x45RROR_NOT_ENOUGH_COPIES\x10\x02\x12#\n\x1f\x45RROR_CANNOT_RECYCLE_INCUBATORS\x10\x03\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_RECYCLEINVENTORYITEMRESPONSE_RESULT = _descriptor.EnumDescriptor(
  name='Result',
  full_name='pogoprotos.networking.responses.RecycleInventoryItemResponse.Result',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSET', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_NOT_ENOUGH_COPIES', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_CANNOT_RECYCLE_INCUBATORS', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=244,
  serialized_end=342,
)
_sym_db.RegisterEnumDescriptor(_RECYCLEINVENTORYITEMRESPONSE_RESULT)


_RECYCLEINVENTORYITEMRESPONSE = _descriptor.Descriptor(
  name='RecycleInventoryItemResponse',
  full_name='pogoprotos.networking.responses.RecycleInventoryItemResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='pogoprotos.networking.responses.RecycleInventoryItemResponse.result', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='new_count', full_name='pogoprotos.networking.responses.RecycleInventoryItemResponse.new_count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RECYCLEINVENTORYITEMRESPONSE_RESULT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=342,
)

_RECYCLEINVENTORYITEMRESPONSE.fields_by_name['result'].enum_type = _RECYCLEINVENTORYITEMRESPONSE_RESULT
_RECYCLEINVENTORYITEMRESPONSE_RESULT.containing_type = _RECYCLEINVENTORYITEMRESPONSE
DESCRIPTOR.message_types_by_name['RecycleInventoryItemResponse'] = _RECYCLEINVENTORYITEMRESPONSE

RecycleInventoryItemResponse = _reflection.GeneratedProtocolMessageType('RecycleInventoryItemResponse', (_message.Message,), dict(
  DESCRIPTOR = _RECYCLEINVENTORYITEMRESPONSE,
  __module__ = 'pogoprotos.networking.responses.recycle_inventory_item_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.RecycleInventoryItemResponse)
  ))
_sym_db.RegisterMessage(RecycleInventoryItemResponse)


# @@protoc_insertion_point(module_scope)
