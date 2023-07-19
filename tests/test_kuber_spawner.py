import pytest

from spawners.kuber import KubernetesSpawner


@pytest.mark.order1
@pytest.mark.asyncio
async def test_spawn():
    spawner = KubernetesSpawner()
    await spawner.spawn(image="serverhub-servers:serverhub-homework-master")


@pytest.mark.order2
@pytest.mark.asyncio
async def test_delete():
    spawner = KubernetesSpawner()
    await spawner.delete('server')

@pytest.mark.order3
@pytest.mark.asyncio
async def test_kuber_spawn_with_limits():
    spawner = KubernetesSpawner()
    spawner.spawn(image="serverhub-servers:serverhub-homework-master", memory_limit=1024 * 1e6, cpus=2)

