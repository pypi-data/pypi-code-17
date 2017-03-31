# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/settings/master/quest_settings.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pogoprotos.enums import quest_type_pb2 as pogoprotos_dot_enums_dot_quest__type__pb2
from pogoprotos.settings.master.quest import daily_quest_settings_pb2 as pogoprotos_dot_settings_dot_master_dot_quest_dot_daily__quest__settings__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/settings/master/quest_settings.proto',
  package='pogoprotos.settings.master',
  syntax='proto3',
  serialized_pb=_b('\n/pogoprotos/settings/master/quest_settings.proto\x12\x1apogoprotos.settings.master\x1a!pogoprotos/enums/quest_type.proto\x1a;pogoprotos/settings/master/quest/daily_quest_settings.proto\"\x8b\x01\n\rQuestSettings\x12/\n\nquest_type\x18\x01 \x01(\x0e\x32\x1b.pogoprotos.enums.QuestType\x12I\n\x0b\x64\x61ily_quest\x18\x02 \x01(\x0b\x32\x34.pogoprotos.settings.master.quest.DailyQuestSettingsb\x06proto3')
  ,
  dependencies=[pogoprotos_dot_enums_dot_quest__type__pb2.DESCRIPTOR,pogoprotos_dot_settings_dot_master_dot_quest_dot_daily__quest__settings__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_QUESTSETTINGS = _descriptor.Descriptor(
  name='QuestSettings',
  full_name='pogoprotos.settings.master.QuestSettings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='quest_type', full_name='pogoprotos.settings.master.QuestSettings.quest_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='daily_quest', full_name='pogoprotos.settings.master.QuestSettings.daily_quest', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=176,
  serialized_end=315,
)

_QUESTSETTINGS.fields_by_name['quest_type'].enum_type = pogoprotos_dot_enums_dot_quest__type__pb2._QUESTTYPE
_QUESTSETTINGS.fields_by_name['daily_quest'].message_type = pogoprotos_dot_settings_dot_master_dot_quest_dot_daily__quest__settings__pb2._DAILYQUESTSETTINGS
DESCRIPTOR.message_types_by_name['QuestSettings'] = _QUESTSETTINGS

QuestSettings = _reflection.GeneratedProtocolMessageType('QuestSettings', (_message.Message,), dict(
  DESCRIPTOR = _QUESTSETTINGS,
  __module__ = 'pogoprotos.settings.master.quest_settings_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.settings.master.QuestSettings)
  ))
_sym_db.RegisterMessage(QuestSettings)


# @@protoc_insertion_point(module_scope)
