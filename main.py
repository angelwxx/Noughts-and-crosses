import sys
import pygame

pygame.init()

BOARD_SIZE = 600
BAR_HEIGHT = 100
WIDTH, HEIGHT = BOARD_SIZE, BOARD_SIZE + BAR_HEIGHT
CELL = BOARD_SIZE // 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (235, 235, 235)
DARK_GRAY = (120, 120, 120)
X_COLOR = (28, 170, 156)
O_COLOR = (242, 85, 96)
WIN_LINE_COLOR = (255, 190, 0)

PLAYING, ROUND_OVER = "playing", "round_over"

LINES = (
    [[(r, c) for c in range(3)] for r in range(3)]
    + [[(r, c) for r in range(3)] for c in range(3)]
    + [[(i, i) for i in range(3)], [(i, 2 - i) for i in range(3)]]
)


def find_winner(board):
    for line in LINES:
        (r1, c1), (r2, c2), (r3, c3) = line
        value = board[r1][c1]
        if value and value == board[r2][c2] == board[r3][c3]:
            return value, line
    return None, None


def is_full(board):
    return all(cell != "" for row in board for cell in row)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Noughts and Crosses")
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.Font(None, 90)
        self.font_mid = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 28)

        self.state = PLAYING
        self.scores = {"X": 0, "O": 0, "Draw": 0}
        self.reset_board()

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current = "X"
        self.winner = None
        self.win_line = None

    def reset_scores(self):
        self.scores = {"X": 0, "O": 0, "Draw": 0}

    def make_move(self, row, col):
        self.board[row][col] = self.current
        winner, line = find_winner(self.board)

        if winner:
            self.winner = winner
            self.win_line = line
            self.scores[winner] += 1
            self.state = ROUND_OVER
        elif is_full(self.board):
            self.scores["Draw"] += 1
            self.state = ROUND_OVER
        else:
            self.current = "O" if self.current == "X" else "X"

    def handle_click(self, pos):
        x, y = pos

        if self.state == ROUND_OVER:
            self.reset_board()
            self.state = PLAYING
            return

        if self.state == PLAYING and y >= BAR_HEIGHT:
            row, col = (y - BAR_HEIGHT) // CELL, x // CELL
            if self.board[row][col] == "":
                self.make_move(row, col)

    def handle_key(self, key):
        if key == pygame.K_r:
            self.reset_scores()
            self.reset_board()
            self.state = PLAYING

    def cell_center(self, row, col):
        return col * CELL + CELL // 2, BAR_HEIGHT + row * CELL + CELL // 2

    def draw_text(self, text, font, color, center):
        surface = font.render(text, True, color)
        self.screen.blit(surface, surface.get_rect(center=center))

    def draw_score_bar(self):
        pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, BAR_HEIGHT))
        self.draw_text(f"X: {self.scores['X']}",
                       self.font_mid, X_COLOR, (110, 38))
        self.draw_text(
            f"Draws: {self.scores['Draw']}", self.font_mid, DARK_GRAY, (WIDTH // 2, 38))
        self.draw_text(f"O: {self.scores['O']}",
                       self.font_mid, O_COLOR, (WIDTH - 110, 38))

        if self.state == PLAYING:
            hint = f"Turn: {self.current}   |   R - reset score"
        else:
            hint = "R - reset score"
        self.draw_text(hint, self.font_small, DARK_GRAY, (WIDTH // 2, 78))

    def draw_board(self):
        self.screen.fill(WHITE)
        for i in range(1, 3):
            pygame.draw.line(self.screen, BLACK, (i * CELL,
                             BAR_HEIGHT), (i * CELL, HEIGHT), 5)
            pygame.draw.line(
                self.screen, BLACK, (0, BAR_HEIGHT + i *
                                     CELL), (WIDTH, BAR_HEIGHT + i * CELL), 5
            )

        for row in range(3):
            for col in range(3):
                cx, cy = self.cell_center(row, col)
                if self.board[row][col] == "X":
                    offset = CELL // 2 - 30
                    pygame.draw.line(
                        self.screen, X_COLOR, (cx - offset, cy - offset), (cx + offset, cy + offset), 15)
                    pygame.draw.line(
                        self.screen, X_COLOR, (cx - offset, cy + offset), (cx + offset, cy - offset), 15)
                elif self.board[row][col] == "O":
                    pygame.draw.circle(self.screen, O_COLOR, (cx, cy), 70, 15)

        if self.win_line:
            start_row, start_col = self.win_line[0]
            end_row, end_col = self.win_line[2]
            start = self.cell_center(start_row, start_col)
            end = self.cell_center(end_row, end_col)
            pygame.draw.line(self.screen, WIN_LINE_COLOR, start, end, 10)

        self.draw_score_bar()

    def draw_round_over(self):
        overlay = pygame.Surface((WIDTH, 160), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 225))
        top = BAR_HEIGHT + (BOARD_SIZE - 160) // 2
        self.screen.blit(overlay, (0, top))

        message = f"Player {self.winner} wins!" if self.winner else "Draw!"
        self.draw_text(message, self.font_big, BLACK, (WIDTH // 2, top + 55))
        self.draw_text("Click to play again", self.font_small,
                       DARK_GRAY, (WIDTH // 2, top + 115))

    def draw(self):
        self.draw_board()
        if self.state == ROUND_OVER:
            self.draw_round_over()
        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
                if event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
