# -*- coding: utf-8 -*-

from encoder import Encoder
PROTO_TO_CS = {
    "int32": "int",
    "uint32": "uint",
    "bytes": "byte[]",
    "int64": "long",
    "uint64": "ulong",
    "string": "string",
    "float": "float",
}

class CsProtoEncoder(Encoder):
    def __init__(self, package):
        super(CsProtoEncoder, self).__init__()
        self.package = package
        return

    def encode(self):
        print '// 本文件由工具自动生成，请勿直接改动'
        print '''using MongoDB.Bson.Serialization.Attributes;
using System.ComponentModel;
using ProtoBuf;
using System.Collections.Generic;

namespace Base'''

        print '{'
        for msg in self.package.message_list:
            self.encode_message(msg)
        print '}'
        return

    def encode_message(self, msg):
        def HasErrorMessage():
            for field in msg.fields:
                if field.type == 'ErrorMessage':
                    return True

        hasErrorMessage = HasErrorMessage()

        print '\t[ProtoContract]'
        print '\tpublic partial class %s%s' % (msg.name, ': IErrorMessage' if hasErrorMessage else '')
        print '\t{'
        for fd in msg.fields:
            for comment in fd.comments:
                print '\t\t//%s' % comment
            if fd.lable != "optional":
                print '\t\t[ProtoMember(%s)]' % (fd.index)
            else:
                print '\t\t[ProtoMember(%s, IsRequired = false)]' % (fd.index)

            ptype = fd.type
            if ptype in PROTO_TO_CS:
                ptype = PROTO_TO_CS[ptype]

            if fd.lable == "repeated":
                cs_type = "List<%s>" % (ptype)
                default_value = "new List<%s>()" % (ptype)
            else:
                cs_type = ptype
                default_value = ''

                if cs_type == 'byte[]':
                    if fd.default is not None:
                        default_value = fd.default + '.ToByteArray()'
                else:
                    if fd.default is not None:
                        print '\t\t[DefaultValue(%s)]' % (fd.default)
                        default_value = fd.default

            if default_value:
                default_value = ' = %s' % default_value

            print "\t\tpublic %s %s%s;" % (cs_type, fd.name, default_value)
            print ''

        if hasErrorMessage:
            print '\t\tpublic ErrorMessage ErrorMessage { get { return this.errmsg; } }'
        print '\t}'
        print ''
        return


class CsJsonEncoder(Encoder):
    def __init__(self, package):
        super(CsJsonEncoder, self).__init__()
        self.package = package
        return

    def encode(self):
        print '// 本文件由工具自动生成，请勿直接改动'
        print '''using MongoDB.Bson.Serialization.Attributes;
using System.Collections.Generic;
using MongoDB.Bson;

namespace Base'''
        print '{'
        for msg in self.package.message_list:
            self.encode_message(msg)
        print '}'
        return

    def encode_message(self, msg):
        print '\tpublic partial class %s: AConfig' % msg.name
        print '\t{'
        for fd in msg.fields:
            if fd.name == "id":
                continue
            ptype = fd.type
            if ptype in PROTO_TO_CS:
                ptype = PROTO_TO_CS[ptype]

            if fd.lable == "repeated":
                cs_type = "List<%s>" % (ptype)
                default = " = new List<%s>()" % (ptype)
            else:
                cs_type = ptype
                default = ''

                if fd.default != None and ptype != 'byte[]':
                    print '\t\t[BsonDefaultValue((%s)%s)]' % (cs_type, fd.default)

            if fd.type == 'float':
                 print '\t\t[BsonRepresentation(BsonType.Double, AllowTruncation = true)]'
            print '\t\tpublic  %s %s%s;' % (cs_type, fd.name, default)
        print '\t}'



