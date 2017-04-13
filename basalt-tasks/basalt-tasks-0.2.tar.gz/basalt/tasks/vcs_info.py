from sh import git 

"""\
The aim of vcs_info is to give some information about the exact version
the package was generated from. Those information can then be stored
somewhere in the package.
"""


def git_get_branch():
    """\
    Git implementation of `get_branch`.
    """
    return git("rev-parse", "--abbrev-ref", "HEAD")


def git_get_commit_rev():
    """\
    Git implementation of `get_commit`.
    """ 
    return git("rev-parse", "HEAD")


def get_branch(vcs='git'):
    """\
    Returns the branch name of the repository.
    """ 
    return globals()[vcs + "_get_branch"]()
    

def get_commit_rev(vcs='git'):
    """\
    Returns the sha1 commit revision of the repository.
    """ 
    return globals()[vcs + "_get_commit_rev"]()

