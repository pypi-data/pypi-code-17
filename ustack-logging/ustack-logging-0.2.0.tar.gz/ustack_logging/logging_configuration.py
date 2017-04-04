import base64
import datadog
from datadog_logger import log_error_events
import kubernetes.client
import logging
import socket


def configure_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(module)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S%z", level=logging.INFO)

    try:
        kubernetes.config.load_incluster_config()

        core_api = kubernetes.client.CoreV1Api()
        environment_info = core_api.read_namespaced_secret("environment-info", "ustudio-system")

        datadog.initialize(
            api_key=base64.b64decode(environment_info.data["datadog-api-key"]).decode("utf8"),
            app_key=base64.b64decode(environment_info.data["datadog-app-key"]).decode("utf8"))

        with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
            namespace = f.read()

        pod_name = socket.gethostname().split(".")[0]

        pod_info = core_api.read_namespaced_pod(pod_name, namespace)

        log_error_events(tags=[
            "environment:{0}".format(
                base64.b64decode(environment_info.data["environment"]).decode("utf8")),
            "service:{0}".format(namespace),
            "role:{0}".format(pod_info.metadata.labels["role"])
        ])
    except:
        logging.warning("Could not initialize DataDog error logging, with error:", exc_info=True)
