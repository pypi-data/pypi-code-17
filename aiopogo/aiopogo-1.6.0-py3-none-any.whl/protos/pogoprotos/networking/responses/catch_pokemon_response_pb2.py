# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/catch_pokemon_response.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pogoprotos.data.capture import capture_award_pb2 as pogoprotos_dot_data_dot_capture_dot_capture__award__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/networking/responses/catch_pokemon_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\n<pogoprotos/networking/responses/catch_pokemon_response.proto\x12\x1fpogoprotos.networking.responses\x1a+pogoprotos/data/capture/capture_award.proto\"\x8c\x04\n\x14\x43\x61tchPokemonResponse\x12Q\n\x06status\x18\x01 \x01(\x0e\x32\x41.pogoprotos.networking.responses.CatchPokemonResponse.CatchStatus\x12\x14\n\x0cmiss_percent\x18\x02 \x01(\x01\x12\x1b\n\x13\x63\x61ptured_pokemon_id\x18\x03 \x01(\x06\x12<\n\rcapture_award\x18\x04 \x01(\x0b\x32%.pogoprotos.data.capture.CaptureAward\x12[\n\x0e\x63\x61pture_reason\x18\x05 \x01(\x0e\x32\x43.pogoprotos.networking.responses.CatchPokemonResponse.CaptureReason\x12\x1a\n\x12\x64isplay_pokedex_id\x18\x06 \x01(\x05\"e\n\x0b\x43\x61tchStatus\x12\x0f\n\x0b\x43\x41TCH_ERROR\x10\x00\x12\x11\n\rCATCH_SUCCESS\x10\x01\x12\x10\n\x0c\x43\x41TCH_ESCAPE\x10\x02\x12\x0e\n\nCATCH_FLEE\x10\x03\x12\x10\n\x0c\x43\x41TCH_MISSED\x10\x04\"P\n\rCaptureReason\x12\t\n\x05UNSET\x10\x00\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x01\x12\x13\n\x0f\x45LEMENTAL_BADGE\x10\x02\x12\x12\n\x0e\x43RITICAL_CATCH\x10\x03\x62\x06proto3')
  ,
  dependencies=[pogoprotos_dot_data_dot_capture_dot_capture__award__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_CATCHPOKEMONRESPONSE_CATCHSTATUS = _descriptor.EnumDescriptor(
  name='CatchStatus',
  full_name='pogoprotos.networking.responses.CatchPokemonResponse.CatchStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CATCH_ERROR', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CATCH_SUCCESS', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CATCH_ESCAPE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CATCH_FLEE', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CATCH_MISSED', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=484,
  serialized_end=585,
)
_sym_db.RegisterEnumDescriptor(_CATCHPOKEMONRESPONSE_CATCHSTATUS)

_CATCHPOKEMONRESPONSE_CAPTUREREASON = _descriptor.EnumDescriptor(
  name='CaptureReason',
  full_name='pogoprotos.networking.responses.CatchPokemonResponse.CaptureReason',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSET', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEFAULT', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ELEMENTAL_BADGE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CRITICAL_CATCH', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=587,
  serialized_end=667,
)
_sym_db.RegisterEnumDescriptor(_CATCHPOKEMONRESPONSE_CAPTUREREASON)


_CATCHPOKEMONRESPONSE = _descriptor.Descriptor(
  name='CatchPokemonResponse',
  full_name='pogoprotos.networking.responses.CatchPokemonResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='pogoprotos.networking.responses.CatchPokemonResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='miss_percent', full_name='pogoprotos.networking.responses.CatchPokemonResponse.miss_percent', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='captured_pokemon_id', full_name='pogoprotos.networking.responses.CatchPokemonResponse.captured_pokemon_id', index=2,
      number=3, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='capture_award', full_name='pogoprotos.networking.responses.CatchPokemonResponse.capture_award', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='capture_reason', full_name='pogoprotos.networking.responses.CatchPokemonResponse.capture_reason', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='display_pokedex_id', full_name='pogoprotos.networking.responses.CatchPokemonResponse.display_pokedex_id', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CATCHPOKEMONRESPONSE_CATCHSTATUS,
    _CATCHPOKEMONRESPONSE_CAPTUREREASON,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=667,
)

_CATCHPOKEMONRESPONSE.fields_by_name['status'].enum_type = _CATCHPOKEMONRESPONSE_CATCHSTATUS
_CATCHPOKEMONRESPONSE.fields_by_name['capture_award'].message_type = pogoprotos_dot_data_dot_capture_dot_capture__award__pb2._CAPTUREAWARD
_CATCHPOKEMONRESPONSE.fields_by_name['capture_reason'].enum_type = _CATCHPOKEMONRESPONSE_CAPTUREREASON
_CATCHPOKEMONRESPONSE_CATCHSTATUS.containing_type = _CATCHPOKEMONRESPONSE
_CATCHPOKEMONRESPONSE_CAPTUREREASON.containing_type = _CATCHPOKEMONRESPONSE
DESCRIPTOR.message_types_by_name['CatchPokemonResponse'] = _CATCHPOKEMONRESPONSE

CatchPokemonResponse = _reflection.GeneratedProtocolMessageType('CatchPokemonResponse', (_message.Message,), dict(
  DESCRIPTOR = _CATCHPOKEMONRESPONSE,
  __module__ = 'pogoprotos.networking.responses.catch_pokemon_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.CatchPokemonResponse)
  ))
_sym_db.RegisterMessage(CatchPokemonResponse)


# @@protoc_insertion_point(module_scope)
