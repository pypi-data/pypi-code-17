"""Test the task implementation by doing a dry run with the files and
printing the results.
"""
import os.path


def task(github_repo, git_repo, branch_name, clone_dir, verbose=True):
    """Verbose test task."""
    changed = False
    source_setup_cfg = os.path.join('..', 'files', 'stack-setup.cfg')
    source_travis_yml = os.path.join('..', 'files', 'default-.travis.yml')
    dest_setup_cfg = os.path.join(clone_dir, 'setup.cfg')
    dest_travis_yml = os.path.join(clone_dir, '.travis.yml')
    ticket_branch = git_repo.create_head(branch_name)
    ticket_branch.checkout()
    if verbose:
        print(github_repo)
        print(git_repo)
        print(branch_name)
        print(clone_dir)
        print('source_setup_cfg  = {0}'.format(source_setup_cfg))
        print('source_travis_yml = {0}'.format(source_travis_yml))
        print('dest_setup_cfg    = {0}'.format(dest_setup_cfg))
        print('dest_travis_yml   = {0}'.format(dest_travis_yml))
    return changed
