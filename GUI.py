import pygame
import math

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class InputBox:
    def __init__(self, pos, size, default_value='', availableSymbols=""):
        self.rect = pygame.Rect(pos, size)
        self.color = GRAY
        self.text = default_value
        self.availableSymbols = availableSymbols
        self.default_value = default_value
        self.last_value = default_value
        self.selected = False
        self.change = False

    def draw(self, surface):
        self.change = False
        pygame.draw.rect(surface, self.color, self.rect, 2)
        font = pygame.font.Font('assets/fonts/Roboto-Black.ttf', 32)
        text_surface = font.render(self.text, True, WHITE)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.selected = True
        else:
            self.selected = False

    def key_press(self, key):
        if self.selected:
            if key == pygame.K_BACKSPACE:
                self.last_value = self.text
                self.text = self.text[:-1]
                if len(self.text) == 0:
                    self.text = self.default_value

                self.change = True
            else:
                key = pygame.key.name(key)
                if len(self.availableSymbols) == 0:
                    return
                if self.availableSymbols.__contains__(key):
                    self.last_value = self.text
                    self.text += key
                    self.change = True

    def revert_press(self):
        self.text = self.last_value
        self.last_value = self.text

class Text:
    def __init__(self, pos, font_path, font_size, text="", color=WHITE):
        self.pos = pos
        self.font_path = font_path
        self.font_size = font_size
        self.text = text
        self.color = color

    def draw(self, surface):
        font = pygame.font.Font(self.font_path, self.font_size)
        text_surface = font.render(self.text, True, self.color)
        surface.blit(text_surface, self.pos)
