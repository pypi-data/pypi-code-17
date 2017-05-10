import configparser
from datetime import datetime
import os
from github import Github
from termcolor import colored, cprint


GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_PASSWORD = os.getenv("GITHUB_PASSWORD")


def main():
    github = Github(GITHUB_USERNAME, GITHUB_PASSWORD)

    repo_type = "owner"
    for repo in github.get_user().get_repos(repo_type):
        if repo.fork is False:
            if repo.name == "ghlint-foobar": # this is for debugging only
                lint(repo)

def lint(repo):
    cprint(repo.name + " (", "white", end="")
    if repo.private is True:
        cprint("Private", "red", end="")
    else:
        cprint("Public", "green", end="")
    cprint(")", "white")

    ghlintrc = read_ghlintrc()
    print "this config"
    print ghlintrc.sections()

    branches = repo.get_branches()
    for branch in branches:
        if branch.name == "master":
            file = repo.get_file_contents("/.ghlintrc")
            decoded_content = "# Test " + "\r\n" + file.decoded_content
            print decoded_content

            has_editorconfig = False
            has_gitignore = False

            for file_in_root in repo.get_dir_contents("/"):
                if file_in_root.path == ".editorconfig":
                    has_editorconfig = True
                if file_in_root.path == ".gitignore":
                    has_gitignore = True

            if has_editorconfig != True:
                print "No .editorconfig"
            if has_gitignore != True:
                print "No .gitignore"

    pulls = repo.get_pulls()
    for pull in pulls:
        print "* " + pull.head.label[11:]
        pr_age = datetime.now() - pull.created_at
        if pr_age.days >= 7: # old pull requests
            print repo.name + " " + pull.head.label[11:]

def find_ghlintrc():
    ghlintrc = None

    if os.path.exists(".ghlintrc"):
        ghlintrc = os.path.abspath(".ghlintrc")

    return ghlintrc

def read_ghlintrc():
    config = configparser.ConfigParser()
    config.read(find_ghlintrc())

    return config


if __name__ == "__main__":
    main()
