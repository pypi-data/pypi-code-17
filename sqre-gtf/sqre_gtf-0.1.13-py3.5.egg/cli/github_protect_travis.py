#!/usr/bin/env python
"""
Command Line Interface to add TravisCI, branch protection and flake8
support for GitHub repository(ies).
"""
from gtf.base import get_parser, get_repos
from gtf.travis import travis
from gtf.protect import protect
from gtf.update import update


def main():
    parser = get_parser('Add TravisCI, protection and flake8 support.')
    parser.add_argument('-b', '--branch_name',
                        help='The branch name to use for clone and'
                        ' pull requests.')
    parser.add_argument('-c', '--clone', action='store_true',
                        help='Add default setup.cfg and/or .travis.yml')
    parser.add_argument('--commit_message', required=True, type=str,
                        help='Commit message to use when committing changes.')
    parser.add_argument('-k', '--task', type=str, default='stack',
                        help='The task to use when updating.')
    parser.add_argument('-u', '--pull', action='store_true',
                        help='Create a GitHub pull request if there are'
                        ' clone changes.')
    parser.add_argument('--pull_message', type=str,
                        help='Pull request message to use when creating'
                        ' a pull request.')
    parser.add_argument('-p', '--protect', action='store_true',
                        help='Add default branch protection')
    parser.add_argument('-t', '--travis', action='store_true',
                        help='Enable Travis CI webhook for repository(ies).')
    args = parser.parse_args()
    repos = get_repos(args)
    for r in repos:
        if args.travis:
            travis(r, verbose=args.verbose)
        if args.clone:
            if not args.branch_name:
                raise Exception('A branch_name argument is required when'
                                ' using clone.')
            update(r, task_name=args.task, branch_name=args.branch_name,
                   commit_message=args.commit_message,
                   pull=args.pull, pull_message=args.pull_message,
                   verbose=args.verbose)
        if args.protect:
            protect(r, verbose=args.verbose)


if __name__ == "__main__":
    main()
