from kubernetes import client, config
from kubernetes.client.rest import ApiException
from base64 import b64encode

import yaml,time
import datetime
import json
import os.path


class KubernetesOperations:
    def __init__(self, config_file=None):
        config.load_kube_config(config_file=config_file)

    @staticmethod
    def get_cluster_name():
        """
        Attempts to read the cluster name of an existing Kubernetes cluster through the kube config file.
        :return: String containing the cluster name, or None if not found.
        """
        try:
            with open(os.path.join(os.path.expanduser('~'), '.kube', 'config')) as f:
                config = yaml.load(f)
            return config['contexts'][0]['name']
        except (OSError, KeyError):
            print("Unable to locate kube config file for existing Kubernetes Cluster.")
            return None

    @staticmethod
    def b64encoded_string(text):
        """
        Returns a string representation of a base64 encoded version of the input text.
        Required because the b64encode method only accept/return bytestrings, but json and yaml require strings
        :param text: Text to encode
        :return string: string representation of the encoded text.
        """
        return b64encode(text.encode()).decode()

    def is_deployment_completed(self, name, namespace, desired_replicas):
        """
        Polls Kubernetes to check if a given deployment has finished being deployed.
        :param name: Name of the deployment
        :param namespace: Namespace containing the deployment.
        :param desired_replicas: Number of replicas requested in the deployment.
        :return bool: Returns true if deployment has successfully deployed desired_replicas pods.
        """
        try:
            api_response = client.ExtensionsV1beta1Api().read_namespaced_deployment_status(name=name,
                                                                                           namespace=namespace)
            print("Currently have {0} available replicas".format(api_response.status.available_replicas))
            return api_response.status.available_replicas == desired_replicas
        except ApiException as e:
            print("Exception when calling ExtensionsV1beta1Api->replace_namespaced_deployment_status: %s\n" % e)
            raise e

    def create_deployment(self, deployment_yaml, namespace, deployment_name):
        """
        Starts the creation of a Kubernetes deployment.
        :param deployment_yaml: Path of the yaml file to deploy
        :param namespace: Namespace to create a deployment in.
        :param deployment_name: Name of the new deployment
        :return: None
        """
        k8s_beta = client.ExtensionsV1beta1Api()
        print("Creating deployment {} in namespace {}".format(deployment_name, namespace))
        try:
            resp = k8s_beta.create_namespaced_deployment(namespace=namespace, body=deployment_yaml)
            print("Deployment created. status= {} ".format(str(resp.status)))
        except ApiException as e:
            exc_json = json.loads(e.body)
            if "AlreadyExists" in exc_json['reason']:
                k8s_beta.replace_namespaced_deployment(name=deployment_name, body=deployment_yaml, namespace=namespace)
            else:
                print("An error occurred while creating the deployment. {}".format(exc_json['message']))
                raise

    def deploy_deployment(self, deployment_yaml, max_deployment_time_s, desired_replica_num, secret_name):
        """
        Deploys a Kubernetes Deployment and waits for the deployment to complete.
        :param deployment_yaml: Path of the yaml file to deploy
        :param max_deployment_time_s: Max time to wait for a deployment to succeed before cancelling.
        :param desired_replica_num: Number of replica pods to create in the deployment
        :param secret_name: Name of the Kubernetes secret that contains the ACR login information for the image
                            specified in the deployment_yaml.
        :return bool: True if the deployment succeeds.
        """
        with open(deployment_yaml) as f:
            dep = yaml.load(f)
        namespace = "default"
        deployment_name = dep["metadata"]["name"]
        dep["spec"]["replicas"] = desired_replica_num
        dep["spec"]["template"]["spec"]["imagePullSecrets"][0]["name"] = secret_name
        self.create_deployment(dep, namespace, deployment_name)
        start_time = time.time()
        while time.time() - start_time < max_deployment_time_s:
            print('Deployment Ongoing')
            if self.is_deployment_completed(dep["metadata"]["name"], namespace, desired_replica_num):
                print("Deployment Complete")
                return True
            time.sleep(15)
        print("Deployment failed, to get the desired number of pods")
        return False

    def expose_frontend(self, service_yaml):
        """
        Exposes the azureml-fe deployment as a service.
        :param service_yaml: Path to azureml-fe-service.yaml
        :return: None
        """
        try:
            k8s_core = client.CoreV1Api()
            namespace = 'default'
            with open(service_yaml) as f:
                dep = yaml.load(f)
                print("Exposing frontend on Kubernetes deployment.")
                k8s_core.create_namespaced_service(body=dep, namespace=namespace)

        except ApiException as e:
            exc_json = json.loads(e.body)
            if 'AlreadyExists' in exc_json['reason']:
                return
            print("Exception during service creation: %s" % e)

    def get_service(self, webservicename):
        """
        Retrieves a service with a given webservicename
        :param webservicename: Name of the webservice.
        :return kubernetes.client.V1Service: Returns the webservice specified or None if one was not found.
        """
        try:
            k8s_core = client.CoreV1Api()
            namespace = 'default'
            label_selector = 'webservicename=={}'.format(webservicename)
            api_response = k8s_core.list_namespaced_service(namespace, label_selector=label_selector)
            if len(api_response.items) is 0:
                return None

            return api_response.items[0]
        except ApiException as e:
            print("Exception occurred while getting a namespaced service. {}".format(e))

    def create_acr_secret_if_not_exist(self, namespace, body):
        """
        Attempts to create an ACR secret on Kubernetes.
        :param namespace: Namespace of the secret.
        :param body: Kubernetes.client.V1Secret containing the acr credentials
        :return bool: True if successful, false if secret already exists.
        """
        retries = 0
        max_retries = 3
        while(retries < max_retries):
            try:
                client.CoreV1Api().create_namespaced_secret(namespace, body)
                return True
            except ApiException as e:
                if e.status == 409:  # 409 indicates secret already exists
                    return False
                retries += 1
                if retries >= max_retries:
                    print("Exception occurred in create_acr_secret_if_not_exist: {}".format(e))
                    raise e

    def replace_secrets(self, name, namespace, body):
        """
        Replaces an existing secret. Cannot patch due to immutability.
        :param name: Name of the secret to replace
        :param namespace: Namespace containing the secret
        :param body: Kubernetes.client.V1Secret containing the secret payload
        :return bool: True if successful, false if secret already exists.
        """
        try:
            client.CoreV1Api().delete_namespaced_secret(name, namespace, client.V1DeleteOptions())
            return self.create_acr_secret_if_not_exist(namespace, body)
        except ApiException as e:
            print("Exception occurred in replace_secrets: {}".format(e))
            raise e

    def create_or_replace_docker_secret_if_exists(self, acr_credentials, secret_name):
        """
        Adds a docker registry secret to Kubernetes secret storage.
        :param acr_credentials: Encoded ACR credentials to store as a secret
        :param secret_name: Name of the secret
        :return bool: True if successful.
        """
        print("Creating Secret {}".format(secret_name))
        namespace = 'default'
        secret = dict()
        secret[".dockercfg"] = acr_credentials
        meta = client.V1ObjectMeta(name=secret_name, namespace="default")
        body = client.V1Secret(data=secret, metadata=meta, type="kubernetes.io/dockercfg")
        if self.create_acr_secret_if_not_exist(namespace, body):
            return True
        else:
            return self.replace_secrets(secret_name, namespace, body)

    def encode_acr_credentials(self, acr_host, acr_uname, acr_pwd, acr_email):
        """
        Encodes ACR credentials for correct storage as a .dockerconfigjson secret.
        :param acr_host: Base url of the acr storage
        :param acr_uname: Username of the ACR
        :param acr_pwd: Password of the ACR
        :param acr_email: Email connected to the ACR
        :return string: Base64 representation of ACR credentials
        """
        return self.b64encoded_string(json.dumps(
            {acr_host:
                 {"username": acr_uname,
                  "password": acr_pwd,
                  "email": acr_email,
                  "auth": self.b64encoded_string(acr_uname+":"+acr_pwd)
                  }
             }
        ))

    def add_acr_secret(self, key, server, username, password, email):
        """
        Adds an ACR secret to Kubernetes.
        :param key: Name of the secret being added
        :param server: Base url of the ACR storage
        :param username: Username of the ACR
        :param password: Password of the ACR
        :param email: Email connected to the ACR
        :return: None
        """
        return self.create_or_replace_docker_secret_if_exists(
            self.encode_acr_credentials(server, username, password, email), key)
