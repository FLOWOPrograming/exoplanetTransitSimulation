import random

import pygame
import sys

import mathp
import graphing
import spaceObject
import GUI

pygame.init()

# Constants
SCREEN_WIDTH = 1920/1.4
SCREEN_HEIGHT = 1080/1.4
DISTANCE_FROM_STAR = 10
FPS = 60

# Set up the objects
rng = random
clock = pygame.time.Clock()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exoplanet transit")

# Set up objects
star, planet, graph = (0, 0, 0)

def set_objects(star_radius, planet_radius, targer_radius, pos, distance_from_star):
    scale = targer_radius / star_radius

    star = spaceObject.SpaceObject(star_radius * scale, (255, 255, 150), pos)
    planet = spaceObject.SpaceObject(planet_radius * scale, (50, 20, 20), (0, 0))
    planet.pos = (star.pos[0] - star.radius - planet.radius - distance_from_star, star.pos[1])

    return star, planet


def update_positions(star, planet, speed):
    # Update logic goes here
    planet.pos = [planet.pos[0] + speed, planet.pos[1]]

    max_distance = star.pos[0] + star.radius + planet.radius + DISTANCE_FROM_STAR

    if max_distance < planet.pos[0]:  # check if the planet is max distance away from the star
        planet.pos = (max_distance, planet.pos[1])
        return False

    return True

def reset(star_radius, planet_radius, targer_radius, pos, distance_from_star):
    star, planet = set_objects(star_radius, planet_radius, targer_radius, pos, distance_from_star)

    return star, planet, []

def calculate_overlap_ratio(star, planet):
    distance = abs(planet.pos[0] - star.pos[0])

    if distance <= star.radius - planet.radius:  # planet is inside the sun fully
        difference = mathp.circle_area(star.radius) - mathp.circle_area(planet.radius)
        ratio = difference / mathp.circle_area(star.radius)

        return ratio
    elif distance >= star.radius + planet.radius:  # planet is fully outside the sun
        return 1
    else:  # planet and sun is intersecting
        overlap = mathp.calculate_intersection_area(star.radius, planet.radius, distance)
        star_area = mathp.circle_area(star.radius)
        difference = star_area - overlap
        ratio = difference / star_area

        if ratio > 1:
            ratio = 1

        return ratio


def main():
    star, planet, graph = reset(100, 50, 100,
                               (min(SCREEN_WIDTH, SCREEN_HEIGHT) / 2, min(SCREEN_WIDTH, SCREEN_HEIGHT) / 2),
                               DISTANCE_FROM_STAR)

    starRadiusInput = GUI.InputBox((400, 500), (100, 40), availableSymbols="0123456789", default_value="100")
    planetRadiusInput = GUI.InputBox((400, 550), (100, 40), availableSymbols="0123456789", default_value="10")

    starRadiusText = GUI.Text((220, 500), 'assets/fonts/Roboto-Black.ttf', 32, text="Star radius: ")
    planetRadiusText = GUI.Text((186, 550), 'assets/fonts/Roboto-Black.ttf', 32, text="Planet radius: ")

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                starRadiusInput.key_press(event.key)
                planetRadiusInput.key_press(event.key)

                if int(planetRadiusInput.text) > int(starRadiusInput.text):
                    if(planetRadiusInput.change == True):
                        planetRadiusInput.revert_press()
                    if(starRadiusInput.change == True):
                        starRadiusInput.revert_press()

            if event.type == pygame.MOUSEBUTTONDOWN:
                starRadiusInput.click(pygame.mouse.get_pos())
                planetRadiusInput.click(pygame.mouse.get_pos())

        if starRadiusInput.change or planetRadiusInput.change:
            star, planet, graph = reset(int(starRadiusInput.text), int(planetRadiusInput.text), 100,
                                        (min(SCREEN_WIDTH, SCREEN_HEIGHT) / 2, min(SCREEN_WIDTH, SCREEN_HEIGHT) / 2),
                                        DISTANCE_FROM_STAR)
            starRadiusInput.change = False
            planetRadiusInput.change = False
            continue

        should_update = update_positions(star, planet, 1)

        if should_update:
            ratio = calculate_overlap_ratio(star, planet)

            graph.append(ratio)

        # Drawing
        screen.fill((0, 0, 0))  # Clear the screen
        star.draw(screen)  # Draw the space object
        planet.draw(screen)

        starRadiusInput.draw(screen)
        planetRadiusInput.draw(screen)

        starRadiusText.draw(screen)
        planetRadiusText.draw(screen)

        graphing.graph(screen, graph, (SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT - 100), (SCREEN_WIDTH - 50, 50))  # Draw the graph

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Cap the frame rate


if __name__ == "__main__":
    main()
