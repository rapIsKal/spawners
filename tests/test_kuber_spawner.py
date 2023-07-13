import pytest

from spawners.kuber import KubernetesSpawner


@pytest.mark.asyncio
async def test_spawn():
    spawner = KubernetesSpawner()
    await spawner.spawn()