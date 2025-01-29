import asyncio
import aiofiles
import os
from agentex.swarms.swarm import Swarm
from agentex.agents.agent import Agent
from agentex.tasks.base_task import BaseTask

class CustomDataTask(BaseTask):
    async def execute(self):
        """Read and process data from sample.txt asynchronously."""
        # Resolve the file path dynamically
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'sample.txt')

        print(f"Reading data from: {file_path}")

        # Open sample.txt asynchronously and read its contents
        async with aiofiles.open(file_path, mode='r') as file:
            contents = await file.read()

        await asyncio.sleep(2)  # Simulate processing time
        print(f"Finished reading data: {contents.strip()}")

        return f"Custom processing complete reading from file -- contents: {contents.strip()}"


async def test_dynamic_task_registration():
    print("Testing dynamic task registration...")

    # Create a local swarm and task manager
    swarm = Swarm(name="TestSwarm", backend="local")
    await swarm.connect()

    # Register custom task types
    swarm.task_manager.register_task_type("custom_data", CustomDataTask)

    # Create an agent with the appropriate capability
    agent = Agent(name="Agent1", swarm=swarm, capabilities=["custom_data"])

    # Add a custom task dynamically
    await swarm.task_manager.add_task("custom_data", {"data": "Dataset B"})

    # Agent requests and processes the custom task
    await agent.request_task()

    await asyncio.sleep(3)  # Allow time for task execution

if __name__ == "__main__":
    asyncio.run(test_dynamic_task_registration())

