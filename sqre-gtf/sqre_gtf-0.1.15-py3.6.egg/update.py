import importlib
import os.path
import shutil

import git
from github3.exceptions import UnprocessableEntity

from .base import get_parser, get_repos, REPOS_DIR
from . import tasks  # flake8: noqa: F401


def _pull_request(github_repo, branch_name, pull_message, verbose):
    """Create a pull request."""
    title, body = pull_message.split('\n', 1)
    try:
        pr = github_repo.create_pull(
            title=title,
            base='master',
            head=branch_name,
            body=body)
        if verbose:
            print('Create pull request {0}'.format(pr))
    except UnprocessableEntity:
        if verbose:
            print('Unable to create pull request for [{0}/{1}]'.format(
                github_repo.owner.login, github_repo.name))


def _commit_and_push(git_repo, branch_name, commit_message, verbose):
    """Commit and push to the remote branch."""
    git_repo.index.commit(commit_message)
    if verbose:
        print('Add commit: {0}'.format(commit_message))
    remote = git_repo.remote(name='origin')
    refspec = 'refs/heads/{br}:refs/heads/{br}'.format(br=branch_name)
    remote.push(refspec=refspec, force=True)


def _clone(github_repo, branch_name, verbose):
    """Clone the GitHub repository and return the Git.repo object."""
    clone_dir = os.path.join(REPOS_DIR, github_repo.name)
    if not os.path.exists(clone_dir):
        git_repo = git.Repo.clone_from(github_repo.clone_url,
                                       clone_dir)
    else:
        git_repo = git.Repo(clone_dir)
    if verbose:
        print('Cloned [{0}/{1}] to {2}'.format(github_repo.owner.login,
                                               github_repo.name,
                                               os.path.abspath(clone_dir)))
    return git_repo, clone_dir


def _get_task(task_name):
    if not 'tasks' in task_name:
        task_name = 'gtf.tasks.' + task_name
    return importlib.import_module(task_name)


def update(github_repo, task_name, branch_name='master',
           commit_message='[gtf] update.',
           pull=False, pull_message='[gtf] update.', verbose=False):
    """Update the GitHub repository using the task.
    """
    git_repo, clone_dir = _clone(github_repo, branch_name, verbose)
    task = _get_task(task_name).task
    changed = task(github_repo, git_repo, branch_name, clone_dir, verbose)
    if changed:
        _commit_and_push(git_repo, branch_name, commit_message, verbose)
        if pull:
            _pull_request(github_repo, branch_name, pull_message, verbose)
