from agentex.rabbitmq.message_broker import MessageBroker

class RabbitMQBackend:
    def __init__(self, rabbitmq_url: str):
        self.broker = MessageBroker(rabbitmq_url)

    async def connect(self):
        await self.broker.connect()

    async def publish(self, routing_key: str, message: str):
        await self.broker.publish("swarm", routing_key, message)

    async def consume(self, queue_name: str, callback):
        """Consume messages from RabbitMQ."""
        async def message_handler(message):
            async with message.process():
                await callback(message.body.decode())

        await self.broker.consume(queue_name, message_handler)

