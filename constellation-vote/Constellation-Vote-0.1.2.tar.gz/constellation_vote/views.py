import json
import pprint

from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden
)
from django.core import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View

from guardian.shortcuts import assign_perm, remove_perm

from guardian.decorators import (
    permission_required,
    permission_required_or_403,
)

from constellation_base.models import GlobalTemplateSettings

from .models import (
    Ballot,
    BallotItem,
    Poll,
    PollOption
)

from .utils import ip_in_range

# py3votecore provides the base summation mechanisms.  These are all noqa 401
# since they are called indirectly via the locals() table
from py3votecore.stv import STV # noqa 401
from py3votecore.plurality_at_large import PluralityAtLarge # noqa 401
from py3votecore.plurality import Plurality # noqa 401
from py3votecore.irv import IRV # noqa 401


@login_required
def view_list(request, show_closed=False):
    ''' Returns a page that includes a list of submitted forms '''
    template_settings = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings.settings_dict()
    polls = Poll.objects.all()

    active_polls = [p for p in polls
                    if p.is_active
                    and request.user.has_perm("poll_visible", p)]

    closed_polls = None
    try:
        active_pks = []
        for a in active_polls:
            active_pks.append(a.pk)
        closed_polls = [p for p in Poll.objects.all()
                        .exclude(pk__in=active_pks)
                        if request.user.has_perm("poll_visible", p)]

    except TypeError as e:
        print(e)

    if show_closed:
        polls = closed_polls
    else:
        polls = active_polls

    return render(request, 'constellation_vote/list.html', {
        'template_settings': template_settings,
        'polls': polls,
    })


@method_decorator(login_required, name="dispatch")
class manage_poll(View):
    def get(self, request, poll_id=None):
        if not Poll.can_edit(request.user, poll_id):
            return redirect("%s?next=%s" % (
                settings.LOGIN_URL, request.path))
        """ Returns a page that allows for the creation of a poll """
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()

        poll = None
        pollOptions = None

        mechanisms = Poll.MECHANISMS

        # If poll_id was set, get that poll and its options to edit
        if poll_id is not None:
            poll = Poll.objects.get(pk=poll_id)
            pollOptions = serializers.serialize(
                "json", PollOption.objects.filter(poll=poll))

        return render(request, 'constellation_vote/manage-poll.html', {
            'template_settings': template_settings,
            'poll': poll,
            'pollOptions': pollOptions,
            'visible_groups': [(g.name, g.pk) for g in Group.objects.all()],
            'mechanisms': mechanisms
            })

    def post(self, request, poll_id=None):
        """ Creates a poll """
        if not Poll.can_edit(request.user, poll_id):
            return HttpResponseForbidden()
        pollDict = json.loads(request.POST["data"])
        try:
            # Try creating the poll and if that fails, then we won't put in
            # options
            pollInfoDict = pollDict["meta"]
            pollOptionsDict = pollDict["options"]
            poll, c = Poll.objects.get_or_create(pk=poll_id)

            poll.title = pollInfoDict["title"]
            poll.desc = pollInfoDict["desc"]

            if pollOptionsDict["starts"] != "":
                poll.starts = datetime.strptime(pollOptionsDict["starts"],
                                                "%m/%d/%Y %H:%M")
            if pollOptionsDict["ends"] != "":
                poll.ends = datetime.strptime(pollOptionsDict["ends"],
                                              "%m/%d/%Y %H:%M")

            if pollOptionsDict["mechanism"] != "":
                poll.mechanism = next(
                    (i for i, m in Poll.MECHANISMS.items() if
                     pollOptionsDict["mechanism"] == m['name']), -1)

            if poll.mechanism >= 200 and pollOptionsDict["winners"] != "":
                poll.required_winners = pollOptionsDict["winners"]
            else:
                poll.required_winners = 1

            if pollOptionsDict["ip_range"] != "":
                poll.ip_range = pollOptionsDict["ip_range"]

            owning_group = Group.objects.get(name=pollOptionsDict["owner"])
            poll.owned_by = owning_group

            # Checkboxes don't POST if they aren't checked
            if "results_visible" in pollOptionsDict:
                poll.results_visible = True
            else:
                poll.results_visible = False

            if "cast_multiple" in pollOptionsDict:
                poll.cast_multiple = True
            else:
                poll.cast_multiple = False

            poll.full_clean()
            poll.save()

            # Now we create the options
            for optionDict in pollDict["choices"]:
                opt_ID = None
                if "pk" in optionDict and optionDict["pk"]:
                    opt_ID = optionDict["pk"]
                opt, c = PollOption.objects.get_or_create(pk=opt_ID)
                opt.poll = poll
                opt.text = optionDict["text"]
                if "desc" in optionDict:
                    opt.desc = optionDict["desc"]
                if "active" in optionDict:
                    opt.active = optionDict["active"]
                opt.save()
            # If we've made it this far, the poll itself is saved
            # Now we can set the permissions on this object
            visible_group = Group.objects.get(name=pollOptionsDict["visible"])
            assign_perm("poll_visible", visible_group, poll)
            assign_perm("poll_owned_by", owning_group, poll)
            invisibleGroups = Group.objects.all().exclude(pk=visible_group.pk)
            for group in invisibleGroups:
                remove_perm("poll_visible", group, poll)
            assign_perm("poll_visible", owning_group, poll)

        except Group.DoesNotExist:
            if poll_id is None:
                poll.delete()
            return HttpResponseBadRequest("Permission groups must be selected")
        except ValidationError:
            if poll_id is None:
                poll.delete()
            return HttpResponseBadRequest("Poll could not be created!")

        return HttpResponse(pollDict)


