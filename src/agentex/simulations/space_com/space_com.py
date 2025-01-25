import pygame
import random
import sys
import asyncio
import os
from agentex import Swarm, CentralHub, Agent, AsyncAgentTask
from agentex.logging.logger import LoggerWrapper
from agentex.simulations.space_com.iso import TerrainManager

# Screen settings
WIDTH, HEIGHT = 800, 600
AGENT_SPEED = 2  # Pixels per frame
SCAN_RADIUS = 100  # Scan range for detecting nearby ships heading to the same resource

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AgentEx Space Simulation")

# Paths setup (relative paths)
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SHIPS_DIR = os.path.join(ASSETS_DIR, "ships")
OBJECTS_DIR = os.path.join(ASSETS_DIR, "objects")
import os
print(f"Current Working Directory (CWD): {os.getcwd()}")

if not os.path.exists(os.path.join(SHIPS_DIR, "craft_speederA_NE.png")):
    raise FileNotFoundError("Speeder image not found at: " + os.path.join(SHIPS_DIR, "craft_speederA_NE.png"))

# Load assets
speeder_image = pygame.image.load(os.path.join(SHIPS_DIR, "craft_speederA_NE.png")).convert_alpha()
rock_image = pygame.image.load(os.path.join(OBJECTS_DIR, "rock_largeA_NE.png")).convert_alpha()
speeder_image = pygame.transform.scale(speeder_image, (40, 40))
rock_image = pygame.transform.scale(rock_image, (50, 50))

# Fixed resource points
RESOURCE_POINTS = [(random.randint(50, 750), random.randint(50, 550)) for _ in range(5)]

# --------- Task Implementations --------- #
class CollectResourceTask(AsyncAgentTask):
    def __init__(self, task_name, description, resource_point, logger=None, silent=False):
        super().__init__(task_name, description, logger)
        self.resource_point = resource_point
        self.silent = silent  # Enable silent mode for this task

    def log(self, message, level="info"):
        """Override log to respect silent mode."""
        if not self.silent:
            super().log(message, level)

    async def execute(self):
        """Simulate collecting the resource."""
        while not self.agent.has_arrived:
            await asyncio.sleep(0.03)  # Wait until ship arrives visually
        self.log(f"[COLLECTION] Resource at {self.resource_point} is being collected", level="info")
        await asyncio.sleep(1.0)  # Simulate collection delay
        self.result = self.resource_point  # Mark the collection point as result
        self.log("---Async task completed successfully.", level="debug")
        return self.resource_point


