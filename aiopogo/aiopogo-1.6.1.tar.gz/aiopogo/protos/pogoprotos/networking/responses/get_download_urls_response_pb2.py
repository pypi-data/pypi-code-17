# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/get_download_urls_response.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pogoprotos.data import download_url_entry_pb2 as pogoprotos_dot_data_dot_download__url__entry__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/networking/responses/get_download_urls_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\n@pogoprotos/networking/responses/get_download_urls_response.proto\x12\x1fpogoprotos.networking.responses\x1a(pogoprotos/data/download_url_entry.proto\"S\n\x17GetDownloadUrlsResponse\x12\x38\n\rdownload_urls\x18\x01 \x03(\x0b\x32!.pogoprotos.data.DownloadUrlEntryb\x06proto3')
  ,
  dependencies=[pogoprotos_dot_data_dot_download__url__entry__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_GETDOWNLOADURLSRESPONSE = _descriptor.Descriptor(
  name='GetDownloadUrlsResponse',
  full_name='pogoprotos.networking.responses.GetDownloadUrlsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='download_urls', full_name='pogoprotos.networking.responses.GetDownloadUrlsResponse.download_urls', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_end=226,
)

_GETDOWNLOADURLSRESPONSE.fields_by_name['download_urls'].message_type = pogoprotos_dot_data_dot_download__url__entry__pb2._DOWNLOADURLENTRY
DESCRIPTOR.message_types_by_name['GetDownloadUrlsResponse'] = _GETDOWNLOADURLSRESPONSE

GetDownloadUrlsResponse = _reflection.GeneratedProtocolMessageType('GetDownloadUrlsResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETDOWNLOADURLSRESPONSE,
  __module__ = 'pogoprotos.networking.responses.get_download_urls_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.GetDownloadUrlsResponse)
  ))
_sym_db.RegisterMessage(GetDownloadUrlsResponse)


# @@protoc_insertion_point(module_scope)
