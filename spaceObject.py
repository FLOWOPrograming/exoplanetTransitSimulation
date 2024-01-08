import pygame

class SpaceObject:
    def __init__(self, radius, colour, pos):
        self.radius = radius
        self.colour = colour
        self.pos = pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)