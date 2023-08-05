import sys, time
from Game import *
from Block import block_colours
from Button import Button, EnergyBar

window_x = 960
window_y = 540

pygame.init()

pygame.display.set_caption('Tetris')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()
tetris = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

is_paused = False


def play():
    global is_paused
    time_before = prev_speed = 0
    destruction_stop = False
    next_rect = pygame.Rect(window_x - 245, 175, 150, 150)

    slow_bar = EnergyBar(105, 200, 190, 40, 20)
    destruction_bar = EnergyBar(105, 290, 190, 40, 20)

    slow_down_time = 30

    while True:
        mouse_pos = pygame.mouse.get_pos()
        game_window.fill(black)
        game_window.blit(background_play, (0, 0))
        game_window.blit(frame_icon, (0, 150))
        game_window.blit(clock_icon, (50, 197))
        game_window.blit(bomb_icon, (50, 280))

        slow_bar.power = tetris.slow_energy
        destruction_bar.power = tetris.destruction_energy

        if tetris.slow_energy > 20:
            slow_bar.power = 20
        if tetris.destruction_energy > 20:
            destruction_bar.power = 20

        play_to_menu = Button(window_x // 10, window_y - 30, "Back to menu", None, get_font(25), white, purple)
        play_to_menu.hover(mouse_pos)
        play_to_menu.update(game_window)

        current_time = time.time()

        if tetris.slow_energy >= 20:
            if not tetris.is_slowing_down:
                time_before = time.time()
                prev_speed = tetris.fall_speed
                tetris.is_slowing_down = True
            if current_time - time_before >= slow_down_time:
                tetris.speed_change(prev_speed)
                tetris.slow_energy = 0
                tetris.is_slowing_down = False
            else:
                tetris.speed_change(0.7)

        pygame.draw.rect(game_window, white, next_rect, 0, 10)

        slow_bar.draw(game_window, block_colours[1])
        destruction_bar.draw(game_window, block_colours[2])

        tetris.fall_time += fps.get_rawtime()
        fps.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tetris.game_over(game_window, window_x, window_y, "The window will be closed automatically")
                time.sleep(2)
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and tetris.state:
                    tetris.rotate()
                if event.key == pygame.K_DOWN and tetris.state:
                    tetris.go_down_fast()
                if event.key == pygame.K_LEFT and tetris.state:
                    tetris.go_side(-1)
                if event.key == pygame.K_RIGHT and tetris.state:
                    tetris.go_side(1)
                if event.key == pygame.K_SPACE and tetris.state:
                    is_paused = True
                    pause()
                if event.key == pygame.K_ESCAPE:
                    tetris.state = True
                    tetris.reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_to_menu.check_action(mouse_pos):
                    tetris.game_over(game_window, window_x, window_y, "Going to the menu")
                    time.sleep(2)
                    tetris.reset_game()
                    main_menu()

            if event.type == GAME_UPDATE and tetris.state and not is_paused:
                tetris.go_down()

        tetris.show_stats(game_window, white, get_font(25), 5, 5, "Score : ", False, tetris.score)
        tetris.show_stats(game_window, white, get_font(25), 5, 40, "Level : ", False, tetris.level)
        tetris.show_stats(game_window, white, get_font(25), window_x - 300, 5, "Best score : ", False,
                          tetris.best_score)
        tetris.show_stats(game_window, white, get_font(25), 5, 80, "Cur speed : ", False, tetris.fall_speed)
        tetris.show_stats(game_window, white, get_font(25), 85, 135, " Power stats ", False)

        tetris.show_stats(game_window, white, get_font(25), window_x - 200, 135, "Next", False)

        if tetris.destruction_energy >= 20:
            destruction_stop = True
            tetris.destruction_energy = 0
            tetris.draw_grid(game_window, window_x // 3 + 50, window_y // 50, True)
            tetris.current_block = tetris.next_block
            tetris.next_block = tetris.get_block()
            time.sleep(1)
        else:
            tetris.draw_grid(game_window, window_x // 3 + 50, window_y // 50)
            if destruction_stop:
                destruction_stop = False
                time.sleep(1)

        if not tetris.state:
            time.sleep(0.7)
            tetris.game_over(game_window, window_x, window_y, "Press ESC to restart")

        pygame.display.update()


def pause():
    global is_paused
    while is_paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tetris.game_over(game_window, window_x, window_y, "This window will be closed automatically")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and tetris.state:
                    is_paused = False

            game_window.blit(background, (0, 0))
            game_window.blit(pause_icon, (window_x / 2 - 200, window_y / 4))

            tetris.show_stats(game_window, white, get_font(30), window_x / 2, window_y / 4 + 150,
                              "Press SPACE to resume", True)
            pygame.display.update()
            fps.tick(60)


def instructions():
    while True:
        game_window.fill(black)
        game_window.blit(background_instr, (0, 0))
        tetris.show_stats(game_window, white, get_font(50), window_x / 2, window_y / 10 - 25, "Instructions",
                          True)
        instr_to_menu = Button(window_x // 10 + 10, window_y - 30, "Back to menu", None, get_font(25), white, purple)
        mouse_pos = pygame.mouse.get_pos()
        instr_to_menu.hover(mouse_pos)
        instr_to_menu.update(game_window)
        game_window.blit(keyboard_icon, (70, 100))
        tetris.show_stats(game_window, white, get_font(20), window_x // 2, window_y - 165,
                          "When the yellow blocks are destroyed, "
                          "it saves energy to slow down following blocks", True)
        tetris.show_stats(game_window, white, get_font(20), window_x // 2, window_y - 140,
                          "for 30s", True)
        tetris.show_stats(game_window, white, get_font(20), window_x // 2, window_y - 110,
                          "When the blue blocks are destroyed, it saves energy to destroy current block", True)
        tetris.show_stats(game_window, white, get_font(20), window_x // 2, window_y - 80,
                          "and go to the next", True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if instr_to_menu.check_action(mouse_pos):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        game_window.blit(background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        game_window.blit(tetris_logo, (window_x / 10, window_y / 5 - 50))

        menu_to_game = Button(window_x / 10 + 173, window_y / 5 + 150, "Play", None, get_font(45), dark_blue, white)
        menu_to_instruc = Button(window_x / 10 + 173, window_y / 5 + 250, "Instruction", None, get_font(45),
                                 dark_blue, white)
        menu_quit = Button(window_x / 10 + 173, window_y / 5 + 350, "Quit", None, get_font(45), dark_blue, white)

        game_window.blit(button_icon, (window_x / 10 - 5, window_y / 5 + 100))
        game_window.blit(button_icon, (window_x / 10 - 5, window_y / 5 + 200))
        game_window.blit(button_icon, (window_x / 10 - 5, window_y / 5 + 300))

        for button in [menu_to_game, menu_to_instruc, menu_quit]:
            button.hover(mouse_pos)
            button.update(game_window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_to_game.check_action(mouse_pos):
                    play()
                if menu_to_instruc.check_action(mouse_pos):
                    instructions()
                if menu_quit.check_action(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