# --------- CollectorShipMiner Class --------- #
# --------- CollectorShipMiner Class --------- #
class CollectorShipMiner(Agent):
    def __init__(self, name, image, pos, logger=None):
        super().__init__(name, logger=logger)
        self.image = image
        self.x, self.y = pos
        self.target = None  # The resource target point
        self.collecting = False  # Is collecting resource
        self.has_arrived = False  # Has visually arrived at target

    def draw(self, surface):
        """Draw the ship and its detection range + shield."""
        # Draw detection range (semi-transparent circle)
        detection_color = (0, 255, 255, 80)  # Light blue with transparency
        s = pygame.Surface((SCAN_RADIUS * 2, SCAN_RADIUS * 2), pygame.SRCALPHA)  # Transparent surface
        pygame.draw.circle(s, detection_color, (SCAN_RADIUS, SCAN_RADIUS), SCAN_RADIUS)
        surface.blit(s, (self.x - SCAN_RADIUS + 20, self.y - SCAN_RADIUS + 20))

        # Draw shield (solid green circle)
        shield_color = (0, 255, 0)  # Light green color
        pygame.draw.circle(surface, shield_color, (int(self.x + 20), int(self.y + 20)), 20, 2)  # 2-pixel thickness

        # Draw the ship itself
        surface.blit(self.image, (self.x, self.y))

    def set_target(self, target):
        """Set the resource target."""
        self.target = target
        self.has_arrived = False  # Reset arrival status
        self.collecting = False  # Reset collecting status

    async def move_toward_target(self, resource_status):
        """Move ship toward the assigned resource point."""
        if not self.target or self.collecting:  # Don't move if already collecting or no target
            return

        # Check if resource is still available
        async with self.lock:
            if not resource_status.get(self.target, True):
                self.logger.dprint(f" Resource at {self.target} is gone. {self.name} is searching for a new resource.", level="warning")
                self.target = None  # Reset target
                self.collecting = False
                self.has_arrived = False
                return

        tx, ty = self.target  # Target x and y
        dx, dy = tx - self.x, ty - self.y  # Distance delta
        distance = (dx ** 2 + dy ** 2) ** 0.5  # Euclidean distance

        if distance > AGENT_SPEED:
            # Move incrementally toward the target
            self.x += AGENT_SPEED * (dx / distance)
            self.y += AGENT_SPEED * (dy / distance)
        else:
            # Reached the target
            self.x, self.y = tx, ty
            self.has_arrived = True  # Mark as visually arrived

            async with self.lock:
                # Check resource again at arrival
                if not resource_status.get(self.target, True):
                    self.logger.dprint(f"[INFO] {self.name} arrived but resource at {self.target} was already collected.", level="info")
                    self.target = None  # Reset target
                    self.collecting = False
                    self.has_arrived = False
                    return
                else:
                    # Start collecting if resource is still available
                    self.logger.dprint(f"[INFO] {self.name} started collecting at {self.target}", level="info")
                    resource_status[self.target] = False  # Mark resource as collected
                    self.collecting = True


    def is_conflict(self, swarm):
        """
        Check if another ship is heading toward the same target within scan range.
        If conflict detected, return True.
        """
        if not self.target or self.collecting:  # If collecting, no conflict resolution needed
            return False

        for other_ship in swarm.agents:
            if other_ship != self and other_ship.target == self.target:
                # Skip ships already collecting at the resource
                if other_ship.collecting:
                    continue
                distance = ((other_ship.x - self.x) ** 2 + (other_ship.y - self.y) ** 2) ** 0.5
                if distance <= SCAN_RADIUS:
                    return True
        return False


# --------- CollectorShipMiner Class --------- #
class CollectorShipMiner(Agent):
    def __init__(self, name, image, pos, logger=None):
        super().__init__(name, logger=logger)
        self.image = image
        self.x, self.y = pos
        self.target = None  # The resource target point
        self.collecting = False  # Is collecting resource
        self.has_arrived = False  # Has visually arrived at target
        self.lock = asyncio.Lock()  # Lock for resource assignment

    def set_target(self, target):
        """Set the resource target."""
        self.target = target
        self.has_arrived = False  # Reset arrival status
        self.collecting = False  # Reset collecting status

    async def move_toward_target(self, resource_status):
        """Move ship toward the assigned resource point."""
        if not self.target or self.collecting:  # Don't move if already collecting or no target
            return

        # Check if resource is still available
        async with self.lock:
            if not resource_status.get(self.target, True):
                self.logger.dprint(f"[INFO] Resource at {self.target} is gone. {self.name} is searching for a new resource.", level="info")
                self.target = None  # Reset target
                self.collecting = False
                self.has_arrived = False
                return

        tx, ty = self.target  # Target x and y
        dx, dy = tx - self.x, ty - self.y  # Distance delta
        distance = (dx ** 2 + dy ** 2) ** 0.5  # Euclidean distance

        if distance > AGENT_SPEED:
            # Move incrementally toward the target
            self.x += AGENT_SPEED * (dx / distance)
            self.y += AGENT_SPEED * (dy / distance)
        else:
            # Reached the target
            self.x, self.y = tx, ty
            self.has_arrived = True  # Mark as visually arrived

            async with self.lock:
                # Check resource again at arrival
                if not resource_status.get(self.target, True):
                    self.logger.dprint(f"[INFO] {self.name} arrived but resource at {self.target} was already collected.", level="info")
                    self.target = None  # Reset target
                    self.collecting = False
                    self.has_arrived = False
                    return
                else:
                    # Start collecting if resource is still available
                    self.logger.dprint(f"[INFO] {self.name} started collecting at {self.target}", level="info")
                    resource_status[self.target] = False  # Mark resource as collected
                    self.collecting = True

    def draw(self, surface):
        """Draw the ship and its detection range + shield."""
        # Draw detection range (semi-transparent circle)
        detection_color = (0, 255, 255, 80)  # Light blue with transparency
        s = pygame.Surface((SCAN_RADIUS * 2, SCAN_RADIUS * 2), pygame.SRCALPHA)  # Transparent surface
        pygame.draw.circle(s, detection_color, (SCAN_RADIUS, SCAN_RADIUS), SCAN_RADIUS)
        surface.blit(s, (self.x - SCAN_RADIUS + 20, self.y - SCAN_RADIUS + 20))

        # Draw shield (solid green circle)
        shield_color = (0, 255, 0)  # Light green color
        pygame.draw.circle(surface, shield_color, (int(self.x + 20), int(self.y + 20)), 20, 2)  # 2-pixel thickness

        # Draw the ship itself
        surface.blit(self.image, (self.x, self.y))

    def is_conflict(self, swarm):
        """
        Check if another ship is heading toward the same target within scan range.
        If conflict detected, return True.
        """
        if not self.target or self.collecting:  # If collecting, no conflict resolution needed
            return False

        for other_ship in swarm.agents:
            if other_ship != self and other_ship.target == self.target:
                if other_ship.collecting or other_ship.has_arrived:
                    continue  # Skip if the other ship is already collecting

                # Calculate distance
                distance = ((other_ship.x - self.x) ** 2 + (other_ship.y - self.y) ** 2) ** 0.5
               

                # Ensure correct detection within scan radius
                if distance <= SCAN_RADIUS:
                    return True

        return False




