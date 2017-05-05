from __future__ import with_statement, print_function

import sys
from optparse import make_option
import traceback
from StringIO import StringIO

from six.moves.urllib.error import HTTPError

from django.core.management.base import BaseCommand

from feedz.models import Post

try:
    from chroniker.models import Job
except ImportError:
    Job = None

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
#        make_option('--feeds', dest="feeds", default='',
#                    help="Specific feeds to refresh."),
        make_option('--force', action='store_true', default=False,
                    help="Specific feeds to refresh."),
        make_option('--year',
                    help="A specific year to process."),
        make_option('--month',
                    help="A specific month to process."),
#        make_option(
#            '--without-error',
#            action='store_true',
#            default=False,
#            help="A specific month to process."),
        make_option(
            '--dryrun',
            action='store_true',
            default=False,
            help="Makes no changes."),
    )

    help = ("Attempts to extract the article text from the URL associated with each post.", )

    def handle(self, *args, **options):
        dryrun = options['dryrun']
        q = Post.objects.all_articleless()

        # Keep retrying until we get a legitimate error code
        # explaining the failure.
        q = q.filter(article_content_error_code__isnull=True)

        #q = q.filter(article_content_success__isnull=True)

        #TODO:retry article_content_success=False but with error_code__isnull=False?
        year = options['year']
        month = options['month']
        if year:
            q = q.filter(date_published__year=year)
        if month:
            q = q.filter(date_published__month=month)
        #q = q.only('id', )
        q = q.order_by('-date_published')
        total = q.count()
        i = 0
        success_count = 0 # successfully retrieved non-empty content
        error_count = 0 # any type of exception was thrown
        meh_count = 0 # no errors were thrown, even if we didn't get content
        print('%i posts without an article.' % (total,))
        if dryrun:
            return
        for post in q.iterator():
            i += 1
            sys.stdout.write('\rProcessing post %i (%i of %i, %i success, %i errors, %i mehs)...' \
                % (post.id, i, total, success_count, error_count, meh_count))
            sys.stdout.flush()
            if Job:
                Job.update_progress(total_parts=total, total_parts_complete=i)
            try:
                post.retrieve_article_content(force=options['force'])
                success_count += bool(len((post.article_content or '').strip()))
                meh_count += not bool(len((post.article_content or '').strip()))
            except HTTPError as e:
                error_count += 1
                print(file=sys.stderr)
                print('Error: Unable to retrieve %s: %s' % (post.link, e), file=sys.stderr)
                post.article_content_error_code = e.code
                post.article_content_error_reason = e.reason
                post.article_content_success = False
                post.save()
            except Exception as e:
                post.article_content_success = False
                ferr = StringIO()
                traceback.print_exc(file=ferr)
                post.article_content = None
                post.article_content_error = ferr.getvalue()
                post.save()
                error_count += 1
                print(sys.stderr)
                print('Error: Unable to retrieve %s: %s' % (post.link, e), file=sys.stderr)
        print
        print('-'*80)
        print('%i successes' % success_count)
        print('%i errors' % error_count)
