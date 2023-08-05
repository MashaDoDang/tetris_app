import pygame
from source import block_colours


class Button:
    def __init__(self, x_pos, y_pos, button_text, image, button_font, base_colour, hover_colour):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.button_text = button_text
        self.image = image
        self.button_font = button_font
        self.text = self.button_font.render(self.button_text, True, base_colour)
        if self.image is None:
            self.image = self.text
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.base_colour = base_colour
        self.hover_colour = hover_colour

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_action(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def hover(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.button_font.render(self.button_text, True, self.hover_colour)
        else:
            self.text = self.button_font.render(self.button_text, True, self.base_colour)


class EnergyBar:
    def __init__(self, x, y, w, h, max_power):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.power = max_power
        self.max_power = max_power

    def draw(self, surface, power_colour):
        ratio = self.power / self.max_power
        pygame.draw.rect(surface, block_colours[7], (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, power_colour, (self.x, self.y, self.w * ratio, self.h))
