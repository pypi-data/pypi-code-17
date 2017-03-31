# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/use_item_capture_response.proto

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
  name='pogoprotos/networking/responses/use_item_capture_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\n?pogoprotos/networking/responses/use_item_capture_response.proto\x12\x1fpogoprotos.networking.responses\"\xb1\x01\n\x16UseItemCaptureResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x19\n\x11item_capture_mult\x18\x02 \x01(\x01\x12\x16\n\x0eitem_flee_mult\x18\x03 \x01(\x01\x12\x15\n\rstop_movement\x18\x04 \x01(\x08\x12\x13\n\x0bstop_attack\x18\x05 \x01(\x08\x12\x12\n\ntarget_max\x18\x06 \x01(\x08\x12\x13\n\x0btarget_slow\x18\x07 \x01(\x08\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_USEITEMCAPTURERESPONSE = _descriptor.Descriptor(
  name='UseItemCaptureResponse',
  full_name='pogoprotos.networking.responses.UseItemCaptureResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='pogoprotos.networking.responses.UseItemCaptureResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='item_capture_mult', full_name='pogoprotos.networking.responses.UseItemCaptureResponse.item_capture_mult', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='item_flee_mult', full_name='pogoprotos.networking.responses.UseItemCaptureResponse.item_flee_mult', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stop_movement', full_name='pogoprotos.networking.responses.UseItemCaptureResponse.stop_movement', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stop_attack', full_name='pogoprotos.networking.responses.UseItemCaptureResponse.stop_attack', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target_max', full_name='pogoprotos.networking.responses.UseItemCaptureResponse.target_max', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target_slow', full_name='pogoprotos.networking.responses.UseItemCaptureResponse.target_slow', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=101,
  serialized_end=278,
)

DESCRIPTOR.message_types_by_name['UseItemCaptureResponse'] = _USEITEMCAPTURERESPONSE

UseItemCaptureResponse = _reflection.GeneratedProtocolMessageType('UseItemCaptureResponse', (_message.Message,), dict(
  DESCRIPTOR = _USEITEMCAPTURERESPONSE,
  __module__ = 'pogoprotos.networking.responses.use_item_capture_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.UseItemCaptureResponse)
  ))
_sym_db.RegisterMessage(UseItemCaptureResponse)


# @@protoc_insertion_point(module_scope)
