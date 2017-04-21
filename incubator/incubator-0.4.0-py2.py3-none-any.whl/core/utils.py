"""
Utility methods for builder.
"""
import io
import logging
import os
import tarfile
import tempfile

import six

from .constants import (APP_NAME, COMMIT_MESSAGE_START, CONTEXT_FILE_IN_MEMORY,
                        CONTEXT_FILE_ON_DISK, DEFAULT_CONTEXT_FILE_LIMIT)
from .output import CHAPTER

logger = logging.getLogger(APP_NAME)


def dockerfile_from_context(context, path):
    with tarfile.open(mode="r", fileobj=context) as t:
        df = t.extractfile(t.getmember(path))
    dockerfile = six.BytesIO()
    dockerfile.writelines(df.readlines())
    dockerfile.seek(0)
    context.seek(0)
    return dockerfile


def mkbuildcontext(path, fileobj, custom_context, dockerfile, client, limit=None):
    if path is None and fileobj is None:
        raise TypeError("Either path or fileobj needs to be provided.")

    dockerfile = dockerfile or "Dockerfile"

    if custom_context:
        if not fileobj:
            raise TypeError("You must specify fileobj with custom_context")
        return fileobj, dockerfile_from_context(fileobj, dockerfile)
    elif fileobj is not None:
        return make_build_context_from_dockerfile(fileobj), fileobj
    elif path.startswith(('http://', 'https://',
                          'git://', 'github.com/', 'git@')):
        # TODO
        return None, None
    elif not os.path.isdir(path):
        raise TypeError("You must specify a directory to build in path")
    else:
        dockerignore = os.path.join(path, '.dockerignore')
        exclude = None
        if os.path.exists(dockerignore):
            with open(dockerignore, 'r') as f:
                exclude = list(filter(bool, f.read().splitlines()))
        context = tar(
            path, client, exclude=exclude, dockerfile=dockerfile, limit=limit
        )
        dockerfile_obj = dockerfile_from_context(context=context, path=dockerfile)
        return context, dockerfile_obj


def exclude_paths(root, exclude, dockerfile, client):
    files = client.exclude_paths_from_context(root, exclude, dockerfile)
    return files


def tar(path, client, exclude=None, dockerfile=None, fileobj=None, limit=DEFAULT_CONTEXT_FILE_LIMIT):
    if not fileobj:
        fileobj = tempfile.SpooledTemporaryFile(max_size=limit)

    root = os.path.abspath(path)
    exclude = exclude or []

    logger.debug(CHAPTER.format("context:"))
    with tarfile.open(mode='w', fileobj=fileobj) as t:
        for p in sorted(exclude_paths(root, exclude,
                                      dockerfile=dockerfile,
                                      client=client)):
            logger.debug("- {}".format(p))
            t.add(name=os.path.join(path, p), arcname=p)
    logger.debug("")
    fileobj.seek(0)

    if isinstance(fileobj, tempfile.SpooledTemporaryFile):
        if fileobj.name:
            context_file_type = CONTEXT_FILE_ON_DISK
        else:
            context_file_type = CONTEXT_FILE_IN_MEMORY
        logger.debug(CHAPTER.format("context type: {}".format(context_file_type)))

    return fileobj


def make_build_context_from_dockerfile(dockerfile):
    f = six.BytesIO()
    with tarfile.open(mode='w', fileobj=f) as t:
        if isinstance(dockerfile, six.StringIO) or isinstance(dockerfile, io.StringIO):
            dfinfo = tarfile.TarInfo('Dockerfile')
            dfinfo.size = len(dockerfile.getvalue())
            dockerfile.seek(0)
        elif isinstance(dockerfile, six.BytesIO) or isinstance(dockerfile, io.BytesIO):
            dfinfo = tarfile.TarInfo('Dockerfile')
            dfinfo.size = len(dockerfile.getvalue())
            dockerfile.seek(0)
        else:
            dfinfo = t.gettarinfo(fileobj=dockerfile, arcname='Dockerfile')
        t.addfile(dfinfo, dockerfile)
    f.seek(0)
    return f


def get_name_and_tag(name):
    name_parts = name.split(':')
    if len(name_parts) == 2:
        repo = name_parts[0]
        tag = name_parts[1]
    else:
        repo = name
        tag = "latest"

    return repo, tag


class ImageLayer(object):
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
        self.conf.commit_config.setdefault('Labels', {})
        self.conf.commit_config['Labels'].setdefault(label_name, "")
        self.conf.commit_config['Labels'][label_name] += formated_content

    @property
    def commands(self):
        return self._commands


class ResultImage(object):
    def __init__(self, image_id, logs=None):
        self._id = image_id
        self._logs = logs or []

    @property
    def id(self):
        return self._id

    @property
    def logs(self):
        return self._logs

    def add_log(self, log):
        self._logs.append(log)

    def __str__(self):
        return "ResultImage<id: {}>".format(str(self._id))


class CommandLog(object):
    def __init__(self, command, logs=None):
        self._command = command
        self._logs = logs or []

    @property
    def command(self):
        return self._command

    @property
    def logs(self):
        return self._logs

    def add_log(self, log):
        self._logs.append(log)

    def add_logs(self, logs):
        self._logs += logs


class LayerConfig(object):
    def __init__(self):
        self.commit_config = {}
        self.container = None
        self.author = ""
        self._logs = []
        self._workdir = os.curdir

    @property
    def workdir(self):
        return self._workdir

    @workdir.setter
    def workdir(self, workdir):
        new_workdir = os.path.normpath(os.path.join(self._workdir, workdir))
        self.add_property("WorkingDir", new_workdir)
        self._workdir = new_workdir

    def add_property(self, key, value):
        self.commit_config[key] = value

    def add_labels(self, labels):
        self.commit_config.setdefault("Labels", {})
        self.commit_config["Labels"].update(labels)

    def add_envs(self, envs):
        self.commit_config.setdefault("Env", [])
        for k, v in envs.items():
            self.commit_config["Env"].append('{}:{}'.format(str(k), str(v)))
        unique_envs = list(set(self.commit_config["Env"]))
        self.commit_config["Env"] = unique_envs

    @property
    def logs(self):
        return self._logs

    def add_log(self, log):
        self._logs.append(log)


def volumes_to_list(dict, mode=""):
    if mode:
        mode = ":" + mode
    else:
        mode = ""

    volumes = []
    for key, value in six.iteritems(dict):
        volumes.append("{}:{}{}".format(key, value, mode))
    return volumes


def volumes_to_bind_dict(dict, mode=""):
    volumes = {}
    for key, value in six.iteritems(dict):
        volumes[key] = {"bind": value,
                        "mode": mode
                        }
    return volumes


def volumes_to_dict(volumes):
    volumes = get_list_from_tuple_or_string(volumes)
    result = {}

    for v in volumes:
        v_split = v.split(':')
        result[v_split[0]] = v_split[1]

    return result


def get_list_from_tuple_or_string(value):
    if not value:
        return []
    if isinstance(value, six.string_types):
        return [value]
    else:
        return list(value)
