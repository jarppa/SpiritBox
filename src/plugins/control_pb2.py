# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: control.proto

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
  name='control.proto',
  package='spiritbox',
  syntax='proto3',
  serialized_pb=_b('\n\rcontrol.proto\x12\tspiritbox\"-\n\x0e\x43ontrolMessage\x12\r\n\x05\x65vent\x18\x01 \x01(\r\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\tb\x06proto3')
)




_CONTROLMESSAGE = _descriptor.Descriptor(
  name='ControlMessage',
  full_name='spiritbox.ControlMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='event', full_name='spiritbox.ControlMessage.event', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='spiritbox.ControlMessage.data', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
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
  serialized_start=28,
  serialized_end=73,
)

DESCRIPTOR.message_types_by_name['ControlMessage'] = _CONTROLMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ControlMessage = _reflection.GeneratedProtocolMessageType('ControlMessage', (_message.Message,), dict(
  DESCRIPTOR = _CONTROLMESSAGE,
  __module__ = 'control_pb2'
  # @@protoc_insertion_point(class_scope:spiritbox.ControlMessage)
  ))
_sym_db.RegisterMessage(ControlMessage)


# @@protoc_insertion_point(module_scope)
