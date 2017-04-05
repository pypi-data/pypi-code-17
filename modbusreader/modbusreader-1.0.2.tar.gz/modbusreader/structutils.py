"""structutils.py: extends the function of the struct package"""
import struct

__author__ = "Stephan Müller"
__copyright__ = "2017, Stephan Müller"
__license__ = "MIT"


_data_types = {
    "int16": "h",
    "int32": "H",
    "uint32": "I",
    "float": "f",
    "byte": "x",
    "boolean": "?"
}


def get_format(data_type):
    """
    Get struct format type from human readable data type

    :param data_type: human readable data type. One of: int16, int32, uint32, float, byte, boolean
    :type data_type: str
    :return: struct format type
    :type: str
    """
    try:
        return _data_types[data_type]
    except KeyError:
        raise ValueError("format for given data type does not exist")


def calcsize(data_type):
    """
    Return size in bytes of the struct described by the given data type

    :param data_type: human readable data type. One of: int16, int32, uint32, float, byte, boolean
    :type data_type: str
    :return: size in bytes of the struct described by the given data type
    :type: int
    """
    return struct.calcsize(get_format(data_type))


def int16list_to_bytes(int16_list):
    """
    Packs all given integer values into bytes object

    :param int16_list: list containing unsigned 16 bit integers
    :type int16_list: list of int
    :return: packed integer values
    :type: bytes
    """
    byte_list = b''
    for int16_value in int16_list:
        byte_list += struct.pack(">H", int16_value)
    return byte_list


def bytes_to_datatype(byte_list, data_type):
    """
    Unpacks a bytes object to the given data type

    :param byte_list: bytes object
    :type byte_list: bytes
    :param data_type: human readable data type. One of: int16, int32, uint32, float, byte, boolean
    :type data_type: str
    :return: unpacked value
    :type: int, float, byte, boolean

    :raise ValueError: If size of data type is not equal to the size of the bytes object.
    """
    if calcsize(data_type) != len(byte_list):
        raise ValueError("Given data type (" + data_type + ") requires different length of bytes." +
                         " Given: " + str(len(byte_list)) + ", required: " + str(calcsize(data_type)))
    return struct.unpack(">" + get_format(data_type), byte_list)[0]
