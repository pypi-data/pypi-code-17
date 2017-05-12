import os

import yaml
from typing import NamedTuple

GITLAB_PROPERTY = "gitlab"
GITLAB_URL_PROPERTY = "url"
GITLAB_TOKEN_PROPERTY = "token"
GITLAB_PROJECT_PROPERTY = "project"
GITLAB_NAMESPACE_PROPERTY = "namespace"


class GitLabConfiguration(NamedTuple):
    """
    GitLab configuration.
    """
    url: str
    token: str
    project: str = None
    namespace: str = None


class Configuration(NamedTuple):
    """
    Program configuraiton.
    """
    gitlab: GitLabConfiguration


def parse_configuration(configuration_file: str) -> Configuration:
    """
    Parses the program configuration in the given file.
    :return: the configuration
    """
    if not (os.path.isfile(configuration_file) and os.access(configuration_file, os.R_OK)):
        raise ValueError(f"Cannot read configuration file: {configuration_file}")

    with open(configuration_file, "r") as file:
        json_configuration = yaml.load(file)

    project = json_configuration[GITLAB_PROPERTY][GITLAB_PROJECT_PROPERTY] \
        if GITLAB_PROJECT_PROPERTY in json_configuration[GITLAB_PROPERTY] else None
    namespace = json_configuration[GITLAB_PROPERTY][GITLAB_NAMESPACE_PROPERTY] \
        if GITLAB_NAMESPACE_PROPERTY in json_configuration[GITLAB_PROPERTY] else None

    gitlab_configuration = GitLabConfiguration(
        url=json_configuration[GITLAB_PROPERTY][GITLAB_URL_PROPERTY],
        token=json_configuration[GITLAB_PROPERTY][GITLAB_TOKEN_PROPERTY],
        project=project,
        namespace=namespace
    )

    return Configuration(gitlab=gitlab_configuration)
