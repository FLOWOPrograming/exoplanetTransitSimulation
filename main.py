import pygame
import sys
import math

import mathp

class SpaceObject:
    def __init__(self, radius, colour):
        self.radius = radius
        self.colour = colour
        self.pos = (min(SCREEN_WIDTH, SCREEN_HEIGHT) // 2, min(SCREEN_WIDTH, SCREEN_HEIGHT) // 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)

pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60
GRAPH_START = (600, 600)


# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Space")

clock = pygame.time.Clock()

# Create space objects
star = SpaceObject(radius=100, colour=(255, 255, 150))
planet = SpaceObject(radius=70, colour=(100, 20, 20))
planet.pos = (planet.pos[0] - star.radius - planet.radius - 50, planet.pos[1])

# Graph
graph = [-1 for _ in range(star.pos[0] + star.radius + planet.radius + 50 - planet.pos[0])]
STEP = 600 / len(graph)

def draw_graph(screen, graph, step):
    last_coord = (GRAPH_START[0], GRAPH_START[1])

    for i, ratio in enumerate(graph):
        if ratio < 0:
            break

        x = GRAPH_START[0] + step * i
        y = GRAPH_START[1] - GRAPH_START[1] * ratio

        pygame.draw.line(screen, (255, 100, 100), last_coord, (int(x), int(y)), 2)
        last_coord = (x, y)

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

            if(distance == 0):
                continue

            print(distance)

            overlap = mathp.calculate_intersection_area(star.radius, planet.radius, distance)
            star_area = mathp.circle_area(star.radius)
            difference = star_area - overlap
            ratio = difference / star_area

            graph[graph_time] = ratio
            graph_time += 1

        # Drawing
        screen.fill((0, 0, 0))  # Clear the screen
        star.draw(screen)  # Draw the space object
        planet.draw(screen)
        draw_graph(screen, graph, STEP)  # Draw the graph

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Cap the frame rate

if __name__ == "__main__":
    main()
