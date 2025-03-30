import random
from itertools import combinations
from knowledge import *


MINE = -1


class Minesweeper:
    BOT = "bot"
    HUMAN = "human"

    def __init__(self, height: int, width: int, probability_mine: int | float = 0.25):
        assert height > 0 and width > 0 and 0 <= probability_mine <= 1
        self.height: int = height
        self.width: int = width
        self.probability_mine: int | float = probability_mine
        self.board: list[list[int]] = self.setup_board()
        self.score: int | float = 0
        self.mines: set[tuple[int, int]] = self.__get_mines()
        self.safes: set[tuple[int, int]] = self.__get_safes()
        self.mines_found: set[tuple[int, int]] = set()
        self.safes_found: set[tuple[int, int]] = set()

    def __get_mines(self) -> set[tuple[int, int]]:
        return {
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if self.is_mine((i, j))
        }

    def __get_safes(self) -> set[tuple[int, int]]:
        return {
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if self.is_safe((i, j))
        }

    def flagging(self, cell: tuple[int, int], player: str = HUMAN) -> None:
        if player == Minesweeper.BOT:
            self.mines_found.add(cell)
            return

        if not self.is_within_board(cell) or cell in self.safes_found:
            return

        if cell in self.mines_found:
            self.mines_found.remove(cell)
        else:
            self.mines_found.add(cell)

    def get_count(self, cell: tuple[int, int]) -> int:
        return self.board[cell[0]][cell[1]]

    def get_neighbors(self, cell: tuple[int, int]) -> set[tuple[int, int]]:
        return {
            (i, j)
            for i in range(cell[0] - 1, cell[0] + 2)
            for j in range(cell[1] - 1, cell[1] + 2)
            if self.is_within_board((i, j)) and (i, j) != cell
        }

    def is_flagged(self, cell: tuple[int, int]) -> bool:
        return cell in self.mines_found

    def is_mine(self, cell) -> bool:
        return self.is_within_board(cell) and self.board[cell[0]][cell[1]] == MINE

    def is_safe(self, cell) -> bool:
        return self.is_within_board(cell) and self.board[cell[0]][cell[1]] != MINE

    def is_within_board(self, cell: tuple[int, int]) -> bool:
        return 0 <= cell[0] < self.height and 0 <= cell[1] < self.width

    def mark_safe(self, cell: tuple[int, int], player: str = HUMAN) -> None:
        if player == Minesweeper.BOT and cell in self.mines_found:
            self.flagging(cell)
        if not self.is_within_board(cell) or cell in self.mines_found:
            return
        self.safes_found.add(cell)

    def setup_board(self) -> list[list[int]]:
        board = [
            random.choices([MINE, 0], [self.probability_mine, 1 - self.probability_mine], k=self.width)
            for _ in range(self.height)
        ]

        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == MINE:
                    continue
                board[i][j] = sum(1 for ni, nj in self.get_neighbors((i, j)) if board[ni][nj] == MINE)

        return board

    def won(self) -> bool:
        return self.mines_found == self.mines and self.safes_found == self.safes


class MinesweeperAI:
    def __init__(self, height: int, width: int):
        assert height > 0 and width > 0
        self.height = height
        self.width = width
        self.knowledge: Connective = And()
        self.discovered: dict[Proposition, bool] = {}

    def make_move(self) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
        mines = set()
        safes = set()
        print(self.knowledge)
        for i in range(self.height):
            for j in range(self.width):
                mine = Proposition((i, j))
                if self.knowledge.entails(mine, self.discovered):
                    print(f"{i, j} is a mine")
                    mines.add((i, j))
                elif self.knowledge.entails(Not(mine), self.discovered):
                    print(f"{i, j} is a safe")
                    safes.add((i, j))

        return mines, safes

    def mark_mine(self, cell: tuple[int, int]) -> None:
        mine = Proposition(cell)
        self.knowledge.add(mine)
        self.discovered[mine] = True

    def mark_safe(self, cell: tuple[int, int]) -> None:
        mine = Proposition(cell)
        self.knowledge.add(Not(mine))
        self.discovered[mine] = False

    def add_knowledge(self, cells: set[tuple[int, int]], count: int) -> None:
        cells: set[Proposition] = {Proposition(cell) for cell in cells}
        mines_or_safes = Or()
        for combination in combinations(cells, count):
            either_mines_or_safes = And()
            for cell in combination:
                either_mines_or_safes.add(cell)

            for cell in cells:
                if cell not in combination:
                    either_mines_or_safes.add(Not(cell))

            mines_or_safes.add(either_mines_or_safes)

        self.knowledge.add(mines_or_safes)


if __name__ == "__main__":
    from numpy import array
    game = Minesweeper(4, 8)
    print(array(game.board))