@method_decorator(login_required, name="dispatch")
class ballot_view(View):
    @method_decorator(permission_required(
        'constellation_vote.poll_visible', (Poll, 'pk', 'poll_id')))
    def get(self, request, poll_id):
        """Return a ballot for casting or editing"""
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()

        poll = Poll.objects.get(pk=poll_id)

        if(not ip_in_range(request, poll.ip_range)):
            return render(request, 'constellation_vote/error.html', {
                'template_settings': template_settings,
                'message': "Please visit the polling place to cast your vote"
            })

        ballot = None
        selected_options = []
        can_cast = True

        # If user has already filled out the poll once.
        # Return their previous ballot
        if Ballot.objects.filter(poll=poll, owned_by=request.user).exists():

            can_cast = poll.cast_multiple

            ballot = Ballot.objects.get(poll=poll, owned_by=request.user)

            # Maintain order
            selected_option_pks = BallotItem.objects \
                .select_related('poll_option') \
                .filter(ballot=ballot) \
                .values_list('poll_option', flat=True)

            for pk in selected_option_pks:
                selected_options.append(PollOption.objects.get(pk=pk))

            # Everything else
            poll_options = PollOption.objects.filter(poll=poll).exclude(
                pk__in=selected_option_pks)
        else:
            poll_options = PollOption.objects.filter(poll=poll)

        return render(request, 'constellation_vote/ballot.html', {
            'template_settings': template_settings,
            'poll': poll,
            'poll_options': poll_options,
            'selected_options': selected_options,
            'can_cast': can_cast,
            })

    @method_decorator(permission_required_or_403(
        'constellation_vote.poll_visible', (Poll, 'pk', 'poll_id')))
    def post(self, request, poll_id):
        '''Vote or Edit a request'''
        poll = Poll.objects.get(pk=poll_id)
        if not poll.is_active:
            return HttpResponseBadRequest("Attempted to vote in closed poll!")

        try:
            with transaction.atomic():
                ballot, c = Ballot.objects.get_or_create(poll=poll,
                                                         owned_by=request.user)

                if not c and not ballot.poll.cast_multiple:
                    return HttpResponseBadRequest("Vote was already cast.")

                options = json.loads(request.POST['data'])
                if len(options) > poll.required_winners \
                   and poll.mechanism != 201:  # 201 is STV
                    return HttpResponseBadRequest("Too many ballot options!")

                ballot.full_clean()
                ballot.save()
                ballot.selected_options.clear()

                for i, option in enumerate(options):
                    pollOption = PollOption.objects.get(pk=option)
                    item = BallotItem(ballot=ballot,
                                      poll_option=pollOption,
                                      order=i)
                    item.full_clean()
                    item.save()
        except:
            return HttpResponseBadRequest("Vote could not be cast.")

        return HttpResponse()


@login_required
@permission_required('constellation_vote.poll_visible',
                     (Poll, 'pk', 'poll_id'))
