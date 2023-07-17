import asyncio


def sync_to_async(func):
    async def _inner(*args, **kwargs):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, func, *args)
    return _inner
