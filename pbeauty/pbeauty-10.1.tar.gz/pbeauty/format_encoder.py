# -*- coding: utf-8 -*-

from _utils import StdoutToBuffer

class FormatEncoder(object):
    def __init__(self, package_descriptor):
        self.package_descriptor = package_descriptor
        return

    def encode(self):
        return StdoutToBuffer(self._encode)

    def _encode(self):
        if self.package_descriptor.imports:
            for importfile in self.package_descriptor.imports:
                print 'import "%s";' % importfile
            print ''

        if self.package_descriptor.namespaces:
            print 'package %s;' % ('.'.join(self.package_descriptor.namespaces))
            print ''

        for msg in self.package_descriptor.message_list:
            if msg.IS_ENUM:
                self._encode_enum(msg)
            else:
                self._encode_message(msg)
        return


    def _encode_enum(self, msg):
        for comment in msg.comments:
            print '// %s' % comment
        print 'enum %s {' % msg.name

        max_name_length = 0
        for name, _, _ in msg.fields:
            if len(name) > max_name_length:
                max_name_length = len(name)

        formats = '  %%-%ds = %%s;' % (max_name_length)
        for name, value, comments in msg.fields:
            for comment in comments:
                print '  // %s' % comment
            print formats % (name, value)
        print '};'
        print ''

    def _encode_message(self, msg):
        for comment in msg.comments:
            print '// %s' % comment
        print 'message %s {' % msg.name
        max_name_length = 0
        max_type_length = 0
        max_index_length = 0
        for fd in msg.fields:
            if len(fd.name) > max_name_length:
                max_name_length = len(fd.name)
            if len(fd.type) > max_type_length:
                max_type_length = len(fd.type)
            if len(fd.index) > max_index_length:
                max_index_length = len(fd.index)

        format1 = '  %%s %%-%ds %%-%ds = %%-%ds [default=%%s];' % (max_type_length, max_name_length, max_index_length)
        format2 = '  %%s %%-%ds %%-%ds = %%s;' % (max_type_length, max_name_length)

        for fd in msg.fields:
            for comment in fd.comments:
                print '  // %s' % comment
            if fd.default is not None:
                print format1 % (fd.lable, fd.type, fd.name, fd.index, fd.default)
            else:
                print format2 % (fd.lable, fd.type, fd.name, fd.index)

        print '};\n'



