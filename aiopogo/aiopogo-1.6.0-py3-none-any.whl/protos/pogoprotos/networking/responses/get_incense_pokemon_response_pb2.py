# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/get_incense_pokemon_response.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pogoprotos.enums import pokemon_id_pb2 as pogoprotos_dot_enums_dot_pokemon__id__pb2
from pogoprotos.data import pokemon_display_pb2 as pogoprotos_dot_data_dot_pokemon__display__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/networking/responses/get_incense_pokemon_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\nBpogoprotos/networking/responses/get_incense_pokemon_response.proto\x12\x1fpogoprotos.networking.responses\x1a!pogoprotos/enums/pokemon_id.proto\x1a%pogoprotos/data/pokemon_display.proto\"\xbf\x03\n\x19GetIncensePokemonResponse\x12Q\n\x06result\x18\x01 \x01(\x0e\x32\x41.pogoprotos.networking.responses.GetIncensePokemonResponse.Result\x12/\n\npokemon_id\x18\x02 \x01(\x0e\x32\x1b.pogoprotos.enums.PokemonId\x12\x10\n\x08latitude\x18\x03 \x01(\x01\x12\x11\n\tlongitude\x18\x04 \x01(\x01\x12\x1a\n\x12\x65ncounter_location\x18\x05 \x01(\t\x12\x14\n\x0c\x65ncounter_id\x18\x06 \x01(\x06\x12\x1e\n\x16\x64isappear_timestamp_ms\x18\x07 \x01(\x03\x12\x38\n\x0fpokemon_display\x18\x08 \x01(\x0b\x32\x1f.pogoprotos.data.PokemonDisplay\"m\n\x06Result\x12\x1d\n\x19INCENSE_ENCOUNTER_UNKNOWN\x10\x00\x12\x1f\n\x1bINCENSE_ENCOUNTER_AVAILABLE\x10\x01\x12#\n\x1fINCENSE_ENCOUNTER_NOT_AVAILABLE\x10\x02\x62\x06proto3')
  ,
  dependencies=[pogoprotos_dot_enums_dot_pokemon__id__pb2.DESCRIPTOR,pogoprotos_dot_data_dot_pokemon__display__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_GETINCENSEPOKEMONRESPONSE_RESULT = _descriptor.EnumDescriptor(
  name='Result',
  full_name='pogoprotos.networking.responses.GetIncensePokemonResponse.Result',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INCENSE_ENCOUNTER_UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INCENSE_ENCOUNTER_AVAILABLE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INCENSE_ENCOUNTER_NOT_AVAILABLE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=516,
  serialized_end=625,
)
_sym_db.RegisterEnumDescriptor(_GETINCENSEPOKEMONRESPONSE_RESULT)


_GETINCENSEPOKEMONRESPONSE = _descriptor.Descriptor(
  name='GetIncensePokemonResponse',
  full_name='pogoprotos.networking.responses.GetIncensePokemonResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='pogoprotos.networking.responses.GetIncensePokemonResponse.result', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pokemon_id', full_name='pogoprotos.networking.responses.GetIncensePokemonResponse.pokemon_id', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='latitude', full_name='pogoprotos.networking.responses.GetIncensePokemonResponse.latitude', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='longitude', full_name='pogoprotos.networking.responses.GetIncensePokemonResponse.longitude', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='encounter_location', full_name='pogoprotos.networking.responses.GetIncensePokemonResponse.encounter_location', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='encounter_id', full_name='pogoprotos.networking.responses.GetIncensePokemonResponse.encounter_id', index=5,
      number=6, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='disappear_timestamp_ms', full_name='pogoprotos.networking.responses.GetIncensePokemonResponse.disappear_timestamp_ms', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pokemon_display', full_name='pogoprotos.networking.responses.GetIncensePokemonResponse.pokemon_display', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GETINCENSEPOKEMONRESPONSE_RESULT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=178,
  serialized_end=625,
)

_GETINCENSEPOKEMONRESPONSE.fields_by_name['result'].enum_type = _GETINCENSEPOKEMONRESPONSE_RESULT
_GETINCENSEPOKEMONRESPONSE.fields_by_name['pokemon_id'].enum_type = pogoprotos_dot_enums_dot_pokemon__id__pb2._POKEMONID
_GETINCENSEPOKEMONRESPONSE.fields_by_name['pokemon_display'].message_type = pogoprotos_dot_data_dot_pokemon__display__pb2._POKEMONDISPLAY
_GETINCENSEPOKEMONRESPONSE_RESULT.containing_type = _GETINCENSEPOKEMONRESPONSE
DESCRIPTOR.message_types_by_name['GetIncensePokemonResponse'] = _GETINCENSEPOKEMONRESPONSE

GetIncensePokemonResponse = _reflection.GeneratedProtocolMessageType('GetIncensePokemonResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETINCENSEPOKEMONRESPONSE,
  __module__ = 'pogoprotos.networking.responses.get_incense_pokemon_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.GetIncensePokemonResponse)
  ))
_sym_db.RegisterMessage(GetIncensePokemonResponse)


# @@protoc_insertion_point(module_scope)
