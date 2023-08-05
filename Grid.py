import pygame
from source import block_colours


class Grid:
    def __init__(self):
        self.row_amount = 20
        self.col_amount = 10
        self.one_square = 25
        self.grid = [[0 for _ in range(self.col_amount)] for _ in range(self.row_amount)]
        self.colours = block_colours

    def draw_grid(self):
        for row in range(self.row_amount):
            for column in range(self.col_amount):
                print(self.grid[row][column], end=" ")
            print()

    def is_in_frame(self, row, column):
        if 0 <= row < self.row_amount and 0 <= column < self.col_amount:
            return True
        return False

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def is_full(self, row):
        for column in range(self.col_amount):
            if self.grid[row][column] == 0:
                return False
        return True

    def erase_row(self, row):
        special_bricks = []
        slow_bricks = 0
        destruction_bricks = 0
        for column in range(self.col_amount):
            if self.grid[row][column] == 1:
                slow_bricks += 1
            elif self.grid[row][column] == 2:
                destruction_bricks += 1
            self.grid[row][column] = 0
        special_bricks.append(slow_bricks)
        special_bricks.append(destruction_bricks)
        return special_bricks

    def move_row_down(self, row, rows_num):
        for column in range(self.col_amount):
            self.grid[row + rows_num][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_row(self):
        erased_lines = slow_bricks = destruction_bricks = 0
        erase_res = []
        for row in range(self.row_amount - 1, 0, -1):
            if self.is_full(row):
                special_bricks = self.erase_row(row)
                destruction_bricks = special_bricks[0]
                slow_bricks = special_bricks[1]
                erased_lines += 1
            elif erased_lines > 0:
                self.move_row_down(row, erased_lines)
        erase_res.append(erased_lines)
        erase_res.append(slow_bricks)
        erase_res.append(destruction_bricks)
        return erase_res

    def reset(self):
        for row in range(self.row_amount):
            for column in range(self.col_amount):
                self.grid[row][column] = 0

    def draw(self, game_window, offset_x, offset_y):
        for row in range(self.row_amount):
            for column in range(self.col_amount):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column * self.one_square + offset_x, row * self.one_square + offset_y,
                                        self.one_square - 1, self.one_square - 1)
                pygame.draw.rect(game_window, self.colours[cell_value], cell_rect)
