import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (242, 85, 96)
X_COLOR = (28, 170, 156)
TEXT_COLOR = (0, 0, 0)

CELL_SIZE = WIDTH // 3

font = pygame.font.Font(None, 100)
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"


def draw_board():
    SCREEN.fill(WHITE)
    for col in range(1, 3):
        pygame.draw.line(SCREEN, LINE_COLOR, (col * CELL_SIZE,
                         0), (col * CELL_SIZE, HEIGHT), 5)
    for row in range(1, 3):
        pygame.draw.line(SCREEN, LINE_COLOR, (0, row * CELL_SIZE),
                         (WIDTH, row * CELL_SIZE), 5)


def draw_symbols():
    for row in range(3):
        for col in range(3):
            symbol = board[row][col]
            if symbol == "X":
                draw_x(col, row)
            elif symbol == "O":
                draw_o(col, row)


def draw_x(col, row):
    start_pos = (col * CELL_SIZE + 30, row * CELL_SIZE + 30)
    end_pos = ((col + 1) * CELL_SIZE - 30, (row + 1) * CELL_SIZE - 30)
    pygame.draw.line(SCREEN, X_COLOR, start_pos, end_pos, 15)
    pygame.draw.line(
        SCREEN, X_COLOR, (start_pos[0], end_pos[1]), (end_pos[0], start_pos[1]), 15)


def draw_o(col, row):
    pygame.draw.circle(SCREEN, CIRCLE_COLOR,
                       (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 90, 15)


def draw_message(message):
    text = font.render(message, True, TEXT_COLOR)
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() //
                2, HEIGHT // 2 - text.get_height() // 2))


def check_win(player):
    for row in range(3):
        if all([board[row][col] == player for col in range(3)]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False


def check_draw():
    return all([board[row][col] != "" for row in range(3) for col in range(3)])


def main():
    global current_player
    game_over = False
    draw_board()
    while True:
        draw_symbols()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = event.pos
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE

                if board[row][col] == "":
                    board[row][col] = current_player

                    if check_win(current_player):
                        draw_board()
                        draw_symbols()
                        draw_message(f"Player {current_player} wins!")
                        pygame.display.update()
                        pygame.time.delay(2000)
                        board[:] = [["" for _ in range(3)] for _ in range(3)]
                        draw_board()
                        current_player = "X"
                        continue

                    elif check_draw():
                        draw_board()
                        draw_symbols()
                        draw_message("Draw!")
                        pygame.display.update()
                        pygame.time.delay(2000)
                        board[:] = [["" for _ in range(3)] for _ in range(3)]
                        draw_board()
                        current_player = "X"
                        continue

                    current_player = "O" if current_player == "X" else "X"

        pygame.display.update()


main()
