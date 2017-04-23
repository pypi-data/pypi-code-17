import argparse
from argparse import RawTextHelpFormatter
from .run import run
from .ping import ping
from .list import list_jobs
from .info import info
from .cat import cat

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

parser.prog = 'jenkins'
parser.description = """Jenkins stupid simple CLI.
Commands were written with the same name as UNIX programs to be 
more intuitive for everyone."""

subparsers = parser.add_subparsers(help='command help')

ping_parser = subparsers.add_parser('ping', help='Tries to connect to given Jenkins server.')
ping_parser.set_defaults(func=ping)


run_parser = subparsers.add_parser('run', help='Trigger given job.')
run_parser.add_argument('job')
run_parser.add_argument('arguments', metavar='args',
                        help='Arguments to build parametrized job: arg1=value arg2=value',
                        default=None, nargs='*')
run_parser.set_defaults(func=run)


list_parser = subparsers.add_parser('ls', help='Retrieves all job names that matches with given pattern.')
list_parser.add_argument('pattern', metavar='pattern', help='Search for jobs that contains the given string'
                                                            ' will ignore case by default')
list_parser.add_argument('--view', metavar='view_name',
                         help='Search for jobs that belongs to the given view', default=None)
list_parser.set_defaults(func=list_jobs)


info_parser = subparsers.add_parser('info', help='Gather relevant information from given job.')
info_parser.add_argument('job', metavar='job_name', default=None,
                       help='Job name which you want to get information')
info_parser.set_defaults(func=info)


tail_parser = subparsers.add_parser('cat', help='Reads last build console logs')
tail_parser.add_argument('job', metavar='job_name', default=None,
                         help='Job name which you want collect the console logs')
tail_parser.set_defaults(func=cat)