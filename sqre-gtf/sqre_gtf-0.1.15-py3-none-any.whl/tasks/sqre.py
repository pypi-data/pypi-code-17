"""Configure .travis.yml using a default version that only runs flake8.
"""
import os.path
import shutil

from gtf.base import FILES_DIR


def add_file(git_repo, source, dest, file_name):
    if not os.path.exists(dest):
        shutil.copy(source, dest)
        git_repo.index.add([file_name])
        return True


def task(github_repo, git_repo, branch_name, clone_dir, verbose=False):
    """Add a default .travis.yml if it doesn't exist."""
    source_travis_yml = os.path.join(FILES_DIR, 'default-.travis.yml')
    dest_travis_yml = os.path.join(clone_dir, '.travis.yml')
    git_repo.git.reset('--hard', 'origin/master')
    ticket_branch = git_repo.create_head(branch_name)
    ticket_branch.checkout()
    return add_file(git_repo, source_travis_yml, dest_travis_yml,
                    '.travis.yml')
