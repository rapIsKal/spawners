import base64
import json
import os

import boto3 as boto3
from kubernetes import config, client

from spawners.base import register_spawner, BaseSpawner
from utils.decorators import sync_to_async


@register_spawner('kubernetes')
class KubernetesSpawner(BaseSpawner):
    def __init__(self):
        config.load_kube_config()
        self.api = client.AppsV1Api()

    def _aws_login(self):
        ecr_client = boto3.client(
            "ecr",
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
        )
        token = ecr_client.get_authorization_token()
        username, password = (
            base64.b64decode(token["authorizationData"][0]["authorizationToken"])
                .decode()
                .split(":")
        )
        return {"username": username, "password": password}

    @staticmethod
    def _prepare_auth_data(data):
        return {".dockerconfigjson": base64.b64encode(
            json.dumps(data).encode()).decode()}

    def build_aws_secret(self):
        auth_data = self._aws_login()
        api_instance = client.CoreV1Api()
        data = {"auths": {f"{os.getenv('AWS_ACCOUNT_ID')}.dkr.ecr.{os.getenv('AWS_REGION')}.amazonaws.com": auth_data}}
        metadata = client.V1ObjectMeta(name="mysecret", labels={"app": "myapp"})
        sec = client.V1Secret(type='kubernetes.io/dockerconfigjson', data=self._prepare_auth_data(data),
                              metadata=metadata)
        api_instance.create_namespaced_secret(namespace="infinity-stand", body=sec)




    @sync_to_async
    def spawn(self, image: str = "busybox:1.26.1", server=None, proxy_path: str = None,
                    memory_limit: int = 512 * 1e6, cpus: int = 1, mount: bool = True, mount_session_files=False,
                    extra_env: dict = None):
        name = "my-app"
        spec = client.V1DeploymentSpec(
            selector=client.V1LabelSelector(match_labels={"app": "myapp"}),
            template=client.V1PodTemplateSpec(),
        )
        container = client.V1Container(
            image=image,
            name=name,
        )
        spec.template.metadata = client.V1ObjectMeta(
            name="busybox",
            labels={"app": "myapp"},
        )
        spec.template.spec = client.V1PodSpec(containers=[container])
        dep = client.V1Deployment(
            metadata=client.V1ObjectMeta(name=name),
            spec=spec,
        )
        self.api.create_namespaced_deployment(namespace="infinity-stand", body=dep)

    # here decorator should be changed to built-in sync_to_async, for example in django-asgiref
    @sync_to_async
    def delete(self, server):
        return self.api.delete_namespaced_deployment(name="my-app", namespace="infinity-stand",
                                                     body=client.V1DeleteOptions(propagation_policy="Foreground", grace_period_seconds=5))

