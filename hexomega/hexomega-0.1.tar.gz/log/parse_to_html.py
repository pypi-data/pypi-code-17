from yattag import Doc
from parse import *
import os

from users.models import Project


class parse_log(object):
    def __init__(self, project=None):
        # self.project = project
        # self.logpath = Project.objects.get(name__exact=self.project.name).activitylog.content
        self.logpath = project.activitylog.content
        print(self.logpath)

        if os.path.exists(self.logpath):
            self.logfile = open(self.logpath, 'r')
        else:
            if not os.path.exists('/'.join(self.logpath.split('/')[:-1])):
                print('/'.join(self.logpath.split('/')[:-1]))
                os.makedirs('/'.join(self.logpath.split('/')[:-1]), 0o755)
            self.logfile = open(self.logpath, 'w')
            self.logfile.close()
            self.logfile = open(self.logpath, 'r')
        self.log_data = self.logfile.readlines().reverse()

    def test(self):
        woah = ''

        for line in self.log_data:
            data = parse('[{}] [{}] [{}] [{}] [{}] [{}]', line)

            doc, tag, text = Doc().tagtext()

            if data[0] == 'INFO':
                k = 'info-class'
            elif data[0] == 'WARNING':
                k = 'warning-class'
            else:
                k = 'success-class'
            # if data[0] == 'INFO':
            #     k = 'panel panel-info'
            # elif data[0] == 'WARNING':
            #     k = 'panel panel-warning'
            # else:
            #     k = 'panel panel-warning'

            with tag('div', klass=k):
                # with tag('h4'):
                #     text(data[0])
                with tag('span', klass='username'):
                    text(data[1] + ' ')
                with tag('i'):
                    text(data[4] + ' ')
                with tag('p'):
                    text(data[5])

            woah += doc.getvalue()

        return woah
