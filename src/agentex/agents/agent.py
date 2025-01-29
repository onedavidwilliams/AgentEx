import asyncio
class Agent:
    def __init__(self, name: str, swarm, on_message=None, groups=None, capabilities=None):
        """
        Initialize an agent.
        :param name: Name of the agent.
        :param swarm: The swarm this agent belongs to.
        :param on_message: Optional callback for incoming messages.
        :param groups: Optional list of groups to join at instantiation.
        :param capabilities: Optional list of capabilities (tags) for dynamic task assignment.
        """
        self.name = name
        self.swarm = swarm
        self.on_message = on_message
        self.groups = set(groups) if groups else set()
        self.capabilities = set(capabilities) if capabilities else set()

        # Join groups at instantiation
        for group in self.groups:
            self.join_group(group)

        # Register capabilities with the swarm
        for capability in self.capabilities:
            self.swarm.register_agent_capability(self, capability)

    async def send_message(self, message: str):
        """Send a message to the agent's own queue."""
        await self.swarm.send_to_agent(self.name, message)

    async def broadcast(self, message: str):
        """Broadcast a message to the entire swarm."""
        await self.swarm.broadcast(message)

    def join_group(self, group_name: str):
        """Join a specific group."""
        self.groups.add(group_name)
        self.swarm.add_agent_to_group(self, group_name)

    def leave_group(self, group_name: str):
        """Leave a specific group."""
        if group_name in self.groups:
            self.groups.remove(group_name)
            self.swarm.remove_agent_from_group(self, group_name)

    def add_capability(self, capability: str):
        """Add a new capability to the agent."""
        self.capabilities.add(capability)
        self.swarm.register_agent_capability(self, capability)

    def remove_capability(self, capability: str):
        """Remove a capability from the agent."""
        if capability in self.capabilities:
            self.capabilities.remove(capability)
            self.swarm.unregister_agent_capability(self, capability)

    async def consume_messages(self):
        """Start consuming messages from the agent's queue."""
        async def handle_message(message):
            if self.on_message:
                await self.on_message(message)
            else:
                print(f"{self.name} received: {message}")

        await self.swarm.consume_messages(queue_name=f"agent.{self.name}", callback=handle_message)
    
    async def request_task(self):
        """Request a task from the Swarm based on capabilities."""
        for capability in self.capabilities:
            task = await self.swarm.task_manager.get_task(capability)
            if task:
                print(f"{self.name} received task: {task}")
                await self.execute_task(task)
                return

        print(f"{self.name} found no available tasks.")

    async def execute_task(self, task):
        """
        Execute the task and handle success or failure.
        :param task: The Task object to execute.
        """
        try:
            await task.mark_in_progress()  # Start the task

            # Execute the task and capture the result
            result = await task.execute()

            # Pass the result to mark_completed()
            await task.mark_completed(result)
            print(f"{self.name} successfully completed task {task.task_id}: {result}")

        except Exception as e:
            print(f"{self.name} encountered an error while processing task {task.task_id}: {str(e)}")
            if task.retries > 0:
                task.retries -= 1
                print(f"Retrying task {task.task_id} (remaining retries: {task.retries})")
                await self.execute_task(task)  # Retry the task
            else:
                await task.mark_failed(str(e))
                print(f"Task {task.task_id} failed permanently.")

