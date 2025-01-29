import asyncio

class LocalMessageBackend:
    def __init__(self):
        self.queues = {}

    async def connect(self):
        pass  # No setup required for local backend

    async def publish(self, routing_key: str, message: str):
        if routing_key not in self.queues:
            self.queues[routing_key] = asyncio.Queue()
        await self.queues[routing_key].put(message)

    async def consume(self, queue_name: str, callback):
        if queue_name not in self.queues:
            self.queues[queue_name] = asyncio.Queue()
        while True:
            message = await self.queues[queue_name].get()
            await callback(message)