# import Observer.py
import numpy as np
from enum import Enum


class Players(Enum):
    NONE = '_'
    X = 'X'
    O = 'O'


class GameStatus(Enum):
    NOT_OVER = 0
    X_WIN = 1
    O_WIN = 2
    STALEMATE = 3


class ClaimStatus(Enum):
    NONE = 0
    X_CLAIM = 1
    O_CLAIM = 2


class TTTBoard:
    """
    Tic Tac Toe Board to be contained within a UTTT board square
    """

    def __init__(self):
        self.board = [Players.NONE] * 9
        self.status = ClaimStatus.NONE
        self.row_container = [0] * 3
        self.col_container = [0] * 3
        self.diag_container = 0
        self.odiag_container = 0

    def is_valid_move(self, cell):
        if self.status == ClaimStatus.NONE:
            return self.board[cell] == Players.NONE
        else:
            return False

    def add_marker(self, player, cell):
        # Assuming move is valid, add marker and update containers
        self.board[cell] = player
        self.row_container[cell // 3] += 1
        self.col_container[cell % 3] += 1
        if cell % 4 == 0:
            self.diag_container += 1
        if cell % 2 == 0 and cell % 8 != 0:
            self.odiag_container += 1
        self.check_claimed(cell)

    def check_claimed(self, cell):
        # Updates claimed status after move is made
        if self.row_container[cell // 3] == 3:
            self.check_players([cell // 3, (cell // 3) + 1, (cell // 3) + 2])
        if self.col_container[cell % 3] == 3:
            self.check_players([cell % 3, (cell % 3) + 3, (cell % 3) + 3])
        if self.diag_container == 3:
            self.check_players([2, 4, 6])
        if self.odiag_container == 3:
            self.check_players([0, 4, 8])

    def check_players(self, cells):
        # If the 3 cells given have the same Player, then status is updated to that Player's win
        if self.status == ClaimStatus.NONE:  # Added in case multiple check_claimed ifs are triggered
            for i in range(3):
                if self.board[cells[i]] != self.board[cells[(i + 1) % 3]]:
                    return
            self.status = self.board[cells[0]]

    def get_cell_contents(self, cell: int) -> Players:
        return self.board[cell]


class UTTTBoard:
    """
    Ultimate Tic Tac Toe Board Model
    Has functionality to make moves, check if moves are valid, check game status, get contents of a square, restart game...
    """

    def __init__(self):
        # Initiate Blank Board
        self.board = []
        [self.board.append(TTTBoard()) for _ in range(9)]
        self.observers = []
        self.game_status = GameStatus.NOT_OVER

    def add_observer(self, observer):
        # Add observers to list
        self.observers.append(observer)

    def notify_observers(self, string):
        # Update all observers
        for observer in self.observers:
            observer.update(self, string)

    def make_move(self, square, cell, player):
        # Add marker to the board
        if self.is_valid_move(square, cell):
            self.board[square].board[cell] = player
        else:
            self.notify_observers("Invalid Move.")

    def is_valid_move(self, square, cell):
        if square < 0 or square > 8 or cell < 0 or cell > 9:
            return False
        else:
            return self.board[square].is_valid_move(cell)

    def get_content(self, square, cell):
        return self.board[square].board[cell]

    def __str__(self):
        ret = ""
        squares = \
        np.array([[[[i] * 3 for i in range(k, k + 3)] for _ in range(3)] for k in [0, 3, 6]]).reshape([1, 81])[0]
        cells = np.array([[0, 1, 2] * 3, [3, 4, 5] * 3, [6, 7, 8] * 3] * 3).flatten()
        for i in range(81):
            if i % 27 == 0 and i != 0: ret += "\n================================"
            if i % 9 == 0: ret += "\n"
            if i % 3 == 0 and i % 9 != 0: ret += "|| "
            ret += self.get_content(squares[i], cells[i]).value + '  '
        return ret
