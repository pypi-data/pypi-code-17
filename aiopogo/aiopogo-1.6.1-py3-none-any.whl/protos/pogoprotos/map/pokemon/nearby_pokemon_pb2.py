# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/map/pokemon/nearby_pokemon.proto

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
  name='pogoprotos/map/pokemon/nearby_pokemon.proto',
  package='pogoprotos.map.pokemon',
  syntax='proto3',
  serialized_pb=_b('\n+pogoprotos/map/pokemon/nearby_pokemon.proto\x12\x16pogoprotos.map.pokemon\x1a!pogoprotos/enums/pokemon_id.proto\x1a%pogoprotos/data/pokemon_display.proto\"\xd5\x01\n\rNearbyPokemon\x12/\n\npokemon_id\x18\x01 \x01(\x0e\x32\x1b.pogoprotos.enums.PokemonId\x12\x1a\n\x12\x64istance_in_meters\x18\x02 \x01(\x02\x12\x14\n\x0c\x65ncounter_id\x18\x03 \x01(\x06\x12\x0f\n\x07\x66ort_id\x18\x04 \x01(\t\x12\x16\n\x0e\x66ort_image_url\x18\x05 \x01(\t\x12\x38\n\x0fpokemon_display\x18\x06 \x01(\x0b\x32\x1f.pogoprotos.data.PokemonDisplayb\x06proto3')
  ,
  dependencies=[pogoprotos_dot_enums_dot_pokemon__id__pb2.DESCRIPTOR,pogoprotos_dot_data_dot_pokemon__display__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_NEARBYPOKEMON = _descriptor.Descriptor(
  name='NearbyPokemon',
  full_name='pogoprotos.map.pokemon.NearbyPokemon',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pokemon_id', full_name='pogoprotos.map.pokemon.NearbyPokemon.pokemon_id', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='distance_in_meters', full_name='pogoprotos.map.pokemon.NearbyPokemon.distance_in_meters', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='encounter_id', full_name='pogoprotos.map.pokemon.NearbyPokemon.encounter_id', index=2,
      number=3, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fort_id', full_name='pogoprotos.map.pokemon.NearbyPokemon.fort_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fort_image_url', full_name='pogoprotos.map.pokemon.NearbyPokemon.fort_image_url', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pokemon_display', full_name='pogoprotos.map.pokemon.NearbyPokemon.pokemon_display', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=146,
  serialized_end=359,
)

_NEARBYPOKEMON.fields_by_name['pokemon_id'].enum_type = pogoprotos_dot_enums_dot_pokemon__id__pb2._POKEMONID
_NEARBYPOKEMON.fields_by_name['pokemon_display'].message_type = pogoprotos_dot_data_dot_pokemon__display__pb2._POKEMONDISPLAY
DESCRIPTOR.message_types_by_name['NearbyPokemon'] = _NEARBYPOKEMON

NearbyPokemon = _reflection.GeneratedProtocolMessageType('NearbyPokemon', (_message.Message,), dict(
  DESCRIPTOR = _NEARBYPOKEMON,
  __module__ = 'pogoprotos.map.pokemon.nearby_pokemon_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.map.pokemon.NearbyPokemon)
  ))
_sym_db.RegisterMessage(NearbyPokemon)


# @@protoc_insertion_point(module_scope)