# --------- Main Game Loop --------- #
async def assign_new_task(swarm, resource_status):
    """Background task to continuously assign new tasks."""
    logger = LoggerWrapper(log_level="info", use_exlog=True)
    resource_lock = asyncio.Lock()  # Lock to prevent race conditions
    while True:
        for ship in swarm.agents:
            if ship.collecting:  # Skip conflict check if already collecting
                continue

            # If no target, assign a new one
            if not ship.target:
                async with resource_lock:  # Lock resource assignment
                    available_resources = [point for point, available in resource_status.items() if available]
                    if available_resources:
                        new_target = random.choice(available_resources)
                        task = CollectResourceTask("CollectResource", "Collect resource", new_target, logger=logger, silent=True)
                        task.agent = ship  # Pass reference of the agent to task for synchronization
                        ship.set_target(new_target)
                        resource_status[new_target] = True  # Ensure it is marked as available during travel
                        asyncio.create_task(ship.async_assign_task(task))  # Create async task without blocking

            # Conflict check: divert to another resource if conflict detected
            if ship.is_conflict(swarm):
                logger.dprint(f"[DIVERT] {ship.name} detected another ship heading toward {ship.target}. Diverting...", level="warning")
                other_resources = [point for point in resource_status if point != ship.target and resource_status[point]]
                if other_resources:
                    new_target = random.choice(other_resources)
                    ship.set_target(new_target)
                    logger.dprint(f"{ship.name} changed course to {new_target}", level="info")

        await asyncio.sleep(0.1)


async def run_simulation():
    logger = LoggerWrapper(log_level="info", use_exlog=True)
    terrain_manager = TerrainManager(BASE_DIR)
    # Central Hub and Swarm Setup
    central_hub = CentralHub(logger=logger)
    swarm = Swarm("ResourceCollectionSwarm", central_hub=central_hub, logger=logger)

    # Create CollectorShips
    collector_ships = [CollectorShipMiner(f"CollectorShip_{i}", speeder_image, (random.randint(100, 700), random.randint(100, 500)), logger=logger) for i in range(4)]
    for ship in collector_ships:
        swarm.add_agent(ship)

    # Resource Points and Status
    resource_status = {point: True for point in RESOURCE_POINTS}
    # Background task to continuously assign tasks
    asyncio.create_task(assign_new_task(swarm, resource_status))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 30))  # Clear screen
        terrain_manager.draw_terrain(screen, WIDTH, HEIGHT)
        for point, available in resource_status.items():
            if available:
                screen.blit(rock_image, point)  # Draw resources

        for ship in collector_ships:
            await ship.move_toward_target(resource_status)
        #     if ship.has_arrived and ship.collecting:
        #         logger.dprint(f"{ship.name} collected resource at {ship.target}", level="info")

            ship.draw(screen)

        pygame.display.flip()
        await asyncio.sleep(0.03)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(run_simulation())
