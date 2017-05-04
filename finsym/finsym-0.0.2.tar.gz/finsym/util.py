import sys
import symbols

_py_version = sys.version.split(' ')[0]

if _py_version > '3.4.0':
    from serialize3.serializers import to_serializable
else:
    from serialize2 import to_serializable

serializer = to_serializable
deserializer = symbols.from_serialized
