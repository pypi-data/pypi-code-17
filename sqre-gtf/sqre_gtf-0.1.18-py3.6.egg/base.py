"""Base utility methods to automate Github, TravisCI and Flake8 changes.
"""
import argparse
import os

from codekit import codetools


GTF_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
HOME_DIR = os.path.expanduser('~')
REPOS_DIR = os.path.realpath(os.path.join(HOME_DIR, 'sqre-repos'))
FILES_DIR = os.path.realpath(os.path.join(GTF_DIR_PATH, 'files'))
gh = None


def _get_gh():
    global gh
    if not gh:
        gh = codetools.login_github()
    return gh


def token():
    gh = _get_gh()
    return gh.session.headers['Authorization'].split('token ')[1]


def get_repos(args):
    gh = _get_gh()
    repos = []
    if args.repos_dir:
        global REPOS_DIR
        REPOS_DIR = os.path.realpath(os.path.expanduser(args.repos_dir))
        os.makedirs(REPOS_DIR, exist_ok=True)
    if args.repo:
        repos.append(gh.repository(args.owner, args.repo))
    if args.repos:
        for repo_name in repos:
            repos.append(gh.repository(args.owner, repo_name))
    if args.file:
        for repo_name in open(args.file).read().split('\n'):
            if repo_name:
                repos.append(gh.repository(args.owner, repo_name))
    if not repos:
        Exception('A repository argument is required.')
    return repos


def get_parser(description):
    parser = argparse.ArgumentParser(
        description=description)
    parser.add_argument('-f', '--file',
                        help='The file with a line delimited list of'
                        ' repository names.')
    parser.add_argument('-o', '--owner',
                        help='The GitHub owner or organization of the'
                        ' repository(ies).')
    parser.add_argument('-d', '--repos_dir',
                        help='The directory used to clone repositories into.')
    parser.add_argument('-r', '--repo',
                        help='The GitHub repository to apply to apply'
                        ' changes to.')
    parser.add_argument('-s', '--repos', nargs='+',
                        help='GitHub repositories to apply changes to.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Display additional information.')
    return parser
