import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = WIDTH // 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_COLOR = (28, 170, 156)
O_COLOR = (242, 85, 96)

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
        self.reset_board()

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current = "X"

    def make_move(self, row, col):
        self.board[row][col] = self.current
        winner, _ = find_winner(self.board)

        if winner:
            self.show_message(f"Player {winner} wins!")
        elif is_full(self.board):
            self.show_message("Draw!")
        else:
            self.current = "O" if self.current == "X" else "X"

    def show_message(self, message):
        self.draw_board()
        self.draw_text(message, self.font_big, BLACK,
                       (WIDTH // 2, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        self.reset_board()

    def handle_click(self, pos):
        x, y = pos
        row, col = y // CELL, x // CELL
        if self.board[row][col] == "":
            self.make_move(row, col)

    @staticmethod
    def cell_center(row, col):
        return col * CELL + CELL // 2, row * CELL + CELL // 2

    def draw_text(self, text, font, color, center):
        surface = font.render(text, True, color)
        self.screen.blit(surface, surface.get_rect(center=center))

    def draw_board(self):
        self.screen.fill(WHITE)
        for i in range(1, 3):
            pygame.draw.line(self.screen, BLACK, (i * CELL, 0),
                             (i * CELL, HEIGHT), 5)
            pygame.draw.line(self.screen, BLACK,
                             (0, i * CELL), (WIDTH, i * CELL), 5)

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

    def draw(self):
        self.draw_board()
        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
