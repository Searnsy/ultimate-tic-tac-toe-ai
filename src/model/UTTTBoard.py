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
        return self.status == ClaimStatus.NONE and self.board[cell] == Players.NONE

    def add_marker(self, player, cell):
        # Assuming move is valid, add marker and update containers
        self.board[cell] = player
        self.row_container[cell // 3] += 1
        self.col_container[cell % 3] += 1
        if cell % 4 == 0:
            self.diag_container += 1
        if cell % 2 == 0 and cell % 8 != 0:
            self.odiag_container += 1
        return self.check_claimed(cell)

    def check_claimed(self, cell):
        # Updates claimed status after move is made
        board_claimed = False
        if self.row_container[cell // 3] == 3:
            if self.check_players([3 * (cell // 3), 3 * (cell // 3) + 1, 3 * (cell // 3) + 2]):
                board_claimed = True
        if not board_claimed and self.col_container[cell % 3] == 3:
            if self.check_players([cell % 3, (cell % 3) + 3, (cell % 3) + 6]):
                board_claimed = True
        if not board_claimed and self.diag_container == 3:
            if self.check_players([2, 4, 6]):
                board_claimed = True
        if not board_claimed and self.odiag_container == 3:
            if self.check_players([0, 4, 8]):
                board_claimed = True
        return board_claimed

    def check_players(self, cells):
        # If the 3 cells given have the same Player, then status is updated to that Player's win
        board_claimed = False
        if self.status == ClaimStatus.NONE and \
                self.board[cells[0]] == self.board[cells[1]] and \
                self.board[cells[1]] == self.board[cells[2]]:
            self.status = self.board[cells[0]]
            board_claimed = True
        return board_claimed

    def get_cell_contents(self, cell: int) -> Players:
        return self.board[cell]


class UTTTBoard:
    """
    Ultimate Tic Tac Toe Board Model
    Has functionality to make moves, check if moves are valid, check game status, get contents of a square, restart game...
    """

    def __init__(self):
        # Initiate Blank Board
        self.board = [TTTBoard() for _ in range(9)]
        self.status_board = TTTBoard()
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
        game_win = False
        if self.is_valid_move(square, cell):
            if self.board[square].add_marker(player, cell):
                if self.status_board.add_marker(player, square):
                    if player == Players.X:
                        self.game_status = GameStatus.X_WIN
                    else:
                        self.game_status = GameStatus.O_WIN
                    game_win = True
        else:
            self.notify_observers("Invalid Move.")
        return game_win

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
