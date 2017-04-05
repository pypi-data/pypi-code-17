from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin
import itertools
from guardian.mixins import GuardianUserMixin

import os
from HexOmega.settings import BASE_DIR


class User(AbstractUser, GuardianUserMixin):
    # username = models.CharField(max_length=30, primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    is_admin = False
    is_leader = False
    is_member = False
    phone = models.TextField(max_length=15, blank=True)
    email = models.EmailField(unique=True, blank=True)

    def __str__(self):
        return self.get_full_name()


class AdminUser(User, PermissionsMixin):
    """
    Class that hold data for every admin level user.
    Most of the fields are inherited from AbstractUser.
    """
    is_admin = True

    class Meta:
        db_table = 'AdminUser'
        permissions = (
            ('can_create_admin', 'Can create Admin'),
        )


@receiver(post_save, sender=AdminUser)
def add_admin_to_group(sender, **kwargs):
    """
    Runs as soon as any AdminUser object is saved.
    Creates/adds to the admin group and permissions are given
    to the admin group.

    :param sender: AdminUser
    :param kwargs: list of essential arguments
    :return: None
    """

    admin_group, created = Group.objects.get_or_create(name='admin_group')
    if created:
        pass
    if kwargs['instance'].username != 'AnonymousUser':
        admin_group.user_set.add(kwargs.get('instance'))


class LeaderUser(User, PermissionsMixin):
    is_leader = True

    class Meta:
        db_table = 'Leader'
        permissions = (
            ('can_create_leader', 'Can create Team Leader'),
        )


@receiver(post_save, sender=LeaderUser)
def add_leader_to_group(sender, **kwargs):
    """
    Runs as soon as any LeaderUser object is saved.
    Creates/adds to the leader group and permissions are given
    to the leader group.

    :param sender: LeaderUser
    :param kwargs: list of essential arguments
    :return: None
    """
    leader_group, created = Group.objects.get_or_create(name='leader_group')
    if created:
        pass
    if kwargs['instance'].username != 'AnonymousUser':
        leader_group.user_set.add(kwargs.get('instance'))


class Role(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Role'


class Project(models.Model):
    """
    Model changelog:
        1.  have to add null=True for the date fields.
    """

    @property
    def get_name(self):
        return self.name

    name = models.CharField(max_length=50, blank=False, unique=True)
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Closed', 'Closed')
    )
    status = models.CharField(choices=STATUS_CHOICES, default=0, max_length=7)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    description = models.TextField(max_length=500, blank=True)
    leader = models.OneToOneField(LeaderUser, models.DO_NOTHING)
    admins = models.ManyToManyField(AdminUser)

    def path(self):
        return os.path.join(BASE_DIR,
                            os.path.join('projects', self.name + '/'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Project'


@receiver(post_save, sender=Project)
def add_activitylog(sender, instance, created, **kwargs):
    if created:
        print(instance.name)
        c = os.path.join(BASE_DIR,
                         os.path.join('projects',
                                      os.path.join(instance.name, 'activity.log')))
        print(c)
        print('/'.join(c.split('/')[:-1]))
        instance.path = '/'.join(c.split('/')[:-1]) + '/'
        # instance.save()
        ActivityLog.objects.create(title=instance.name, project=instance, content=c)
        if not os.path.exists('/'.join(c.split('/')[:-1])):
            os.makedirs('/'.join(c.split('/')[:-1]), 0o755)
        f = open(c, 'w+')
        f.close()


@receiver(post_save, sender=Project)
def add_actionlist(sender, instance, created, **kwargs):
    if created:
        ActionList.objects.create(name=instance.name, project=instance)


class ActionList(models.Model):
    name = models.CharField(max_length=30)
    project = models.OneToOneField(Project)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ActionList'


class MemberUser(User, PermissionsMixin):
    role = models.ForeignKey(Role, models.DO_NOTHING)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    # tasks = models.ManyToManyField(Task)
    is_member = True

    class Meta:
        db_table = 'Member'
        permissions = (
            ('can_create_member', 'Can create Team Member'),
        )


def get_path(instance, filename):
    p = instance.action_list.project.path()
    print(p)
    if type(filename) is str:
        f = os.path.join(p, filename)
    else:
        f = os.path.join(p, filename.name)
    print(f)
    return f


def get_student_list(project):
    m = project.memberuser_set.all()
    l = project.leader
    students = list(m)
    students.append(l)
    for s in students:
        print(str(s.username) + ' -- ' + str(type(s)))
    return [s.username for s in students]


class Task(models.Model):
    """
        Model Changelog:
            1.  have to add members_assigned as a many to many relation.
                (a task can have many members and many tasks can be done by
                one member)
    """
    TASK_STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Final', 'Final'),
        ('Unassigned', 'Unassigned'),
        ('Assigned', 'Assigned'),
        ('Completed', 'Completed'),
        ('Late', 'Late'),
        ('Not Submitted', 'Not Submitted')
    )
    status = models.CharField(choices=TASK_STATUS_CHOICES, max_length=14, default=2, blank=False)
    start_date = models.DateTimeField(auto_now=True)
    est_end = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=50)
    action_list = models.ForeignKey(ActionList, models.CASCADE, null=True, blank=True)
    deliverable = models.FileField(upload_to=get_path, blank=True, null=True)
    to_leader = models.NullBooleanField(verbose_name="Is the leader working on this Task?", null=True)
    members = models.ManyToManyField(MemberUser)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Task'


class ActivityLog(models.Model):
    title = models.CharField(max_length=30)
    # the content variable is the path to the actual log file.
    content = models.TextField(max_length=100, blank=True, null=True)
    project = models.OneToOneField(Project)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ActivityLog'

# @receiver(post_save, sender=MemberUser)
# def add_member_to_group(sender, instance, created, **kwargs):
#     """
#     Runs as soon as any MemberUser object is saved.
#     Creates/adds to the member group and permissions are given
#     to the member group.
#
#     :param created:
#     :param instance: instance of member user
#     :param sender: MemberUser
#     :param kwargs: list of essential arguments
#     :return: None
#     """
#     if created and instance.username != 'AnonymousUser':
#         # member_group.user_set.add(kwargs.get('instance'))
#         instance.groups.add(Group.objects.get_or_create(name='member_group'))
