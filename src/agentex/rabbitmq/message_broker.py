import aio_pika
from aio_pika import ExchangeType

class MessageBroker:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect(self.rabbitmq_url)
        self.channel = await self.connection.channel()

    async def setup_exchange(self, exchange_name: str):
        return await self.channel.declare_exchange(exchange_name, ExchangeType.TOPIC)

    async def publish(self, exchange_name: str, routing_key: str, message: str):
        exchange = await self.setup_exchange(exchange_name)
        await exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=routing_key,
        )

    async def consume(self, queue_name: str, callback):
        queue = await self.channel.declare_queue(queue_name, durable=True)
        await queue.consume(callback)

    async def close(self):
        await self.channel.close()
        await self.connection.close()
