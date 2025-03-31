from minesweeper import Minesweeper, MinesweeperAI
import pygame
import sys


pygame.init()

IS_LEFT_CLICK = 1
IS_RIGHT_CLICK = 3
FPS = 60

PROBABILITY_MINE = 0.25
# Board dimensions (adjustable)
BOARD_WIDTH = 5  # Number of cells horizontally
BOARD_HEIGHT = 5  # Number of cells vertically
CELL_SIZE = 40  # Size of each cell in pixels

# Margins and offsets
LEFT_MARGIN = 50  # Space between the table and the left screen edge
TOP_MARGIN = 20  # Top margin for a consistent look
RIGHT_PANEL_X = LEFT_MARGIN + BOARD_WIDTH * CELL_SIZE + 50  # Offset from the board

# Screen dimensions (calculated to fit the table vertically)
SCREEN_WIDTH = BOARD_WIDTH * CELL_SIZE + LEFT_MARGIN + 250  # 200px for the right panel
SCREEN_HEIGHT = BOARD_HEIGHT * CELL_SIZE + TOP_MARGIN * 2

# Colors
BACKGROUND_COLOR = "black"
TILE_COLOR = "grey"
HIDDEN_TILE_COLOR = "dark cyan"
TABLE_BORDER_COLOR = "black"
AI_MOVE_FONT_COLOR = "cyan"
AI_MOVE_OUTLINE_COLOR = "cyan"
AI_MOVE_BUTTON_COLOR = "brown"
SCORE_FONT_COLOR = "violet"
WON = ("You won :)", "dark green")
LOST = ("You lose :(", "red")
TRIGGERED_MINE_COLOR = "red"
NUMBER_FONT_COLOR = "black"

FLAG_IMAGE = pygame.image.load("images/flag.png")
MINE_IMAGE = pygame.image.load("images/mine.png")
FLAG_IMAGE = pygame.transform.scale(FLAG_IMAGE, (CELL_SIZE - 4, CELL_SIZE - 4))
MINE_IMAGE = pygame.transform.scale(MINE_IMAGE, (CELL_SIZE - 4, CELL_SIZE - 4))

button_rect = pygame.Rect(RIGHT_PANEL_X, 50, 150, 50)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Minesweeper")

# Fonts
font = pygame.font.Font(None, 36)


def detonate(game: Minesweeper, cell: tuple[int, int]):
    x = LEFT_MARGIN + cell[1] * CELL_SIZE
    y = TOP_MARGIN + cell[0] * CELL_SIZE
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(TILE_COLOR)
        draw_numbers(game.board)
        draw_board(HIDDEN_TILE_COLOR, exclude=game.safes_found)
        pygame.draw.rect(screen, TRIGGERED_MINE_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, TABLE_BORDER_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)
        draw_mines(game.mines)
        draw_flags(game.mines_found)
        draw_right_panel(game.score)
        display_game_status(LOST)
        pygame.display.flip()


def display_game_status(status: tuple[str, str]):
    """Displays the game status (e.g., "You won" or "You lose") below the score text in the right panel."""
    status_surface = font.render(status[0], True, status[1])

    status_x = LEFT_MARGIN + BOARD_WIDTH * CELL_SIZE + 50
    status_y = (120 + SCREEN_HEIGHT) // 2  # Adjust based on your UI layout (score text is at 120+)

    screen.blit(status_surface, (status_x, status_y))


def draw_board(box_color, exclude: set[tuple[int, int]] | None = None):
    """Draw the Minesweeper board with a left margin."""
    if exclude is None:
        exclude = set()

    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if (row, col) in exclude:
                continue
            x = LEFT_MARGIN + col * CELL_SIZE
            y = TOP_MARGIN + row * CELL_SIZE
            pygame.draw.rect(screen, box_color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, TABLE_BORDER_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)


def draw_flags(flags: set[tuple[int, int]]):
    for flag in flags:
        draw_image(FLAG_IMAGE, flag)


def draw_image(image, cell):
    """Draws an image in the specified cell on the board."""
    row, col = cell

    # Calculate cell position
    x = LEFT_MARGIN + col * CELL_SIZE
    y = TOP_MARGIN + row * CELL_SIZE

    # Calculate centered position for the image
    img_x = x + (CELL_SIZE - image.get_width()) // 2
    img_y = y + (CELL_SIZE - image.get_height()) // 2

    screen.blit(image, (img_x, img_y))


