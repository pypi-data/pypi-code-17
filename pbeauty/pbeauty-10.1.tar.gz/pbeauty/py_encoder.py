# -*- coding: utf-8 -*-

from encoder import Encoder
import typedef

class PyJsonEncoder(Encoder):
    def __init__(self, package):
        super(PyJsonEncoder, self).__init__()
        self.package = package
        return

    def encode(self):
        print '# -*- coding: utf-8 -*-'
        print "'''"
        print '本文件由工具自动生成，请勿直接改动'
        print "'''"
        for msg in self.package.message_list:
            self.encode_message(msg)
        return

    def encode_message(self, msg):
        print 'class %s(object):' % msg.name
        print '\tdef __init__(self):'
        for fd in msg.fields:
            default = fd.default
            print '\t\tself.%s=%s' % (fd.name, default)

        print ''
        print '\tdef to_json(self):'
        print '\t\treturn {'
        for fd in msg.fields:
            print '\t\t\t"%s": self.%s,' % (fd.name, fd.name)
        print '\t\t}'


        print ''
        print '\tdef from_json(self, js):'
        for fd in msg.fields:
            default = fd.default
            if typedef.Types.IsBasicalType(fd.type):
                print '\t\tself.%s = js.get("%s", %s)' % (fd.name, fd.name, default)
            else:
                print '\t\t%s = js.get("%s", None)' % (fd.name, fd.name)
                print '\t\tif %s is not None:' % (fd.name)
                print '\t\t\tself.%s = %s()' % (fd.name, fd.type)
                print '\t\t\tself.%s.from_json(%s)' % (fd.name, fd.name)
        print '\t\treturn'
        print ''




