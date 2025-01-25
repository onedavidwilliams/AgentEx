import asyncio
import random
from agentex import AsyncAgentTask
from exlog import ExLog
from agentex.logging.logger import LoggerWrapper
class CollectResourceTask(AsyncAgentTask):
    def __init__(self, name, description, resource_point, resource_type="Resource", resource_status=None, logger=None):
        super().__init__(name, description, logger=logger)
        self.resource_point = resource_point
        self.resource_type = resource_type
        self.resources_collected = random.randint(3, 5)  # Random number of units collected
        self.resource_status =  resource_status
    
    async def execute(self):
        agent = self.agent
        
        try:
            while not agent.has_arrived:
                self.logger.dprint(f"{agent.name} moving to {self.resource_point}. Current position: {agent.x, agent.y}", level="debug")
                await agent.move_to(*self.resource_point)
                await asyncio.sleep(0.03)  # Wait until the ship arrives

            await asyncio.sleep(1.0)  # Simulate collection time

            # Update resources
            if self.resource_status[self.resource_point] > 0 and agent.has_arrived:
                self.resource_status[self.resource_point] -= self.resources_collected
                agent.resources_collected += self.resources_collected
                self.logger.dprint(f"{agent.name} collected {self.resources_collected} units. Remaining at {self.resource_point}: {self.resource_status[self.resource_point]}", level="info")

                if self.resource_status[self.resource_point] <= 0:
                    self.logger.dprint(f"Resource at {self.resource_point} depleted!", level="warning")

            
        finally:
            # Reset flags properly
            agent.collecting = False
            agent.has_arrived = False
            agent.returning_base = True
            agent.target = None  # Clear target after collection
            result = f"Collected {self.resources_collected} resources"
            return result


    
class ReturnToBaseTask(AsyncAgentTask):
    """A task that handles returning the ship to its base."""
    def __init__(self, name, description, location, logger=None):
        super().__init__(name, description, logger=logger)
        self.location = location  # Base position
        
    async def execute(self):
        agent = self.agent
        bx, by = agent.base_position
        bx += agent.base_width // 2
        by += agent.base_height // 2
        resources_to_drop = agent.resources_collected
        try:
            
            self.logger.dprint(f"{agent.name} returning to base at ({bx}, {by}).", level="info")
            await agent.move_to(bx, by)  # Move to base

            # Simulate unloading resources
            await asyncio.sleep(1.0)
            self.logger.dprint(f"{agent.name} unloaded {resources_to_drop} resources at base.", level="info")
            agent.resources_collected = 0  # Reset collected resources

        finally:
            # Reset flags properly
            agent.collecting = False
            agent.returning_base = False
            agent.has_arrived = False
            agent.target = None
            result=f"Collected {resources_to_drop} resources"
            return result

def is_at_base(agent, tolerance=2):
    bx, by = agent.base_position
    bx += agent.base_width // 2
    by += agent.base_height // 2
    at_base = (
        abs(agent.x - bx) <= tolerance and
        abs(agent.y - by) <= tolerance
    )
    return at_base


async def assign_new_task(swarm, resource_status):
    logger = LoggerWrapper(log_level=0, use_exlog=True)
    while True:
        for ship in swarm.agents:
            # Skip if the ship already has a task
            if ship.task:
                #logger.dprint(f"{ship.name} is still processing task '{ship.task.task_name}'.", level="debug")
                continue

            at_base = is_at_base(ship)

            # Assign return-to-base task
            if ship.resources_collected > 0 and ship.returning_base and not at_base:
                logger.dprint(f"{ship.name} is assigned a return-to-base task. Are they at the base: {at_base}", level="info")
                return_task = ReturnToBaseTask(
                    name=f"{ship.name}_ReturnToBase",
                    description="Return to base after collecting resources",
                    location=ship.base_position,
                    logger=logger
                )
                return_task.agent = ship
                ship.target = ship.base_position
                await ship.async_assign_task(return_task)
                continue

            # Assign resource collection task
            if not ship.target and not ship.returning_base and not ship.collecting:
                available_resources = [point for point, available in resource_status.items() if available]
                if available_resources:
                    resource = random.choice(available_resources)
                    resource_type = random.choice(["Rock", "Minerals", "Ice Crystals"])
                    task = CollectResourceTask(
                        name=f"CollectResource_{ship.name}",
                        description="Collect resource",
                        resource_point=resource,
                        resource_type=resource_type,
                        resource_status=resource_status,
                        logger=logger
                    )
                    task.agent = ship
                    ship.target = task.resource_point
                    ship.collecting = True
                    # ship.task = task  # Assign task to the ship first
                    logger.dprint(f"Assigning new resource collection task '{task.task_name}' to '{ship.name}'.", level="info")
                    await ship.async_assign_task(task)
        await asyncio.sleep(0.1)  # Prevent busy looping

