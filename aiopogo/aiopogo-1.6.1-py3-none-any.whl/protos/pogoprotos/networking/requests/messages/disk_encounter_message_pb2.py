# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/requests/messages/disk_encounter_message.proto

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
  name='pogoprotos/networking/requests/messages/disk_encounter_message.proto',
  package='pogoprotos.networking.requests.messages',
  syntax='proto3',
  serialized_pb=_b('\nDpogoprotos/networking/requests/messages/disk_encounter_message.proto\x12\'pogoprotos.networking.requests.messages\"p\n\x14\x44iskEncounterMessage\x12\x14\n\x0c\x65ncounter_id\x18\x01 \x01(\x04\x12\x0f\n\x07\x66ort_id\x18\x02 \x01(\t\x12\x17\n\x0fplayer_latitude\x18\x03 \x01(\x01\x12\x18\n\x10player_longitude\x18\x04 \x01(\x01\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_DISKENCOUNTERMESSAGE = _descriptor.Descriptor(
  name='DiskEncounterMessage',
  full_name='pogoprotos.networking.requests.messages.DiskEncounterMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='encounter_id', full_name='pogoprotos.networking.requests.messages.DiskEncounterMessage.encounter_id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fort_id', full_name='pogoprotos.networking.requests.messages.DiskEncounterMessage.fort_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player_latitude', full_name='pogoprotos.networking.requests.messages.DiskEncounterMessage.player_latitude', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player_longitude', full_name='pogoprotos.networking.requests.messages.DiskEncounterMessage.player_longitude', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=113,
  serialized_end=225,
)

DESCRIPTOR.message_types_by_name['DiskEncounterMessage'] = _DISKENCOUNTERMESSAGE

DiskEncounterMessage = _reflection.GeneratedProtocolMessageType('DiskEncounterMessage', (_message.Message,), dict(
  DESCRIPTOR = _DISKENCOUNTERMESSAGE,
  __module__ = 'pogoprotos.networking.requests.messages.disk_encounter_message_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.requests.messages.DiskEncounterMessage)
  ))
_sym_db.RegisterMessage(DiskEncounterMessage)


# @@protoc_insertion_point(module_scope)
