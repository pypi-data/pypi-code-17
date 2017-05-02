#!/usr/bin/env python
import importlib
import os.path
import shutil

import git
from github3.exceptions import UnprocessableEntity

from gtf.base import get_parser, get_repos, REPOS_DIR
#from gtf import  tasks  # flake8: noqa: F401
from gtf.update import update


def main():
    parser = get_parser('Create a branch and update GitHub repository(ies).')
    parser.add_argument('-b', '--branch_name', required=True,
                        help='The branch name to use for clone and'
                        ' pull requests.')
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
    args = parser.parse_args()
    repos = get_repos(args)
    for r in repos:
        update(r, task_name=args.task, branch_name=args.branch_name,
               commit_message=args.commit_message,
               pull=args.pull, pull_message=args.pull_message,
               verbose=args.verbose)


if __name__ == '__main__':
    main()
