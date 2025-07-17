import sys
import random
import pygame

import mathp
import graphing
import spaceObject
import GUI

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
DISTANCE_FROM_STAR = 10
FPS = 60
SCALE_TARGET_RADIUS = 100

# Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exoplanet Transit Simulator")
clock = pygame.time.Clock()

class Simulation:
    def __init__(self):
        self.star = None
        self.planet = None
        self.graph = []
        self.reset_objects(100, 50)

    def reset_objects(self, star_radius, planet_radius):
        self.star, self.planet = self._create_objects(
            star_radius,
            planet_radius,
            SCALE_TARGET_RADIUS,
            (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2),
            DISTANCE_FROM_STAR
        )
        self.graph = []

    def _create_objects(self, star_radius, planet_radius, target_radius, center_pos, distance):
        scale = target_radius / star_radius
        star = spaceObject.SpaceObject(star_radius * scale, (255, 255, 150), center_pos)
        planet = spaceObject.SpaceObject(planet_radius * scale, (70, 30, 30), (0, 0))
        planet.pos = (
            star.pos[0] - star.radius - planet.radius - distance,
            star.pos[1]
        )
        return star, planet

    def update(self, speed=1):
        self.planet.pos = [self.planet.pos[0] + speed, self.planet.pos[1]]
        max_distance = self.star.pos[0] + self.star.radius + self.planet.radius + DISTANCE_FROM_STAR
        if self.planet.pos[0] > max_distance:
            self.planet.pos = (max_distance, self.planet.pos[1])
            return False
        return True

    def calculate_overlap_ratio(self):
        distance = abs(self.planet.pos[0] - self.star.pos[0])
        star_area = mathp.circle_area(self.star.radius)

        if distance <= self.star.radius - self.planet.radius:
            ratio = (star_area - mathp.circle_area(self.planet.radius)) / star_area
        elif distance >= self.star.radius + self.planet.radius:
            ratio = 1
        else:
            overlap = mathp.calculate_intersection_area(self.star.radius, self.planet.radius, distance)
            ratio = (star_area - overlap) / star_area

        return min(ratio, 1)

    def draw(self, surface):
        self.star.draw(surface)
        self.planet.draw(surface)


class UI:
    def __init__(self):
        self.star_input = GUI.InputBox((400-150, SCREEN_HEIGHT - 130), (100, 40), availableSymbols="0123456789", default_value="100")
        self.planet_input = GUI.InputBox((400-150, SCREEN_HEIGHT - 80), (100, 40), availableSymbols="0123456789", default_value="10")

        self.star_label = GUI.Text((220-150, SCREEN_HEIGHT - 130), 'assets/fonts/Roboto-Black.ttf', 32, text="Star radius: ")
        self.planet_label = GUI.Text((186-150, SCREEN_HEIGHT - 80), 'assets/fonts/Roboto-Black.ttf', 32, text="Planet radius: ")

    def draw(self, surface):
        self.star_input.draw(surface)
        self.planet_input.draw(surface)
        self.star_label.draw(surface)
        self.planet_label.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.star_input.key_press(event.key)
            self.planet_input.key_press(event.key)

            # Prevent planet from being larger than the star
            if int(self.planet_input.text) > int(self.star_input.text):
                if self.planet_input.change:
                    self.planet_input.revert_press()
                if self.star_input.change:
                    self.star_input.revert_press()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.star_input.click(pygame.mouse.get_pos())
            self.planet_input.click(pygame.mouse.get_pos())

    def has_changes(self):
        return self.star_input.change or self.planet_input.change

    def reset_changes(self):
        self.star_input.change = False
        self.planet_input.change = False

    def get_radii(self):
        return int(self.star_input.text), int(self.planet_input.text)


def handle_events(ui):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        ui.handle_event(event)


def main():
    sim = Simulation()
    ui = UI()

    while True:
        handle_events(ui)

        if ui.has_changes():
            star_r, planet_r = ui.get_radii()
            sim.reset_objects(star_r, planet_r)
            ui.reset_changes()
            continue

        if sim.update():
            sim.graph.append(sim.calculate_overlap_ratio())

        # Draw
        screen.fill((0, 0, 0))
        sim.draw(screen)
        ui.draw(screen)
        graphing.graph(screen, sim.graph, (SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT - 100), (SCREEN_WIDTH - 50, 50))
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
