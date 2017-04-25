"""Configure .travis.yml and setup.cfg using the LSST DM pipeline defaults.
This configuration will only run flake8.
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
    """Add setup.cfg and .travis.yml if they don't exist."""
    changed = False
    source_setup_cfg = os.path.join(FILES_DIR,
                                    'stack-setup.cfg')
    source_travis_yml = os.path.join(FILES_DIR,
                                     'default-.travis.yml')
    dest_setup_cfg = os.path.join(clone_dir, 'setup.cfg')
    dest_travis_yml = os.path.join(clone_dir, '.travis.yml')
    git_repo.git.reset('--hard', 'origin/master')
    ticket_branch = git_repo.create_head(branch_name)
    ticket_branch.checkout()
    changed = add_file(git_repo, source_setup_cfg, dest_setup_cfg, 'setup.cfg')
    changed = add_file(git_repo, source_travis_yml, dest_travis_yml,
                       '.travis.yml') or changed
    return changed