def draw_mines(mines: set[tuple[int, int]]) -> None:
    for mine in mines:
        draw_image(MINE_IMAGE, mine)


def draw_numbers(board: list[list[int]]):
    """Draws numbers in the center of each cell based on the given board."""
    for row in range(len(board)):
        for col in range(len(board[row])):
            # Calculate cell position
            x = LEFT_MARGIN + col * CELL_SIZE
            y = TOP_MARGIN + row * CELL_SIZE

            # Get the number to display
            number = board[row][col]

            if number != 0 or True:
                # Render the number text
                number_text = font.render(str(number), True, NUMBER_FONT_COLOR)

                # Calculate position to center the text in the cell
                text_rect = number_text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))

                # Draw the text
                screen.blit(number_text, text_rect)


def draw_right_panel(score: int | float):
    """Draw the right panel with the AI Move button and score."""

    # Draw AI Move button
    pygame.draw.rect(screen, AI_MOVE_BUTTON_COLOR, button_rect)
    pygame.draw.rect(screen, AI_MOVE_OUTLINE_COLOR, button_rect, 2)
    button_text = font.render("AI Move", True, AI_MOVE_FONT_COLOR)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    # Draw Score
    score_text = font.render(f"Score = {score}", True, SCORE_FONT_COLOR)
    score_rect = score_text.get_rect(topleft=(RIGHT_PANEL_X, 120))
    screen.blit(score_text, score_rect)


def ensure_coordinate(cell: tuple[int, int]) -> bool:
    return 0 <= cell[0] < BOARD_HEIGHT and 0 <= cell[1] < BOARD_WIDTH


def get_coordinate() -> tuple[int, int]:
    x, y = pygame.mouse.get_pos()
    x, y = y, x
    i, j = (x - TOP_MARGIN), (y - LEFT_MARGIN)
    return i // CELL_SIZE, j // CELL_SIZE


def victory(game: Minesweeper) -> None:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(TILE_COLOR)
        draw_numbers(game.board)
        draw_board(HIDDEN_TILE_COLOR, exclude=game.safes_found)
        draw_flags(game.mines_found)
        draw_right_panel(game.score)
        display_game_status(WON)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    game = Minesweeper(BOARD_HEIGHT, BOARD_WIDTH, PROBABILITY_MINE)
    agent = MinesweeperAI(BOARD_HEIGHT, BOARD_WIDTH)

    while not game.won():
        for event in pygame.event.get():
            ai_move_button_clicked = event.type == pygame.MOUSEBUTTONUP \
                                     and button_rect.collidepoint(pygame.mouse.get_pos())
            is_left_click = event.type == pygame.MOUSEBUTTONUP and event.button == IS_LEFT_CLICK
            is_right_click = event.type == pygame.MOUSEBUTTONUP and event.button == IS_RIGHT_CLICK
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ai_move_button_clicked:
                mines, safes = agent.make_move()
                for mine in mines:
                    game.flagging(mine, Minesweeper.BOT)
                    agent.mark_mine(mine)
                for safe in safes:
                    game.mark_safe(safe, Minesweeper.BOT)
                    agent.mark_safe(safe)
                    agent.add_knowledge(game.get_neighbors(safe), game.get_count(safe))
            elif is_left_click and not game.is_flagged(cell := get_coordinate()) and ensure_coordinate(cell):
                if game.is_mine(cell):
                    detonate(game, cell)
                game.mark_safe(cell)
                agent.mark_safe(cell)
                agent.add_knowledge(game.get_neighbors(cell), game.get_count(cell))
            elif is_right_click:
                game.flagging(get_coordinate())

        screen.fill(BACKGROUND_COLOR)
        draw_board(TILE_COLOR)
        draw_numbers(game.board)
        draw_board(HIDDEN_TILE_COLOR, exclude=game.safes_found)
        draw_flags(game.mines_found)
        draw_right_panel(game.score)

        pygame.display.flip()
        clock.tick(FPS)

    victory(game)


if __name__ == "__main__":
    main()
