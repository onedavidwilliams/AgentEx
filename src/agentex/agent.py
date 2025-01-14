

import asyncio
from abc import ABC, abstractmethod
from exlog import ExLog
from .tasks import AgentTask, AsyncAgentTask

class Agent:
    def __init__(self, name, group='main', message_callback=None, send_callback=None, logger=None):
        """
        Initialize an Agent.
        :param name: The agent's name.
        :param group: The group name the agent belongs to.
        :param message_callback: A callback function triggered when the agent receives a message.
        :param send_callback: A callback function triggered after sending a message.
        """
        self.name = name
        self.task = None
        self.swarm = None
        self.groups = ['main'] if group == 'main' else ['main', group]
        self.logger = logger or ExLog(log_level=1) # You can change this within the instantiation for your own scripts to be silent just set logger=ExLog(log_level=0)
        self.message_callback = message_callback  # Function called on receive
        self.send_callback = send_callback  # Function called after sending

    def set_swarm(self, swarm):
        """Assign the agent to a swarm."""
        self.swarm = swarm


    def is_available(self):
        """Check if the agent is available to take on a task."""
        return self.task is None

    # Task Assignment (Sync + Async)
    def assign_task(self, task):
        """Assign a task synchronously."""
        self.task = task
        asyncio.create_task(self.execute_task())

    async def async_assign_task(self, task, print_full_result=True):
        """Assign a task asynchronously."""
        self.task = task
        await self.execute_task(print_full_result=print_full_result)

    async def execute_task(self, print_full_result=True):
        """
        Execute the assigned task.

        Parameters:
        - print_full_result (bool): If True, prints the full result; if False, prints a success message without the full result.
        """
        if isinstance(self.task, AsyncAgentTask):
            await self.task.run_task()  # Asynchronous task
        else:
            self.task.run_task()  # Synchronous task

        result = self.task.get_result()  # Retrieve the result after task completion

        if print_full_result:
            self.logger.dprint(f"Task '{self.task.task_name}' completed by '{self.name}'. Result: {result}", level="info")
        else:
            self.logger.dprint(f"Task '{self.task.task_name}' completed successfully by '{self.name}'", level="info")

        self.task = None
        self.swarm.notify_task_completed(self, result, print_full_result=print_full_result)

    # Sending Messages (Sync + Async)
    def send_message(self, message, recipient_name=None, group_name=None):
        """Send a message synchronously."""
        self.logger.dprint(f"Agent '{self.name}' sending message: '{message}'", level="info")
        self.swarm.communicate(message, self, recipient_name, group_name)

        # Call the send callback if defined
        if self.send_callback:
            self.send_callback(self.name, message, recipient_name, group_name)

    async def async_send_message(self, message, recipient_name=None, group_name=None):
        """Send a message asynchronously."""
        self.logger.dprint(f"[ASYNC] Agent '{self.name}' sending message: '{message}'", level="info")
        await self.swarm.async_communicate(message, self, recipient_name, group_name)

        # Call the async send callback if defined
        if self.send_callback:
            await self.send_callback(self.name, message, recipient_name, group_name)

    # Receiving Messages (Sync + Async)
    def receive_message(self, message, sender, from_groups=None, to_group=None):
        """Synchronously receive a message."""
        if from_groups is None:
            from_groups = []
        self.logger.dprint(f"Agent '{self.name}' received message from '{sender}' (groups={from_groups}, to_group={to_group}): '{message}'", level="info")

        # Trigger the external receive callback if provided
        if self.message_callback:
            self.message_callback(self.name, message, sender, from_groups, to_group)

    async def async_receive_message(self, message, sender, from_groups=None, to_group=None):
        """Asynchronously receive a message."""
        if from_groups is None:
            from_groups = []
        self.logger.dprint(f"[ASYNC] Agent '{self.name}' received message from '{sender}' (groups={from_groups}, to_group={to_group}): '{message}'", level="info")
        await asyncio.sleep(0)  # Yield control

        if self.message_callback:
            await self.message_callback(self.name, message, sender, from_groups, to_group)
