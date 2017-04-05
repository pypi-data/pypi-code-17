# @author: Abhi Rudra
# utilities for the backend services.
import schedule
from django.core.mail import send_mail, send_mass_mail
from haikunator import haikunator
from twilio.rest import TwilioRestClient
from datetime import datetime, timedelta
import time
import _thread
import os

from log.Log import log
from users.models import MemberUser

sys_email = 'hex.omega@yandex.com'


def get_default_password():
    h = haikunator.Haikunator()
    return h.haikunate()


def mail_kickoff(*args, var=1, **kwargs):
    if var is 1:
        _thread.start_new_thread(send_default_password_threads, (args[0], args[1]))
    elif var is 2:
        _thread.start_new_thread(send_reminder_threads, (args[0],))
    elif var is 3:
        _thread.start_new_thread(send_upload_update, (args[0], args[1]))


def send_upload_update(user, task):
    subject = 'Upload Update - ' + task.title
    body = 'Deliverable for task:[{}] has been uploaded by {}'.format(task.title, user.get_full_name())
    l = [m.email for m in task.members.all()]
    l.append(task.action_list.project.leader.email)
    l.extend([a.email for a in task.action_list.project.admins.all()])
    send_mail(
        subject,
        body,
        sys_email,
        l,
        fail_silently=False
    )


def send_default_password_threads(user, password, **kwargs):
    subject = 'Password - Hex Omega Systems'
    body = 'Password for {}({}) is {}\n\n'.format(user.get_full_name(), user.username, password)
    print(password)
    body += 'Please login and change your password, under Profile->Edit Profile.\n'
    send_mail(
        subject,
        body,
        sys_email,
        [user.email],
        fail_silently=False
    )


def start_schedule_thread():
    print('Yo')
    _thread.start_new_thread(tasks_email_schedule, ())


def tasks_email_schedule():
    from users.models import Project
    print('Haha')
    for project in Project.objects.all():
        print(project.name)
        send_mail(
            'test_scheduler',
            'This is a test for the scheduler. \nPlease ignore.\n' + project.name,
            sys_email,
            ['avsv96@gmail.com'],
            fail_silently=False
        )
        lp = []
        for task in project.actionlist.task_set.all():
            if task.est_end.date() < datetime.now().date():
                for m in task.members.all():
                    log('WARNING', m, '{} is late in submission of deliverable for {}'.format(m.username, task.title))
                if task.to_leader is True:
                    log('WARNING', task.action_list.project.leader,
                        '{} is late in submission of deliverable for {}'.format(
                            task.action_list.project.leader.username, task.title))
            if task.est_end.date() - timedelta(days=1) == datetime.now().date():
                if task.status is not 'Completed' and task.status is not 'Unassigned':
                    l = [member.email for member in task.members.all() if member.email is not '']
                    if task.to_leader:
                        l.append(task.action_list.project.leader.email)
                    sub = task.action_list.project.name + ' : ' + task.title
                    msg = 'This is an automated reminder to submit your deliverable before tomorrow.\n\n'
                    msg += 'Please do not reply to this mail.'
                    t = (sub, msg, sys_email, l)
                    print(t, file=open('mass_mail_log.txt', 'w+'))
                    lp.append(t)

        if len(lp) is not 0:
            mail_kickoff(lp, var=2)
            print(lp, file=open('tasks.txt', 'w+'))


def send_reminder_threads(mails, **kwargs):
    send_mass_mail(
        tuple(mails),
        fail_silently=False
    )


def uploaded_file_handler(f, path):
    with open(os.path.join(path, f.name), 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def project_deadline_schedule():
    from users.models import Project
    print('Haha')
    for project in Project.objects.all():
        print(project.name)
        send_mail(
            'test_scheduler',
            'This is a test for the scheduler. \nPlease ignore.\n' + project.name,
            sys_email,
            ['avsv96@gmail.com'],
            fail_silently=False
        )
        lp = []
        if project.end_date == datetime.now() + timedelta(days=2):
            l = [member.email for member in MemberUser.objects.filter(project__name=project.name)]
            l.append(project.leader.email)
            sub = project.name + ' Project Closing Notice'
            msg = 'This is an automated alert. This project will be closed in two days.\n\n'
            msg += 'Please do not reply to this mail.'
            t = (sub, msg, sys_email, l)
            print(t, file=open('mass_mail_log.txt', 'w+'))
            lp.append(t)

        if project.end_date == datetime.now():
            project.status = '1'
            project.save()

        if len(lp) is not 0:
            mail_kickoff(lp, var=2)
            print(lp, file=open('tasks.txt', 'w+'))
