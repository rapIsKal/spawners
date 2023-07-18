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