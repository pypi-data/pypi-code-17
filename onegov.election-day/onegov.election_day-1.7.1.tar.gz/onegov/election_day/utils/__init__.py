from hashlib import sha256
from onegov.ballot import Election, Vote, Ballot
from onegov.election_day.models import ArchivedResult


def handle_headerless_params(request):
    if 'headerless' in request.params:
        request.browser_session['headerless'] = True
    if 'headerful' in request.params:
        if request.browser_session.has('headerless'):
            del request.browser_session['headerless']


def add_last_modified_header(response, last_modified):
    """ Adds the give date to the response as Last-Modified header. """

    if last_modified:
        response.headers.add(
            'Last-Modified',
            last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")
        )


def get_election_summary(election, request, url=None):
    """ Returns some basic informations about the given election as a JSON
    seriazable dict. """

    last_modified = election.last_result_change
    if last_modified:
        last_modified = last_modified.isoformat()

    return {
        'date': election.date.isoformat(),
        'domain': election.domain,
        'elected': election.elected_candidates,
        'last_modified': last_modified,
        'progress': {
            'counted': election.counted_entities or 0,
            'total': election.total_entities or 0
        },
        'title': election.title_translations,
        'type': 'election',
        'url': url or request.link(election),
    }


def get_vote_summary(vote, request, url=None):
    """ Returns some basic informations about the given vote as a JSON
    seriazable dict. """

    try:
        divider = vote.ballots.count() or 1
    except AttributeError:
        divider = 1

    last_modified = vote.last_result_change
    if last_modified:
        last_modified = last_modified.isoformat()

    summary = {
        'answer': vote.answer or "",
        'date': vote.date.isoformat(),
        'domain': vote.domain,
        'last_modified': last_modified,
        'nays_percentage': vote.nays_percentage,
        'progress': {
            'counted': (vote.progress[0] or 0) / divider,
            'total': (vote.progress[1] or 0) / divider
        },
        'title': vote.title_translations,
        'type': 'vote',
        'url': url or request.link(vote),
        'yeas_percentage': vote.yeas_percentage,
    }
    if 'local' in (vote.meta or {}):
        summary['local'] = {
            'answer': vote.local_answer or "",
            'nays_percentage': vote.local_nays_percentage,
            'yeas_percentage': vote.local_yeas_percentage,
        }
    return summary


def get_summary(item, request):
    """ Returns some basic informations about the given election/vote as a JSON
    seriazable dict. """
    if isinstance(item, Election):
        return get_election_summary(item, request)

    if isinstance(item, Vote):
        return get_vote_summary(item, request)

    if isinstance(item, ArchivedResult):
        if item.type == 'election':
            return get_election_summary(item, None, item.url)
        if item.type == 'vote':
            return get_vote_summary(item, None, item.url)

    raise NotImplementedError(
        "get_summary can't handle type {}".format(type(item))
    )


def get_summaries(items, request):
    """ Converts the given list of election/votes to a JSON seriazable
    list of summaries.

    """

    return [get_summary(item, request) for item in items]


def get_archive_links(archive, request):
    """ Returns a JSON seriazable dict of available archive links. """

    return {
        str(year): request.link(archive.for_date(year))
        for year in archive.get_years()
    }


def add_local_results(source, target, principal, session):
    """ Adds the result of the principal.

    Municipalities are interested in their own result rather than the
    cantonal end result of votes. We query the result of the municipality
    within the given vote (source) and add it to the target.

    """

    def accepted(ballot):
        return ballot.yeas > ballot.nays

    adjust = (
        principal.domain == 'municipality' and
        principal.municipality and
        source.type == 'vote' and
        'id' in (source.meta or {})
    )
    if adjust:
        entity_id = principal.municipality
        vote = session.query(Vote).filter(Vote.id == source.meta['id']).first()
        if vote and vote.proposal:
            yeas = None
            nays = None
            answer = None

            proposal = vote.proposal.results
            proposal = proposal.filter_by(entity_id=entity_id)
            proposal = proposal.first()

            if proposal and proposal.counted:
                if vote.counter_proposal and vote.tie_breaker:
                    counter = vote.counter_proposal.results
                    counter = counter.filter_by(entity_id=entity_id)
                    counter = counter.first()

                    tie = vote.tie_breaker.results
                    tie = tie.filter_by(entity_id=entity_id)
                    tie = tie.first()

                    if counter and counter.counted and tie and tie.counted:
                        if accepted(proposal) and accepted(counter):
                            if accepted(tie):
                                answer = 'proposal'
                            else:
                                answer = 'counter-proposal'
                        elif accepted(proposal):
                            answer = 'proposal'
                        elif accepted(counter):
                            answer = 'counter-proposal'
                        else:
                            answer = 'rejected'

                        if answer == 'counter-proposal':
                            yeas = counter.yeas
                            nays = counter.nays
                        else:
                            yeas = proposal.yeas
                            nays = proposal.nays
                else:
                    yeas = proposal.yeas
                    nays = proposal.nays
                    answer = 'accepted' if accepted(proposal) else 'rejected'

            if yeas and nays and answer:
                yeas = yeas / ((yeas + nays) or 1) * 100
                target.local_answer = answer
                target.local_yeas_percentage = yeas
                target.local_nays_percentage = 100 - yeas


def pdf_filename(item, locale):
    """ Generates a filename from an election or vote:

        ['election' or 'vote']-[hash of id].[timestamp].[locale].pdf

    """
    return '{}-{}.{}.{}.pdf'.format(
        'election' if isinstance(item, Election) else 'vote',
        sha256(item.id.encode('utf-8')).hexdigest(),
        int(item.last_result_change.timestamp()),
        locale
    )


def svg_filename(item, type_, locale=None):
    """ Generates a filename from an election, ballot or vote:

        ['election' or 'vote']-[hash of id].[type_].[timestamp].[locale].svg

    """

    if isinstance(item, Ballot):
        name = 'ballot'
        hash = str(item.id)
        ts = int(item.vote.last_result_change.timestamp())
    else:
        name = 'election' if isinstance(item, Election) else 'vote'
        hash = sha256(item.id.encode('utf-8')).hexdigest()
        ts = int(item.last_result_change.timestamp())

    return '{}-{}.{}.{}.{}.svg'.format(name, hash, ts, type_, locale or 'any')
