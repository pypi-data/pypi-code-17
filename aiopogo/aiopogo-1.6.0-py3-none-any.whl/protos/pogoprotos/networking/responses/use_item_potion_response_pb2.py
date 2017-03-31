# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/use_item_potion_response.proto

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
  name='pogoprotos/networking/responses/use_item_potion_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\n>pogoprotos/networking/responses/use_item_potion_response.proto\x12\x1fpogoprotos.networking.responses\"\xe1\x01\n\x15UseItemPotionResponse\x12M\n\x06result\x18\x01 \x01(\x0e\x32=.pogoprotos.networking.responses.UseItemPotionResponse.Result\x12\x0f\n\x07stamina\x18\x02 \x01(\x05\"h\n\x06Result\x12\t\n\x05UNSET\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\x14\n\x10\x45RROR_NO_POKEMON\x10\x02\x12\x14\n\x10\x45RROR_CANNOT_USE\x10\x03\x12\x1a\n\x16\x45RROR_DEPLOYED_TO_FORT\x10\x04\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_USEITEMPOTIONRESPONSE_RESULT = _descriptor.EnumDescriptor(
  name='Result',
  full_name='pogoprotos.networking.responses.UseItemPotionResponse.Result',
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
      name='ERROR_NO_POKEMON', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_CANNOT_USE', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_DEPLOYED_TO_FORT', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=221,
  serialized_end=325,
)
_sym_db.RegisterEnumDescriptor(_USEITEMPOTIONRESPONSE_RESULT)


_USEITEMPOTIONRESPONSE = _descriptor.Descriptor(
  name='UseItemPotionResponse',
  full_name='pogoprotos.networking.responses.UseItemPotionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='pogoprotos.networking.responses.UseItemPotionResponse.result', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stamina', full_name='pogoprotos.networking.responses.UseItemPotionResponse.stamina', index=1,
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
    _USEITEMPOTIONRESPONSE_RESULT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=100,
  serialized_end=325,
)

_USEITEMPOTIONRESPONSE.fields_by_name['result'].enum_type = _USEITEMPOTIONRESPONSE_RESULT
_USEITEMPOTIONRESPONSE_RESULT.containing_type = _USEITEMPOTIONRESPONSE
DESCRIPTOR.message_types_by_name['UseItemPotionResponse'] = _USEITEMPOTIONRESPONSE

UseItemPotionResponse = _reflection.GeneratedProtocolMessageType('UseItemPotionResponse', (_message.Message,), dict(
  DESCRIPTOR = _USEITEMPOTIONRESPONSE,
  __module__ = 'pogoprotos.networking.responses.use_item_potion_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.UseItemPotionResponse)
  ))
_sym_db.RegisterMessage(UseItemPotionResponse)


# @@protoc_insertion_point(module_scope)
