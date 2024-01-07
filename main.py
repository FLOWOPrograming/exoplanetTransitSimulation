import random

import pygame
import sys
import math

import mathp
import graphing

class SpaceObject:
    def __init__(self, radius, colour):
        self.radius = radius
        self.colour = colour
        self.pos = (min(SCREEN_WIDTH, SCREEN_HEIGHT) / 2, min(SCREEN_WIDTH, SCREEN_HEIGHT) / 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)

pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60
GRAPH_START = (600, 600)
rng = random

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exoplanet transit")

clock = pygame.time.Clock()

# Create space objects
star = SpaceObject(radius=100, colour=(255, 255, 150))
planet = SpaceObject(radius=5, colour=(50, 20, 20))
planet.pos = (planet.pos[0] - star.radius - planet.radius - 50, planet.pos[1])

# Graph
graph = []

def main():
    graph_time = 0

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update logic goes here
        if planet.pos[0] + 1 < star.pos[0] + star.radius + planet.radius + 50:
            planet.pos = [planet.pos[0] + 1, planet.pos[1]]

            distance = math.sqrt((planet.pos[0] - star.pos[0]) ** 2)
            ratio = 0

            if (distance <= star.radius-planet.radius):
                difference = mathp.circle_area(star.radius) - mathp.circle_area(planet.radius)
                ratio = difference / mathp.circle_area(star.radius)
            elif (distance >= star.radius + planet.radius):
                ratio = 1
            elif (distance <= star.radius and distance > star.radius - planet.radius):
                overlap = mathp.calculate_intersection_area(star.radius, planet.radius, distance)
                star_area = mathp.circle_area(star.radius)
                difference = star_area - overlap
                ratio = difference / star_area
            else:
                overlap = mathp.calculate_intersection_area(star.radius, planet.radius, distance)
                star_area = mathp.circle_area(star.radius)
                difference = star_area - overlap
                ratio = difference / star_area

            #ratio += rng.randint(0, 100) / 20000

            graph.append(ratio)
            graph_time += 1

        # Drawing
        screen.fill((0, 0, 0))  # Clear the screen
        star.draw(screen)  # Draw the space object
        planet.draw(screen)
        graphing.graph(screen, graph, (700, 500), (1100, 100))  # Draw the graph

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Cap the frame rate

if __name__ == "__main__":
    main()
