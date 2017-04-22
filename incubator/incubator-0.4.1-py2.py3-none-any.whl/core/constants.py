"""
Constants used by builder.
"""
import os

CONFIG_BUILDARGS = 'buildargs'
CONFIG_CONTAINER_LIMITS = 'container_limits'
CONFIG_CONTEXT_FILE_LIMIT = "context_file_limit"
CONFIG_FORCE_RM = "forcerm"
CONFIG_INFINITE_COMMAND = "infinite_command"
CONFIG_LABELS = "labels"
CONFIG_LAYERS = "layers"
CONFIG_MKDIR_COMMAND = 'mkdir_command'
CONFIG_NAME = "config_name"
CONFIG_PULL = "pull"
CONFIG_RM = "rm"
CONFIG_TAGS = "tags"
CONFIG_VERSION = "version"
CONFIG_VOLUMES = "volumes"

DEFAULT_CONTEXT_FILE_LIMIT = 0
DEFAULT_REPOSITORY = "incubator-image"
DEFAULT_FORCE_RM = False
DEFAULT_INFINITE_COMMAND = "cat -"
DEFAULT_MKDIR_COMMAND = 'mkdir --parent'
DEFAULT_PULL = False
DEFAULT_RM = False
DEFAULT_TAG = "latest"
DEFAULT_VERSION = 1

COMMIT_MESSAGE_START = "This layer is composed of these commands:"

FILE_MODE_FROM_URL = 0o600

APP_NAME = 'incubator'

CONTEXT_FILE_IN_MEMORY = "in memory"
CONTEXT_FILE_ON_DISK = "on disk"

MAX_API_ATTEMPTS = 10

DEFAULT_CONFIG_FILES = ["{}/.incubator.rc".format(os.path.expanduser("~")),
                        "./.incubator.rc"]
