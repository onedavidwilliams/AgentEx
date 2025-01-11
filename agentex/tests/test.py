import asyncio
from agentex import CentralHub, Swarm, Agent, AgentTask, AsyncAgentTask
  # For additional logger instantiation if needed


# Mock tasks for testing
class TestSyncTask(AgentTask):
    def execute(self, *args, **kwargs):
        self.result = "Sync task result"
        self.logger.dprint(f"Executing sync task: {self.task_name}", level="info")

class TestAsyncTask(AsyncAgentTask):
    async def execute(self, *args, **kwargs):
        await asyncio.sleep(1)  # Simulate async work
        self.result = "Async task result"
        self.logger.dprint(f"Executing async task: {self.task_name}", level="info")

# Main test function
async def main_swarm():
    # Initialize the central hub
    central_hub = CentralHub()

    # Create swarms
    swarm1 = Swarm("Swarm1", central_hub)
    swarm2 = Swarm("Swarm2", central_hub)

    # Create agents for swarm1
    agent1 = Agent("Agent1", group="main")
    agent2 = Agent("Agent2", group="main")
    swarm1.add_agent(agent1)
    swarm1.add_agent(agent2)

    # Create agents for swarm2
    agent3 = Agent("Agent3", group="analytics")
    agent4 = Agent("Agent4", group="analytics")
    swarm2.add_agent(agent3)
    swarm2.add_agent(agent4)

    print("DEBUG: Swarm2 has agents:", [a.name for a in swarm2.agents])

    # Create and add tasks to swarm1
    sync_task = TestSyncTask(task_name="TestSyncTask", description="A synchronous test task")
    async_task = TestAsyncTask(task_name="TestAsyncTask", description="An asynchronous test task")
    swarm1.add_task(sync_task)
    swarm1.add_task(async_task)

    # Simulate inter-swarm communication
    agent1.send_message("Hello, Agent2", recipient_name="Agent2")
    swarm1.send_message_to_swarm("Hello, Swarm2 team", recipient_swarm_name="Swarm2")

    # Wait for all tasks to complete
    await asyncio.sleep(2)  # Adjust sleep time for async tasks

# Run the test
if __name__ == "__main__":
    asyncio.run(main_swarm())
