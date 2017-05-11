import os

from .constants import COMMIT_MESSAGE_START


class ImageLayer(object):
    """
    Represent one layer in final image.

    Contains commands and configuration for this layer.
    """

    def __init__(self, number, commands=None):
        self._commands = commands or []
        self.number = number
        self.is_last = False
        self.commit_message = COMMIT_MESSAGE_START
        self.conf = LayerConfig()

    def __str__(self):
        commands = "["
        for cmd in self.commands:
            commands += "<{}>".format(str(cmd))
        commands += "]"
        return "layer {}: {}".format(str(self.number), commands)

    def add_command(self, command, content):
        self._commands.append(command)

        formated_content = " {}".format(content.rstrip())
        self.commit_message += formated_content
        label_name = "layer_{}_commands".format(str(self.number))
        self.conf.labels.setdefault(label_name, "")
        self.conf.labels[label_name] += formated_content

    @property
    def commands(self):
        return self._commands


class LayerConfig(object):
    """
    Represent configuration of one layer.

    Contains metadata and commit config for new layer.
    """
    def __init__(self, envs=None, labels=None):
        self.container = None
        self.author = None
        self.labels = labels or {}

        self._logs = []
        self._workdir = os.curdir
        self._envs = envs or {}

        self._commit_config_properties = {}

    def add_property(self, key, value):
        self._commit_config_properties[key] = value

    def add_labels(self, labels):
        self.labels.update(labels)

    def add_envs(self, envs):
        self._envs.update(envs)

    def add_log(self, log):
        self._logs.append(log)

    @property
    def workdir(self):
        return self._workdir

    @workdir.setter
    def workdir(self, workdir):
        new_workdir = os.path.normpath(os.path.join(self._workdir, workdir))
        self.add_property("WorkingDir", new_workdir)
        self._workdir = new_workdir

    @property
    def commit_config(self):
        """
        Read-only property which can be used as a commit-config dictionary
        on container commit.

        :return: dict as a commit-config for this layer
        """
        config = dict(self._commit_config_properties)

        config.setdefault("Env", [])
        for k, v in self._envs.items():
            config["Env"].append('{}:{}'.format(str(k), str(v)))

        config.setdefault("Labels", {})
        config["Labels"].update(self.labels)

        return config

    @property
    def logs(self):
        return self._logs

    @property
    def envs(self):
        return self._envs
