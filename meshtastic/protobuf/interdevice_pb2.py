# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: meshtastic/protobuf/interdevice.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'meshtastic/protobuf/interdevice.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%meshtastic/protobuf/interdevice.proto\x12\x13meshtastic.protobuf\"s\n\nSensorData\x12.\n\x04type\x18\x01 \x01(\x0e\x32 .meshtastic.protobuf.MessageType\x12\x15\n\x0b\x66loat_value\x18\x02 \x01(\x02H\x00\x12\x16\n\x0cuint32_value\x18\x03 \x01(\rH\x00\x42\x06\n\x04\x64\x61ta\"_\n\x12InterdeviceMessage\x12\x0e\n\x04nmea\x18\x01 \x01(\tH\x00\x12\x31\n\x06sensor\x18\x02 \x01(\x0b\x32\x1f.meshtastic.protobuf.SensorDataH\x00\x42\x06\n\x04\x64\x61ta*\xd5\x01\n\x0bMessageType\x12\x07\n\x03\x41\x43K\x10\x00\x12\x15\n\x10\x43OLLECT_INTERVAL\x10\xa0\x01\x12\x0c\n\x07\x42\x45\x45P_ON\x10\xa1\x01\x12\r\n\x08\x42\x45\x45P_OFF\x10\xa2\x01\x12\r\n\x08SHUTDOWN\x10\xa3\x01\x12\r\n\x08POWER_ON\x10\xa4\x01\x12\x0f\n\nSCD41_TEMP\x10\xb0\x01\x12\x13\n\x0eSCD41_HUMIDITY\x10\xb1\x01\x12\x0e\n\tSCD41_CO2\x10\xb2\x01\x12\x0f\n\nAHT20_TEMP\x10\xb3\x01\x12\x13\n\x0e\x41HT20_HUMIDITY\x10\xb4\x01\x12\x0f\n\nTVOC_INDEX\x10\xb5\x01\x42\x66\n\x13\x63om.geeksville.meshB\x11InterdeviceProtosZ\"github.com/meshtastic/go/generated\xaa\x02\x14Meshtastic.Protobufs\xba\x02\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'meshtastic.protobuf.interdevice_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\023com.geeksville.meshB\021InterdeviceProtosZ\"github.com/meshtastic/go/generated\252\002\024Meshtastic.Protobufs\272\002\000'
  _globals['_MESSAGETYPE']._serialized_start=277
  _globals['_MESSAGETYPE']._serialized_end=490
  _globals['_SENSORDATA']._serialized_start=62
  _globals['_SENSORDATA']._serialized_end=177
  _globals['_INTERDEVICEMESSAGE']._serialized_start=179
  _globals['_INTERDEVICEMESSAGE']._serialized_end=274
# @@protoc_insertion_point(module_scope)
