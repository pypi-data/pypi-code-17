import json
import time

from subprocess import Popen, PIPE, STDOUT 

class Check(object):

    def __init__(self, deployment, cluster):

        # Assume valid unless we say so later.
        self.valid = True

        env = deployment['Env']
        sourceID = deployment.get("SourceID")
        self.manifestID = sourceID.get("Location")
        if self.manifestID == "":
            self.setInvalid()
        flavor = deployment.get("Flavor") or ""
        if flavor != "":
            self.manifestID += ":" + flavor

        # The cluster could be read from the deployments OT_ENV var, but taking it from
        # args (see Main.run) as that's more explicit, and means we depend only on explicit
        # config in mnanifests, rather than inherited config from the env defs in Sous.
        self.Cluster = cluster

        # Disco init URL is read from deployments but is typically inherited, and thus
        # absent from manifests. We should keep an eye on this and ensure we continue to
        # depend on full Sous deployments rather than manifests.
        self.DiscoInitURL = env.get('OT_DISCO_INIT_URL') or self.setInvalid("Missing OT_DISCO_INIT_URL")

        # Read from general deployment fields.
        #
        self.NumInstances = deployment['NumInstances'] or self.setInvalid("Missing NumInstances")
    
        # Read from env vars expected to be explicitly set in the manifest.
        #
        # Right now SERVICE_TYPE this is the only required env var.
        self.AnnounceName = env.get('SERVICE_TYPE') or self.setInvalid("Missing SERVICE_TYPE") 
        # Default sensu team to be revisited.
        self.SensuTeam = env.get('OT_AUTOCHECK_SENSU_TEAM') or "alert_testing"
        # Default runbook should be enforced.
        self.AutocheckRunbookURL = env.get("OT_AUTOCHECK_RUNBOOK") or "https://wiki.otcorp.opentable.com/display/DCNetOps/Runbooks"
        # Paging enabled by default.
        self.DisablePaging = env.get("OT_AUTOCHECK_DISABLE_PAGING") or "YES"
        self.AutoCheckTimeout = env.get("OT_AUTOCHECK_TIMEOUT_SECONDS") or 30

    def command_args(self):
        return [
            "-s", self.AnnounceName,
            "-d", self.DiscoInitURL,
            "-c", str(self.NumInstances),
            "-w", str(self.NumInstances),
        ]

    def command(self, binPath):
        return [binPath] + self.command_args()

    # __repr__ is a standard Python method to define the string representation of something,
    # in this case its JSON representation.
    def __repr__(self):
        return json.dumps(self.json(), indent=4, sort_keys=True)

    # setInvalid marks this check as invalid and returns a string meant to convey
    # that information is undefined.
    def setInvalid(self, reason):
        self.valid = False
        self.invalidReason = reason
        return "<undefined>"

    def checkName(self):
        return "sous-autocheck_{0.AnnounceName}_{0.Cluster}".format(self)

    # result returns a json serialisable map of the results of running
    # this check. (It runs the check command in a shell. TODO: Run the check
    # command more securely.)
    def result(self, binPath, interval):
        command = self.command(binPath)
        print "Running {0}".format(" ".join(command))
        cmd = Popen(command, stderr=STDOUT, stdout=PIPE)
        startTime = time.time()
        output = cmd.communicate()
        endTime = time.time()
        stdout = output[0]
        exitCode = cmd.returncode

        return {
            "client": "sous-sensu-checks",
            "check": {
                # Result-specific fields.
                "name": self.checkName(),
                "status": exitCode,
                "output": stdout,
                "issued": int(startTime),
                "executed": int(startTime),
                "duration": "{0:.3f}".format(endTime - startTime),

                # General check fields.
                "command": " ".join(command),
                "contact": self.SensuTeam,
                "runbook": self.AutocheckRunbookURL,
                "page": True,
                "timeout": self.AutoCheckTimeout,
                "interval": interval,
                "region": self.Cluster,
            },
        }

