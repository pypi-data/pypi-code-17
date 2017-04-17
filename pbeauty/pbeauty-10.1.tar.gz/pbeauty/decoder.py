# -*- coding: utf-8 -*-

from errors import DecodeError
from descriptor import FieldDescriptor, MessageDescriptor, EnumDescriptor, PackageDescriptor
from scanner import Context, IntScanner, StringScanner, EnumScanner, ScannerHelper
from typedef import Lable, Types

import os

class FieldDecoder(object):
    def __init__(self, package, message, context):
        self.package = package
        self.message = message
        self.context = context
        return

    def decode(self):
        context = self.context
        lable = None
        for l in Lable.LABLE_ENUM:
            if context.findstring(l):
                lable = l
                break
        if not lable:
            if context.line()[:1] != '}':
                raise context.error('Expected "required", "optional", or "repeated".')
            return

        field_type = context.findraw()
        if not field_type:
            raise context.error("Expected type name.")

        if not Types.IsBasicalType(field_type) \
                and field_type not in self.package.user_types:
            raise context.error('"%s" is not defined.' % field_type)

        field_name = context.findraw()
        if not field_name:
            raise context.error("Expected field name.")

        context.findstring('=', alert = True)

        index = context.findraw(IntScanner(negetive = False))
        if not index:
            raise context.error("Expected field number.")

        default = None
        if context.findstring('['):
            if lable == Lable.LABLE_REPEATED:
                raise DecodeError(context, "Repeated fields can't have default values.")

            if Types.IsBasicalType(field_type):
                scanner = ScannerHelper.TypeToScanner(field_type)
            else:
                msg = self.package.user_types[field_type]
                if msg.IS_ENUM:
                    scanner = EnumScanner
                else:
                    raise DecodeError(context, "Messages can't have default values.")

            context.findstring('default', alert = True)
            context.findstring('=', alert = True)

            scanner = scanner()
            default = context.findraw(scanner)
            if not default:
                raise context.error(scanner.ERROR)
            default = scanner.value()

            context.findstring(']', alert = True)
        context.findstring(';', alert = True)
        return FieldDescriptor(lable, field_type, field_name, index, default, context.get_comments())

class MessageDecoder(object):
    def __init__(self, package, context):
        self.package = package
        self.context = context
        return

    def decode(self):
        context = self.context
        messagename = context.findraw()
        if not messagename:
            raise DecodeError(context, 'Expected message name.')

        context.findstring('{', alert = True)

        comments = context.get_comments()
        fields = []
        while not context.findstring('}'):
            context.skip_semicolon()
            if context.eof():
                raise context.error("Reached end of input in message definition (missing '}').")
            field = FieldDecoder(self.package, self, context).decode()
            if field:
                fields.append(field)
            else:
                break
        context.findstring(';', alert = False)
        return MessageDescriptor(messagename, fields, comments)

class EnumDecoder(object):
    def __init__(self, context):
        self.context = context
        return

    def decode(self):
        context = self.context
        enumname = context.findraw()
        if not enumname:
            raise context.error('Expected enum name.')
        context.findstring('{', alert = True)
        comments = context.get_comments()

        fields = []
        while True:
            context.skip_semicolon()
            if context.eof():
                raise context.error("Reached end of input in enum definition (missing '}').")
            if context.findstring('}'):
                break

            name = context.findraw()
            if not name:
                raise context.error("Expected enum constant name.")

            context.findstring('=', alert = True)
            scanner = IntScanner(negetive = False)
            if not context.findraw(scanner):
                raise context.error("Missing numeric value for enum constant.")

            context.findstring(';', alert = True)
            fields.append((name, scanner.value(), context.get_comments()))
        context.findstring(';', alert = False)
        return EnumDescriptor(enumname, fields, comments)

class PackageDecoder(object):
    def __init__(self, context):
        self.context = context
        self.namespaces = []
        self.imports = []
        self.message_list = []
        self.user_types = {}
        return

    def scan_package(self):
        context = self.context
        if self.namespaces:
            raise context.error("Multiple package definitions.")

        packages = []
        while True:
             package = context.findraw()
             if not package:
                 raise context.error('Expected identifier.')
             packages.append(package)

             if not context.findstring('.'):
                 break

        context.findstring(';', alert = True)
        self.namespaces = packages
        return

    def scan_message(self):
        msg = MessageDecoder(self, self.context).decode()
        self.message_list.append(msg)
        self.user_types[msg.name] = msg
        return

    def scan_enum(self):
        msg = EnumDecoder(self.context).decode()
        self.message_list.append(msg)
        self.user_types[msg.name] = msg
        return

    def scan_import(self):
        context = self.context
        scanner = StringScanner()
        context.findraw(scanner)
        filename = scanner.value()
        if not filename:
            raise context.error('Expected a string naming the file to import.')
        filename = filename[1:len(filename)-1]
        context.findstring(';', alert = True)

        if not filename:
            return
        if filename in self.imports:
            raise context.error('Import "%s" was listed twice.' % (filename))
        if not os.path.exists(filename):
            raise context.error("%s File not found." % filename)

        self.imports.append(filename)

        decoder = PackageDecoder(Context(filename))
        package = decoder.decode()
        for msg in package.message_list:
            self.user_types[msg.name] = msg
        return

    def decode(self):
        context = self.context
        while True:
            context.skip_semicolon()
            if context.eof():
                break
            string = context.findraw()
            if string == 'package':
                self.scan_package()
            elif string == 'message':
                self.scan_message()
            elif string == 'enum':
                self.scan_enum()
            elif string == 'import':
                self.scan_import()
            else:
                raise context.error('Expected top-level statement (e.g. "message").')
        return PackageDescriptor(context.filename, self.namespaces, self.imports, self.message_list)

def Decode(filename):
    context = Context(filename)
    return PackageDecoder(context).decode()

