import pygame
import os

class TerrainManager:
    def __init__(self, base_dir, tile_width=128, tile_height=64):
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_width_half = tile_width // 2
        self.tile_height_half = tile_height // 2

        objects_dir = os.path.join(base_dir, "assets")
        terrain_path = os.path.join(objects_dir, "terrain/terrain_SW.png")
        self.terrain_tile = pygame.image.load(terrain_path).convert_alpha()

    def map_to_screen(self, map_x, map_y):
        screen_x = (map_x - map_y) * self.tile_width_half
        screen_y = (map_x + map_y) * self.tile_height_half
        return screen_x, screen_y

    def draw_terrain(self, screen, screen_width, screen_height):
        max_tiles_x = screen_width // self.tile_width_half + 4
        max_tiles_y = screen_height // self.tile_height_half + 4

        for x in range(-max_tiles_x, max_tiles_x):
            for y in range(-max_tiles_y, max_tiles_y):
                screen_x, screen_y = self.map_to_screen(x, y)
                tile_x = screen_x - self.tile_width_half
                tile_y = screen_y - self.tile_height
                screen.blit(self.terrain_tile, (tile_x, tile_y))
