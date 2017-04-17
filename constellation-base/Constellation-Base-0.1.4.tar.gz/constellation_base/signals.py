from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from django.contrib.auth.models import Group

from .models import LocalGroupACLEntry


@receiver(user_logged_in)
def addSupplementalGroups(sender, user, request, **kwargs):
    """Apply additional groups on login"""
    supGroups = LocalGroupACLEntry.objects.filter(username=user.username)

    for group in supGroups.iterator():
        group.group.user_set.add(user)


@receiver(user_logged_in)
def add_to_default_group(sender, user, request, **kwargs):
    group, _ = Group.objects.get_or_create(name="<All Users>")
    user.groups.add(group)
