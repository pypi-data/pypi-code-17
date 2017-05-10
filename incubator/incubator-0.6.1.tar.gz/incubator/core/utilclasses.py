class ResultImage(object):
    """
    Represent final image built by incubator.
    """

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
    """
    Represent logs for one dockerfile command.
    """

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
