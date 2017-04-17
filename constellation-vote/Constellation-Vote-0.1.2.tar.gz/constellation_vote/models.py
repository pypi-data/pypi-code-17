from django.utils import timezone

from django.contrib.auth.models import User, Group
from django.db import models
from guardian.shortcuts import get_groups_with_perms


class Poll(models.Model):
    """ Model for the Poll Itself """
    title = models.CharField(max_length=128)
    desc = models.TextField(blank=True, null=True)

    starts = models.DateTimeField(default=timezone.now)
    ends = models.DateTimeField(blank=True, null=True)

    owned_by = models.ForeignKey(Group, null=True, blank=True)
    results_visible = models.BooleanField(default=False)

    ip_range = models.TextField(default="0.0.0.0/0")

    # The mechanisms need to be identified in such a way that we can add more
    # later if needed without changing the way results for previous elections
    # are setup.  This can be achieved by just assigning them consecurively,
    # but for some semblance of sanity in the data in the database, we use the
    # following convention:

    # -1: mechanism unset
    # 00-99: Special mechanisms (reserved)
    # 100-199: Single Winner
    # 200-299: Multiple Winner

    # The following mechanisms are supported by py3votecore and have IDs
    # allocated:

    # 100: Plurality
    # 101: Instant Runoff
    # 200: Plurality at Large
    # 201: Single Transferrable Vote
    MECHANISMS = {
        -1: {
            "callable": "None",
            "name": "Unset Mechanism",
            },
        100: {
            "callable": "Plurality",
            "name": "Plurality (First-Past-The-Post)",
            "limit_ballot": True
            },
        101: {
            "callable": "IRV",
            "name": "Instant Runoff",
            "limit_ballot": True
            },
        200: {
            "callable": "PluralityAtLarge",
            "name": "PluralityAtLarge",
            "limit_ballot": True
            },
        201: {
            "callable": "STV",
            "name": "Single Transferrable Vote",
            }
        }

    mechanism = models.IntegerField(default=-1)

    required_winners = models.IntegerField(default=1)
    cast_multiple = models.BooleanField(default=True)

    archived = models.BooleanField(default=False)

    @classmethod
    def can_edit(cls, user, poll_id):
        """ Returns whether or not the user provided has permission to edit a
        new or existing poll """
        if (poll_id is None):
            return user.has_perm("constellation_vote.add_poll")
        else:
            poll = cls.objects.filter(pk=poll_id).first()
            return (user.has_perm("constellation_vote.poll_owned_by", poll) or
                    user.has_perm("constellation_vote.add_poll"))

    @property
    def is_active(self):
        """ Returns whether or not the poll is active """
        now = timezone.now()
        return self.starts <= now <= self.ends

    @property
    def visible_by(self):
        """ Returns the group that has the poll_visible permission """
        perms = get_groups_with_perms(self, attach_perms=True)
        if perms:
            return list(filter(lambda x: 'poll_visible' in perms[x] and
                               'poll_owned_by' not in perms[x],
                               perms.keys()))[0]
        else:
            return ""

    class Meta:
        permissions = (
            ("poll_owned_by", "Poll Owner"),
            ("poll_visible", "Poll is Visible")
        )


class PollOption(models.Model):
    """Model for the individual Poll Options"""
    poll = models.ForeignKey(Poll,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    text = models.CharField(blank=True, null=True, max_length=75)
    desc = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.text


class Ballot(models.Model):
    """A filled out ballot from the Poll"""
    poll = models.ForeignKey(Poll)
    owned_by = models.ForeignKey(User)

    date_cast = models.DateTimeField(auto_now=True)

    selected_options = models.ManyToManyField(PollOption, through='BallotItem')

    def to_ballot(self):
        ballot = {}
        ballot["count"] = 1
        items = list(BallotItem.objects.filter(ballot=self))
        items.sort(key=lambda x: x.order)
        ballot["ballot"] = []
        for item in items:
            if item.poll_option.active:
                ballot["ballot"].append(item.poll_option.text)
        return ballot

    class Meta:
        unique_together = (("poll", "owned_by"),)


class BallotItem(models.Model):
    """Intermediary relation model for many-to-many"""
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    poll_option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    # We need an order field, because django does not guarantee order on the
    # primary keys
    order = models.IntegerField()

    def __str__(self):
        return "{0} ({1})".format(self.poll_option, self.order)

    class Meta:
        unique_together = (("ballot", "poll_option"), ("ballot", "order"))
        ordering = ['order']
