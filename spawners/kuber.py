import asyncio

from kubernetes import config, client

from spawners.base import register_spawner, BaseSpawner
from utils.decorators import sync_to_async


@register_spawner('kubernetes')
class KubernetesSpawner(BaseSpawner):
    def __init__(self):
        config.load_kube_config()
        self.api = client.AppsV1Api()

    def build_aws_secret(self):
        raise NotImplementedError('waiting for access to create secrets')
        #api_instance = client.CoreV1Api()
        #sec = client.V1Secret()



    @sync_to_async
    def spawn(self, image: str = None, server=None, proxy_path: str = None,
                    memory_limit: int = 512 * 1e6, cpus: int = 1, mount: bool = True, mount_session_files=False,
                    extra_env: dict = None):
        name = "my-busybox"
        spec = client.V1DeploymentSpec(
            selector=client.V1LabelSelector(match_labels={"app": "busybox"}),
            template=client.V1PodTemplateSpec(),
        )
        container = client.V1Container(
            image="busybox:1.26.1",
            args=["sleep", "900"],
            name=name,
        )
        spec.template.metadata = client.V1ObjectMeta(
            name="busybox",
            labels={"app": "busybox"},
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
        return self.api.delete_namespaced_deployment(name="my-busybox", namespace="infinity-stand",
                                                     body=client.V1DeleteOptions(propagation_policy="Foreground", grace_period_seconds=5))