def view_poll_results(request, poll_id):
    """Display poll results, summing up the election on load"""
    template_settings = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings.settings_dict()
    poll = Poll.objects.get(pk=poll_id)

    # Get the ballots into the correct form
    b = Ballot.objects.filter(poll=poll)
    ballots = []
    for o in b.iterator():
        ballots.append(o.to_ballot())

    num_votes = len(ballots)

    # Tabulate the results
    results = None
    call = poll.MECHANISMS[poll.mechanism]["callable"]
    if 100 <= poll.mechanism <= 199:
        # Single winner system, don't pass required_winners
        results = globals()[call](ballots)
    elif 200 <= poll.mechanism <= 299:
        # Multiple winner system, pass required_winners
        results = globals()[call](ballots,
                                  required_winners=poll.required_winners)

    # Prepare and finalize the template
    if results is not None:
        results = results.as_dict()
    options = PollOption.objects.filter(poll=poll)
    return render(request, "constellation_vote/view_results.html", {
        'template_settings': template_settings,
        'poll': poll,
        'options': options,
        'results': results,
        'num_votes': num_votes,
    })


@login_required
@staff_member_required
def view_dotmatrix(request, poll_id, s_factor=0):
    """This view generates a view suitable for printing on a dot-matrix
    printer"""
    s_factor = int(s_factor)

    text = []
    poll = Poll.objects.get(pk=poll_id)

    # Leading header
    if len("Poll Opens: " + poll.title) > len(str(poll.starts)):
        headerbar = "="*len(poll.title)
    else:
        headerbar = "="*len(str(poll.starts))

    text.append(headerbar)
    text.append("Poll Opens: " + poll.title)
    text.append(str(poll.starts))
    text.append(headerbar)

    # Ballots
    for ballot in Ballot.objects.filter(poll=poll).iterator():
        line = ""
        line += "[" + ballot.date_cast.strftime("%Y-%m-%e %H:%M") + "] "

        if s_factor >= 3:
            line += "(" \
                    + ballot.owned_by.first_name \
                    + " " + ballot.owned_by.last_name + ") "

        line += str(list(BallotItem.objects
                         .select_related('poll_option')
                         .filter(ballot=ballot)
                         .values_list('poll_option', flat=True)))
        text.append(line)

    # Trailing Footer
    if len("Poll Closes: " + poll.title) > len(str(poll.starts)):
        footerbar = "="*len(poll.title)
    else:
        footerbar = "="*len(str(poll.ends))

    text.append(footerbar)
    text.append("Poll Closes: " + poll.title)
    text.append(str(poll.ends))
    text.append(footerbar)

    # Option Mapping
    text.append("="*len("Option Mapping"))
    text.append("Option Mapping")
    text.append("="*len("Option Mapping"))
    for option in PollOption.objects.filter(poll=poll).iterator():
        text.append("{:>3}: {}".format(option.pk, option.text))

    # Final Results
    text.append("="*len("Final Results"))
    text.append("Final Results")
    text.append("="*len("Final Results"))

    # Get the ballots into the correct form
    b = Ballot.objects.filter(poll=poll)
    ballots = []
    for o in b.iterator():
        ballots.append(o.to_ballot())

    num_votes = len(ballots)

    # Tabulate the results
    results = None
    call = poll.MECHANISMS[poll.mechanism]["callable"]
    if 100 <= poll.mechanism <= 199:
        # Single winner system, don't pass required_winners
        results = globals()[call](ballots)
    elif 200 <= poll.mechanism <= 299:
        # Multiple winner system, pass required_winners
        results = globals()[call](ballots,
                                  required_winners=poll.required_winners)

    # Prepare and finalize the template
    if results is not None:
        results = results.as_dict()

    # Add just the winner/winners
    if "winner" in results:
        text.append(results["winner"])
    else:
        for winner in results["winners"]:
            text.append("  - {}".format(winner))

    # Voter ID?
    if s_factor >= 2:
        text.append("="*len("Participants ({0})".format(num_votes)))
        text.append("Participants ({0})".format(num_votes))
        text.append("="*len("Participants ({0})".format(num_votes)))

        # Output names but not who they voted for
        for ballot in Ballot.objects.filter(poll=poll).iterator():
            text.append("  - {}".format(ballot.owned_by.first_name + " " + ballot.owned_by.last_name))

    if s_factor >= 1:
        # Verbose Mechanism Output
        text.append("="*len("Verbose Mechanism Output"))
        text.append("Verbose Mechanism Output")
        text.append("="*len("Verbose Mechanism Output"))
        text.append(pprint.pformat(results))

    return HttpResponse("\n".join(text))

# -----------------------------------------------------------------------------
# Dashboard
# -----------------------------------------------------------------------------


@login_required
def view_dashboard(request):
    '''Return a card that will appear on the main dashboard'''

    return render(request, 'constellation_vote/dashboard.html')
