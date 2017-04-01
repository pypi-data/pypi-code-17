# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/nickname_pokemon_response.proto

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
  name='pogoprotos/networking/responses/nickname_pokemon_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\n?pogoprotos/networking/responses/nickname_pokemon_response.proto\x12\x1fpogoprotos.networking.responses\"\xdf\x01\n\x17NicknamePokemonResponse\x12O\n\x06result\x18\x01 \x01(\x0e\x32?.pogoprotos.networking.responses.NicknamePokemonResponse.Result\"s\n\x06Result\x12\t\n\x05UNSET\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\x1a\n\x16\x45RROR_INVALID_NICKNAME\x10\x02\x12\x1b\n\x17\x45RROR_POKEMON_NOT_FOUND\x10\x03\x12\x18\n\x14\x45RROR_POKEMON_IS_EGG\x10\x04\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_NICKNAMEPOKEMONRESPONSE_RESULT = _descriptor.EnumDescriptor(
  name='Result',
  full_name='pogoprotos.networking.responses.NicknamePokemonResponse.Result',
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
      name='ERROR_INVALID_NICKNAME', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_POKEMON_NOT_FOUND', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_POKEMON_IS_EGG', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=209,
  serialized_end=324,
)
_sym_db.RegisterEnumDescriptor(_NICKNAMEPOKEMONRESPONSE_RESULT)


_NICKNAMEPOKEMONRESPONSE = _descriptor.Descriptor(
  name='NicknamePokemonResponse',
  full_name='pogoprotos.networking.responses.NicknamePokemonResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='pogoprotos.networking.responses.NicknamePokemonResponse.result', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _NICKNAMEPOKEMONRESPONSE_RESULT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=101,
  serialized_end=324,
)

_NICKNAMEPOKEMONRESPONSE.fields_by_name['result'].enum_type = _NICKNAMEPOKEMONRESPONSE_RESULT
_NICKNAMEPOKEMONRESPONSE_RESULT.containing_type = _NICKNAMEPOKEMONRESPONSE
DESCRIPTOR.message_types_by_name['NicknamePokemonResponse'] = _NICKNAMEPOKEMONRESPONSE

NicknamePokemonResponse = _reflection.GeneratedProtocolMessageType('NicknamePokemonResponse', (_message.Message,), dict(
  DESCRIPTOR = _NICKNAMEPOKEMONRESPONSE,
  __module__ = 'pogoprotos.networking.responses.nickname_pokemon_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.NicknamePokemonResponse)
  ))
_sym_db.RegisterMessage(NicknamePokemonResponse)


# @@protoc_insertion_point(module_scope)
