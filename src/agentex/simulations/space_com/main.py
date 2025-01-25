import asyncio
import pygame
import random
import os
from agentex.simulations.space_com.terrain import TerrainManager
from agentex.simulations.space_com.agents import CollectorShipMiner
from agentex.simulations.space_com.tasks import assign_new_task
from agentex import CentralHub, Swarm
from agentex.logging.logger import LoggerWrapper
import math

def generate_random_base_positions(num_bases, screen_width, screen_height, min_distance=200):
    """
    Generate random base positions, ensuring they are at least min_distance apart.
    """
    base_positions = []
    while len(base_positions) < num_bases:
        x, y = random.randint(100, screen_width - 100), random.randint(100, screen_height - 100)
        if all(math.dist((x, y), pos) >= min_distance for pos in base_positions):
            base_positions.append((x, y))
    return base_positions

# Screen settings
WIDTH, HEIGHT = 1200, 800
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SHIPS_DIR = os.path.join(ASSETS_DIR, "ships")
OBJECTS_DIR = os.path.join(ASSETS_DIR, "objects")
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AgentEx Space Simulation")

# Load assets
speeder_image = pygame.image.load(os.path.join(SHIPS_DIR, "craft_speederA_NE.png")).convert_alpha()
rock_image = pygame.image.load(os.path.join(OBJECTS_DIR, "rock_largeA_NE.png")).convert_alpha()
# Load hangar images for the bases
base_positions = generate_random_base_positions(4, WIDTH, HEIGHT)
base_images = [
    pygame.transform.scale(
        pygame.image.load(os.path.join(OBJECTS_DIR, f"hangar_smallA_{direction}.png")).convert_alpha(),
        (160, 160)  # 4 times the size of the speeder
    )
    for direction in ["NE", "NW", "SE", "SW"]
]
bases = {f"CollectorShip_{i}": (base_positions[i], base_images[i]) for i in range(4)}

speeder_image = pygame.transform.scale(speeder_image, (80, 80))
rock_image = pygame.transform.scale(rock_image, (90, 90))

RESOURCE_POINTS = {
    (random.randint(50, 750), random.randint(50, 550)): random.randint(10, 20)  # Random capacity for each point
    for _ in range(5)
}
resource_status = {point: capacity for point, capacity in RESOURCE_POINTS.items()}
async def run_simulation():
    logger = LoggerWrapper(log_level=0)
    terrain_manager = TerrainManager(BASE_DIR)
    central_hub = CentralHub(logger=logger)
    swarm = Swarm("ResourceCollectionSwarm", central_hub=central_hub, logger=logger)

    collector_ships = [
        CollectorShipMiner(
            f"CollectorShip_{i}",
            speeder_image,
            (random.randint(100, 700), random.randint(100, 500)),
            base_positions[i],
            base_width=base_images[i].get_width(),
            base_height=base_images[i].get_height(),
            logger=logger
        )
        for i in range(4)
    ]
    for ship in collector_ships:
        swarm.add_agent(ship)

    # Start assigning tasks in the background
    asyncio.create_task(assign_new_task(swarm, resource_status))

    # Draw the static bases once
    for ship_name, (base_pos, base_image) in bases.items():
        screen.blit(base_image, base_pos)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 30))  # Clear the screen for updates

        # Draw terrain and bases
        terrain_manager.draw_terrain(screen, WIDTH, HEIGHT)
        for ship_name, (base_pos, base_image) in bases.items():
            screen.blit(base_image, base_pos)

        # Draw resources
        for point, capacity in resource_status.items():
            if capacity > 0:
                screen.blit(rock_image, point)

        # Draw ships (only visual updates)
        for ship in collector_ships:
            ship.draw(screen)

        pygame.display.flip()
        await asyncio.sleep(0.03)

    pygame.quit()



if __name__ == "__main__":
    asyncio.run(run_simulation())
