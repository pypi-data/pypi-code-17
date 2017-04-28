import json
import os
import threading
import requests

from subprocess import Popen, PIPE, STDOUT
from ws4py.messaging import TextMessage


class Job(object):

    RUNNING = "Running"
    WAITING = "Waiting"
    DONE = "Done"
    ERROR = "Error"

    def __init__(self, status=WAITING):
        self.lines = []
        self.handlers = []
        self.status = status
        self.metadata = {}

    def send_message(self, msg):
        if msg is None:
            return

        if msg.startswith("LOG:"):
            self.lines.append(msg[4:])

        if msg.startswith("STA:"):
            self.status = msg[4:]

        for handler in self.handlers:
            if not handler.terminated:
                handler.send(TextMessage(msg))

    def add_handler(self, handler):
        self.handlers.append(handler)


class LocalJob(threading.Thread, Job):

    def __init__(self, command, metadata, workspace=None, conda_env=None, environment=None, postcommand=None):
        threading.Thread.__init__(self)
        Job.__init__(self, status=Job.RUNNING)

        self.command = command
        self.metadata = metadata
        self.workspace = workspace
        self.conda_env = conda_env
        self.environment = {} if environment is None else environment
        self.postcommand = postcommand

    def run(self):

        # Save metadata
        metadata_path = os.path.join(self.workspace, "metadata.json")
        with open(metadata_path, 'wt') as fd:
            json.dump(self.metadata, fd)

        # Create script
        script_path = os.path.join(self.workspace, "run.sh")

        with open(script_path, "wt") as fd:
            fd.writelines([
                "#!/bin/bash\n",
                "source ~/.bashrc\n",
                "{}\n".format("\n".join(["export {}={}".format(k, v) for k, v in self.environment.items()])),
                "source activate {} 2>/dev/null\n".format(self.conda_env) if self.conda_env is not None else "\n",
                "{} 2>&1 | tee {}\n".format(self.command, os.path.join(self.workspace, "run.sh.stdout")),
                "err=${PIPESTATUS[0]}; if [ $err -ne 0 ]; then exit $err; fi\n",
                "{}\nerr=${{PIPESTATUS[0]}}; if [ $err -ne 0 ]; then exit $err; fi\n".format(self.postcommand) if self.postcommand is not None else "\n"
            ])

        os.chmod(script_path, 0o774)

        p = Popen("bash {}".format(script_path), shell=True, stdout=PIPE, stderr=STDOUT)
        self.send_message("STA:"+Job.RUNNING)

        for l in p.stdout:
            self.send_message("LOG:" + l.decode("utf-8"))

        # Send done status
        p.wait()
        if p.returncode == 0:
            self.send_message("STA:" + Job.DONE)
        else:
            self.send_message("STA:" + Job.ERROR)

        for handler in self.handlers:
            if not handler.terminated:
                handler.close(reason="Job finished")


class RemoteJob(Job):

    def __init__(self, command, metadata,
                 workspace=None,
                 scheduler_url="http://localhost:9090",
                 tee_url="http://localhost:8080/task",
                 port=None,
                 host=None,
                 job_id=None,
                 cores=None,
                 conda_env=None,
                 environment=None,
                 postcommand=None):

        Job.__init__(self)

        self.command = command
        self.postcommand = postcommand
        self.metadata = metadata
        self.job_id = job_id
        self.cores = cores
        self.ws_host_port = "" if host is None else "&host={}".format(host)
        self.ws_host_port += "" if port is None else "&port={}".format(port)
        self.tee_url = tee_url
        self.workspace = workspace
        self.scheduler_url = scheduler_url
        self.conda_env = conda_env
        self.environment = {} if environment is None else environment

    def start(self):

        # Save metadata
        metadata_path = os.path.join(self.workspace, "metadata.json")
        with open(metadata_path, 'wt') as fd:
            json.dump(self.metadata, fd)

        # Create script
        script_path = os.path.join(self.workspace, "run.sh")
        with open(script_path, "wt") as fd:
            fd.writelines([
                "#!/bin/bash\n",
                "source ~/.bashrc\n",
                "{}\n".format("\n".join(["export {}={}".format(k, v) for k, v in self.environment.items()])),
                "source activate {} 2>/dev/null\n".format(self.conda_env) if self.conda_env is not None else "\n",
                "bg-ping -u \"{}?id={}{}&line=STA:Running\"\n".format(self.tee_url, self.job_id, self.ws_host_port),
                "{} 2>&1 | bg-tee -p \"LOG:\" -u \"{}?id={}{}&line=\"\n".format(self.command, self.tee_url, self.job_id, self.ws_host_port),
                "err=${{PIPESTATUS[0]}}; if [ $err -ne 0 ]; then bg-ping -u \"{}?id={}{}&line=STA:Error\"; exit $err; fi\n".format(self.tee_url, self.job_id, self.ws_host_port),
                "{} 2>&1 | bg-tee -p \"LOG:\" -u \"{}?id={}{}&line=\"\n".format(self.postcommand, self.tee_url, self.job_id, self.ws_host_port) if self.postcommand is not None else "\n",
                "err=${{PIPESTATUS[0]}}; if [ $err -ne 0 ]; then bg-ping -u \"{}?id={}{}&line=STA:Error\"; exit $err; fi\n".format(self.tee_url, self.job_id, self.ws_host_port) if self.postcommand is not None else "\n",
                "bg-ping -u \"{}?id={}{}&line=STA:Done\"\n".format(self.tee_url, self.job_id, self.ws_host_port)
            ])

        os.chmod(script_path, 0o774)
        # Send to the server
        requests.post("{}/api/task".format(self.scheduler_url), data={'script': script_path, 'id': self.job_id, 'cores': self.cores})


class DetachedJob(Job):

    def __init__(self, workspace):
        Job.__init__(self, status=Job.DONE)

        log_file = os.path.join(workspace, "run.sh.stdout")
        metadata_file = os.path.join(workspace, "metadata.json")

        # Read metadata
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'rt') as fd:
                    self.metadata = json.load(fd)
            except ValueError as e:
                self.metadata = {'error': e}

        # Load logging
        if os.path.exists(log_file):
            with open(log_file, 'rt') as fd:
                last_line_return_carriage = None
                for line in fd:
                    if '\x1b[0m' in line or line.startswith('['):
                        if not line.startswith('['):
                            last_line_return_carriage = line
                    else:
                        if last_line_return_carriage is not None:
                            self.send_message("LOG:"+last_line_return_carriage.replace('\x1b[0m', ''))
                            last_line_return_carriage = None
                        self.send_message("LOG:"+line)

    def start(self):
        pass
