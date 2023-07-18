import asyncio
import functools


def sync_to_async(func):
    async def _inner(*args, **kwargs):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))
    return _inner
