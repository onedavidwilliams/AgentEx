import asyncio
from collections import defaultdict
from agentex.backends.local_backend import LocalMessageBackend
from agentex.backends.rabbitmq_backend import RabbitMQBackend
from agentex.tasks.task_manager import TaskManager
from agentex.tasks.task import Task

class Swarm:
    def __init__(self, name: str, backend="local", config=None):
        self.name = name
        self.backend = (
            LocalMessageBackend() if backend == "local" else RabbitMQBackend(config["rabbitmq_url"])
        )
        self.groups = defaultdict(set)  # Group-to-agents mapping
        self.capabilities = defaultdict(set)  # Capability-to-agents mapping
        self.task_manager = TaskManager()
    async def connect(self):
        """Connect to the selected backend."""
        await self.backend.connect()

    async def send_to_agent(self, agent: str, message: str):
        """Send a message to a specific agent."""
        routing_key = f"agent.{agent}"
        await self.backend.publish(routing_key, message)

    async def broadcast(self, message: str):
        """Broadcast a message to all agents."""
        await self.backend.publish("broadcast", message)

    async def send_to_group(self, group_name: str, message: str):
        """Send a message to all agents in a group."""
        if group_name not in self.groups or not self.groups[group_name]:
            print(f"Warning: Group '{group_name}' has no agents.")
            return

        for agent in self.groups[group_name]:
            await self.send_to_agent(agent.name, message)

    async def send_to_capability(self, capability: str, message: str):
        """Send a message to all agents with a specific capability."""
        if capability not in self.capabilities or not self.capabilities[capability]:
            print(f"Warning: No agents found with capability '{capability}'.")
            return

        for agent in self.capabilities[capability]:
            await self.send_to_agent(agent.name, message)

    def add_agent_to_group(self, agent, group_name: str):
        """Add an agent to a group."""
        self.groups[group_name].add(agent)

    def remove_agent_from_group(self, agent, group_name: str):
        """Remove an agent from a group."""
        if group_name in self.groups:
            self.groups[group_name].discard(agent)
            if not self.groups[group_name]:  # Clean up empty groups
                del self.groups[group_name]

    def register_agent_capability(self, agent, capability: str):
        """Register an agent's capability."""
        self.capabilities[capability].add(agent)

    def unregister_agent_capability(self, agent, capability: str):
        """Unregister an agent's capability."""
        if capability in self.capabilities:
            self.capabilities[capability].discard(agent)
            if not self.capabilities[capability]:  # Clean up empty capabilities
                del self.capabilities[capability]

    async def consume_messages(self, queue_name: str, callback):
        """Consume messages from a specific queue."""
        await self.backend.consume(queue_name, callback)


    async def assign_task(self, task_type: str, payload: dict):
        """Create and assign a task to the task queue."""
        task = Task(task_type, payload)
        await self.task_manager.add_task(task)