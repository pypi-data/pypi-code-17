# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/get_buddy_walked_response.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pogoprotos.enums import pokemon_family_id_pb2 as pogoprotos_dot_enums_dot_pokemon__family__id__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/networking/responses/get_buddy_walked_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\n?pogoprotos/networking/responses/get_buddy_walked_response.proto\x12\x1fpogoprotos.networking.responses\x1a(pogoprotos/enums/pokemon_family_id.proto\"\x81\x01\n\x16GetBuddyWalkedResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12:\n\x0f\x66\x61mily_candy_id\x18\x02 \x01(\x0e\x32!.pogoprotos.enums.PokemonFamilyId\x12\x1a\n\x12\x63\x61ndy_earned_count\x18\x03 \x01(\x05\x62\x06proto3')
  ,
  dependencies=[pogoprotos_dot_enums_dot_pokemon__family__id__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_GETBUDDYWALKEDRESPONSE = _descriptor.Descriptor(
  name='GetBuddyWalkedResponse',
  full_name='pogoprotos.networking.responses.GetBuddyWalkedResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='pogoprotos.networking.responses.GetBuddyWalkedResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='family_candy_id', full_name='pogoprotos.networking.responses.GetBuddyWalkedResponse.family_candy_id', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='candy_earned_count', full_name='pogoprotos.networking.responses.GetBuddyWalkedResponse.candy_earned_count', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=272,
)

_GETBUDDYWALKEDRESPONSE.fields_by_name['family_candy_id'].enum_type = pogoprotos_dot_enums_dot_pokemon__family__id__pb2._POKEMONFAMILYID
DESCRIPTOR.message_types_by_name['GetBuddyWalkedResponse'] = _GETBUDDYWALKEDRESPONSE

GetBuddyWalkedResponse = _reflection.GeneratedProtocolMessageType('GetBuddyWalkedResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETBUDDYWALKEDRESPONSE,
  __module__ = 'pogoprotos.networking.responses.get_buddy_walked_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.GetBuddyWalkedResponse)
  ))
_sym_db.RegisterMessage(GetBuddyWalkedResponse)


# @@protoc_insertion_point(module_scope)
