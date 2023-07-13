from spawners.base import register_spawner, BaseSpawner


@register_spawner('swarm')
class KubernetesSpawner(BaseSpawner):

    async def spawn(self, image: str = None, server=None, proxy_path: str = None,
                    memory_limit: int = 512 * 1e6, cpus: int = 1, mount: bool = True, mount_session_files=False,
                    extra_env: dict = None):
        raise NotImplementedError()

    async def delete(self, server):
        pass

    async def list_services(self):
        pass

    async def delete_service(self, service_id):
        pass