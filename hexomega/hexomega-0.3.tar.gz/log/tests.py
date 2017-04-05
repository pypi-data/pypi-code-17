from django.test import TestCase
from parse import *

from datetime import datetime, timedelta

from log.Log import log
from users.models import *


# Create your tests here.
class LogTest(TestCase):
    def setUp(self):
        # Create role.
        r = Role()
        r.title = 'Security Coordinator'
        r.save()

        # Create admin
        adm = AdminUser(username='G2503472', first_name='admin', last_name='man')
        adm.email = 'admin_man@example.com'
        adm.set_password('qwerty123')
        adm.save()

        # Create leader
        l = LeaderUser(username='69497604', first_name='leader', last_name='man')
        l.email = 'leader_man@example.com'
        l.set_password('qwerty123')
        l.save()

        # Create project
        p = Project(name='Test')
        p.start_date = datetime.now()
        p.end_date = datetime.now() + timedelta(days=30)
        p.leader_id = l.id
        p.save()
        p.admins.add(adm)
        p.save()

        # Create member
        m = MemberUser(username='56475644', first_name='Heracles', last_name='Alcmene')
        m.set_password('qwerty123')
        m.email = 'heracles@example.com'
        m.role_id = r.id
        m.project_id = p.id
        m.save()

        n = MemberUser(username='40475328', first_name='Perseus', last_name='Son of Danae')
        n.set_password('qwerty123')
        n.email = 'perseus@example.com'
        n.role_id = r.id
        n.project_id = p.id
        n.save()

        o = MemberUser(username='81343691', first_name='Apollo', last_name='Son of Leto')
        o.set_password('qwerty123')
        o.email = 'apollo@example.com'
        o.role_id = r.id
        o.project_id = p.id
        o.save()

    def Test_log_contains_info_member(self):
        m = MemberUser.objects.get(first_name__exact='Heracles')
        p = m.project
        log('INFO', m, 'test content')
        f = open(p.activitylog.content, 'r')
        logfile = f.readlines()[0]
        data = parse('[{}] [{}] [{}] [{}] [{}] [{}]', logfile)
        TestCase.assertEquals(self, data[0], 'INFO')
        TestCase.assertEquals(self, data[1], m.get_full_name())
        TestCase.assertEquals(self, data[2], 'MEMBER')
        TestCase.assertEquals(self, data[3], m.project.name)
        TestCase.assertEquals(self, data[5], 'test content')
        f.flush()
        f.close()

    def Test_log_contains_warning_leader(self):
        l = LeaderUser.objects.get(first_name__exact='leader')
        p = l.project
        log('WARNING', l, 'leader log record')
        f = open(p.activitylog.content, 'r')
        logfile = f.readlines()[1]
        data = parse('[{}] [{}] [{}] [{}] [{}] [{}]', logfile)
        TestCase.assertEquals(self, data[0], 'WARNING')
        TestCase.assertEquals(self, data[1], l.get_full_name())
        TestCase.assertEquals(self, data[2], 'LEADER')
        TestCase.assertEquals(self, data[3], l.project.name)
        TestCase.assertEquals(self, data[5], 'leader log record')
        f.flush()
        f.close()

    def test_log_contains_all_records(self):
        """
        We have added two records, one each for leader and admin.
        This functions asserts if the log file contains two records.
        To make it more comprehensive, after the initial assertion,
        another record is add to the log and the number of records
        are tested once again.

        It calls the previous two methods so the logs are within the same
        execution context.
        :return:
        """
        self.Test_log_contains_info_member()
        self.Test_log_contains_warning_leader()

        p = Project.objects.get(name__exact='Hell')

        f = open(p.activitylog.content, 'r')
        logfile = f.readlines()
        number_of_lines = len(logfile)
        TestCase.assertEquals(self, number_of_lines, 2)
        f.close()
        os.remove(p.activitylog.content)
        s = '/'.join(p.activitylog.content.split('/')[:-1])
        os.rmdir(s)
