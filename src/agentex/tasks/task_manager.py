import asyncio
from collections import defaultdict
from .task import Task

class TaskManager:
    def __init__(self):
        """
        Initialize the TaskManager with separate queues for different task types.
        """
        self.task_queues = defaultdict(asyncio.Queue)  # Task queues per capability
        self.task_registry = {}  # Dynamically registered task types

    def register_task_type(self, task_type: str, task_class):
        """
        Register a custom task type.
        :param task_type: The name of the task type.
        :param task_class: The class implementing the task logic.
        """
        if task_type in self.task_registry:
            raise ValueError(f"Task type '{task_type}' is already registered.")
        self.task_registry[task_type] = task_class
        print(f"Task type '{task_type}' registered successfully.")

    async def add_task(self, task_type: str, payload: dict, retries: int = 0):
        """
        Create a task instance dynamically and add it to the appropriate queue.
        """
        task_class = self.task_registry.get(task_type)
        if task_class is None:
            raise ValueError(f"Unknown task type: {task_type}. Please register it first.")

        task = task_class(task_type, payload, retries)
        await self.task_queues[task_type].put(task)
        print(f"Task '{task_type}' added to queue with payload: {payload}")

    async def get_task(self, capability: str):
        """
        Retrieve a task from the queue for a specific capability.
        """
        if capability in self.task_queues and not self.task_queues[capability].empty():
            task = await self.task_queues[capability].get()
            await task.mark_in_progress()
            print(f"Task {task.task_type} assigned to agent with capability '{capability}'.")
            return task
        else:
            return None
