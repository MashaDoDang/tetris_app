import random, pygame
from source import block_colours


class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Block:
    def __init__(self, sort):
        self.sort = sort
        self.cells = {}
        self.one_square = 25
        self.row_offset = 0
        self.column_offset = 0
        self.colour = random.randint(1, len(block_colours) - 1)
        self.rotation = 0

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_pos(self):
        bricks = self.cells[self.rotation]
        moved_bricks = []
        for position in bricks:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_bricks.append(position)
        return moved_bricks

    def rotate_clockwise(self):
        self.rotation += 1
        if self.rotation == len(self.cells):
            self.rotation = 0

    def rotate_anticlockwise(self):
        self.rotation -= 1
        if self.rotation == -1:
            self.rotation = len(self.cells) - 1

    def draw(self, game_window, offset_x, offset_y, erase=False):
        bricks = self.get_pos()
        for brick in bricks:
            brick_rect = pygame.Rect(offset_x + brick.column * self.one_square,
                                     offset_y + brick.row * self.one_square, self.one_square - 1, self.one_square - 1)
            if erase:
                pygame.draw.rect(game_window, block_colours[0], brick_rect)
            else:
                pygame.draw.rect(game_window, block_colours[self.sort], brick_rect)
