import pygame


def get_font(size):
    return pygame.font.Font("src/pixel_font.ttf", size)


block_colours = [
    (255, 255, 255),
    (255, 213, 0),  # yellow
    (64, 224, 208),  # cyan
    (148, 0, 211),  # purple
    (3, 65, 174),  # blue
    (255, 151, 28),  # orange
    (114, 203, 59),  # green
    (255, 50, 19),  # red
]

black = (0, 0, 0)
white = (255, 255, 255)
green = (114, 203, 59)
purple = (207, 159, 255)
grey = (128, 128, 128)
blue = (173, 216, 230)
dark_blue = (19, 30, 58)

background = pygame.image.load("src/bg9.jpg")
background_play = pygame.image.load("src/bg3.jpg")
background_instr = pygame.image.load("src/bg11.jpg")
clock_icon = pygame.image.load("src/clock.png")
frame_icon = pygame.image.load("src/frame.png")
bomb_icon = pygame.image.load("src/bomb.png")
pause_icon = pygame.image.load("src/pause.png")
tetris_logo = pygame.image.load("src/tetris_logo.png")
button_icon = pygame.image.load("src/button.png")
keyboard_icon = pygame.image.load("src/keyboard.jpg")
