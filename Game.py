from Grid import Grid
from Blocks import *
from source import *
from Record import Record
from datetime import datetime
import random, pygame


class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [SqBlock(), IBlock(), TBlock(), LLBlock(), LRBlock(), SRBlock(), SLBlock()]
        self.current_block = self.get_block()
        self.next_block = self.get_block()
        self.state = True
        self.score = 0
        self.fall_speed = 0.5
        self.fall_time = 0
        self.level = 1
        self.cur_record = Record()
        self.best_score = self.cur_record.get_best_score()
        self.slow_energy = 0
        self.is_slowing_down = False
        self.destruction_energy = 0

    def save_score(self):
        self.cur_record.insert_record(str(datetime.now()), self.score)
        self.best_score = self.cur_record.get_best_score()

    def get_block(self):
        self.blocks = [SqBlock(), IBlock(), TBlock(), LLBlock(), LRBlock(), SRBlock(), SLBlock()]
        return random.choice(self.blocks)

    def update_score(self, erase_res):
        if erase_res[0] == 0:
            self.score += 10
        else:
            self.score += erase_res[0] * 100
        if erase_res[1] != 0 and not self.is_slowing_down:
            self.slow_energy += erase_res[1] * 5
        if erase_res[2] != 0:
            self.destruction_energy += erase_res[2] * 5
        if self.score >= self.level * 1000:
            self.level += 1
            self.fall_speed = round(self.fall_speed - 0.1, 1)

    def stop_block(self):
        bricks = self.current_block.get_pos()
        for position in bricks:
            self.grid.grid[position.row][position.column] = self.current_block.sort
        self.current_block = self.next_block
        self.next_block = self.get_block()
        erase_res = self.grid.clear_full_row()
        self.update_score(erase_res)
        if not self.is_block_suitable():
            self.state = False

    def reset_game(self):
        self.grid.reset()
        self.slow_energy = 0
        self.destruction_energy = 0
        self.current_block = self.get_block()
        self.next_block = self.get_block()
        self.fall_speed = 0.5
        self.level = 1
        self.score = 0

    def speed_change(self, speed):
        self.fall_speed = speed

    def is_block_within(self):
        bricks = self.current_block.get_pos()
        for brick in bricks:
            if not self.grid.is_in_frame(brick.row, brick.column):
                return False
        return True

    def is_block_suitable(self):
        bricks = self.current_block.get_pos()
        for brick in bricks:
            if not self.grid.is_empty(brick.row, brick.column):
                return False
        return True

    def go_side(self, x1):
        self.current_block.move(0, x1)
        if (not self.is_block_within()) or (not self.is_block_suitable()):
            self.current_block.move(0, -x1)

    def go_down_fast(self):
        while self.is_block_within() and self.is_block_suitable():
            self.current_block.move(1, 0)
        self.current_block.move(-1, 0)

    def go_down(self):
        if self.fall_time / 1000 >= self.fall_speed:
            self.fall_time = 0
            self.current_block.move(1, 0)
            if (not self.is_block_within()) or (not self.is_block_suitable()):
                self.current_block.move(-1, 0)
                self.stop_block()

    def rotate(self):
        self.current_block.rotate_clockwise()
        if (not self.is_block_within()) or (not self.is_block_suitable()):
            self.current_block.rotate_anticlockwise()

    def game_over(self, game_window, window_x, window_y, text):
        game_window.fill(black)
        self.save_score()
        self.show_stats(game_window, white, get_font(50), window_x / 2, window_y / 4, "Your score is : ",
                        True, self.score)
        self.show_stats(game_window, white, get_font(25), window_x / 2, window_y / 4 + 100,
                        text, True)
        self.show_stats(game_window, white, get_font(25), window_x / 2, window_y / 4 + 200,
                        "Your best score is : ", True, self.best_score)
        pygame.display.update()

    @staticmethod
    def show_stats(game_window, colour, text_font, pos_x, pos_y, text, is_over=False, attrib=None):
        if attrib is None:
            text_surface = text_font.render(text, True, colour)
        else:
            text_surface = text_font.render(text + str(attrib), True, colour)
        if is_over:
            text_rect = text_surface.get_rect(midtop=(pos_x, pos_y))
        else:
            text_rect = text_surface.get_rect(topleft=(pos_x, pos_y))
        game_window.blit(text_surface, text_rect)

    def draw_grid(self, game_window, offset_x, offset_y, erase=False):
        self.grid.draw(game_window, offset_x, offset_y)
        if erase:
            self.current_block.draw(game_window, offset_x, offset_y, erase)
        else:
            self.current_block.draw(game_window, offset_x, offset_y)

        if self.next_block.sort == 1:
            self.next_block.draw(game_window, 665, 220)
        elif self.next_block.sort == 2:
            self.next_block.draw(game_window, 665, 230)
        else:
            self.next_block.draw(game_window, 675, 220)
