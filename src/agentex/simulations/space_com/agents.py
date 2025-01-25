import pygame
import asyncio
from agentex import Agent

SCAN_RADIUS = 100
AGENT_SPEED = 2

class CollectorShipMiner(Agent):
    def __init__(self, name, image, pos, base_position, base_width, base_height, logger=None):
        super().__init__(name, logger=logger)
        self.image = image
        self.x, self.y = pos
        self.base_position = base_position  # Just the top-left position
        self.base_width = base_width
        self.base_height = base_height
        self.target = None
        self.collecting = False
        self.has_arrived = False
        self.resources_collected = 0
        self.lock = asyncio.Lock()
        self.font = pygame.font.SysFont(None, 12)
        self.returning_base = False
        self.speed = 2
        self.has_task = False 

    def draw(self, surface):
        # Define the pivot point offsets for isometric alignment
        pivot_x_offset = self.image.get_width() // 2  # Adjust based on isometric analysis
        pivot_y_offset = self.image.get_height() // 2 + 8  # Example adjustment, tweak as needed

        detection_color = (0, 255, 255, 80)
        s = pygame.Surface((SCAN_RADIUS * 2, SCAN_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, detection_color, (SCAN_RADIUS, SCAN_RADIUS), SCAN_RADIUS)
        surface.blit(s, (self.x - SCAN_RADIUS + pivot_x_offset,
                        self.y - SCAN_RADIUS + pivot_y_offset))

        shield_color = (0, 255, 0)
        pygame.draw.circle(surface, shield_color,
                        (int(self.x + pivot_x_offset),
                            int(self.y + pivot_y_offset)), 20, 2)
        surface.blit(self.image, (self.x, self.y))

        # Render and draw the ship's name above the ship
        text_surface = self.font.render(self.name, True, (255, 255, 255))  # White color
        text_rect = text_surface.get_rect(center=(self.x + pivot_x_offset,
                                                self.y - 18 + pivot_y_offset))  # Center text above the ship
        surface.blit(text_surface, text_rect)


    
    def set_target(self, target):
        self.target = target
        self.has_arrived = False
        self.collecting = False

    async def move_to(self, tx, ty):
        self.has_arrived = False  # Reset before moving
        while ((self.x - tx) ** 2 + (self.y - ty) ** 2) ** 0.5 > 2:
            dx, dy = tx - self.x, ty - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > self.speed:
                self.x += self.speed * (dx / distance)
                self.y += self.speed * (dy / distance)
            else:
                self.x, self.y = tx, ty  # Snap to position
                break
            await asyncio.sleep(0.03)
        self.has_arrived = True  # Mark as arrived
        self.logger.dprint(f"{self.name} arrived at ({tx}, {ty})", level="info")

