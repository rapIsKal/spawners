from abc import ABC, abstractmethod
from typing import Any

AVAILABLE_SPAWNERS = {}


class BaseSpawner(ABC):

    @abstractmethod
    async def spawn(
        self,
        image: str = None,
        server: Any = None,
        proxy_path: str = None,
        memory_limit: int = 512 * 1e6,
        cpus: int = 1,
        mount: bool = True,
        mount_session_files: bool = False,
    ):
        pass

    @abstractmethod
    async def delete(
            self,
            server: Any,
    ):
        pass


def register_spawner(name):
    def decorator(cls):
        AVAILABLE_SPAWNERS[name] = cls
        return cls

    return decorator
