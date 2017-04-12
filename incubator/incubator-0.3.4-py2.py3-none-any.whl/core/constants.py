"""
Constants used by builder.
"""

CONFIG_LAYERS = "layers"
CONFIG_VOLUMES = "volumes"
CONFIG_LABELS = "labels"
CONFIG_VERSION = "version"
CONFIG_INFINITE_COMMAND = "infinite_command"
CONFIG_REPOSITORY = "repository"
CONFIG_TAGS = "tags"
CONFIG_MKDIR_COMMAND = 'mkdir_command'
CONFIG_BUILDARGS = 'buildargs'
CONFIG_CONTAINER_LIMITS = 'container_limits'
CONFIG_PULL = "pull"

DEFAULT_REPOSITORY = "incubator-image"
DEFAULT_TAG = "latest"

INFINITE_COMMAND = "cat -"
MKDIR_COMMAND = 'mkdir --parent'

DEFAULT_VERSION = 1
COMMIT_MESSAGE_START = "This layer is composed of these commands:"

FILE_MODE_FROM_URL = 0o600

APP_NAME = 'incubator'

CONFIG_CONTEXT_FILE_LIMIT = "context_file_limit"
DEFAULT_CONTEXT_FILE_LIMIT = 0
CONTEXT_FILE_IN_MEMORY = "in memory"
CONTEXT_FILE_ON_DISK = "on disk"

MAX_API_ATTEMPTS = 10
