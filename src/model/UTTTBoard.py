# import Observer.py
import numpy as np
from enum import Enum


class Players(Enum):
    """
    Player Enum for cells and squares
    """
    NONE = '_'
    X = 'X'
    O = 'O'


class GameStatus(Enum):
    """
    Enum for overall game status
    """
    NOT_OVER = 0
    X_WIN = 1
    O_WIN = 2
    STALEMATE = 3


class ClaimStatus(Enum):
    """
    Cell claim status enum
    """
    NONE = 0
    X_CLAIM = 1
    O_CLAIM = 2


class TTTBoard:
    """
    Tic Tac Toe Board to be contained within a UTTT board square
    Cell Indices:
    [ 0, 1, 2]
    [ 3, 4, 5]
    [ 6, 7, 8]
    """

    def __init__(self):
        self.board = [Players.NONE] * 9
        self.status = ClaimStatus.NONE
        self.row_container = [0] * 3
        self.col_container = [0] * 3
        self.diag_container = 0
        self.odiag_container = 0

    def is_valid_move(self, cell):
        """
        If the square has not been claimed and the cell has not been claimed, return True. Else, False
        :param cell: Index of the cell in the square to check
        :return: True if valid move. False otherwise.
        """
        return self.status == ClaimStatus.NONE and self.board[cell] == Players.NONE

    def add_marker(self, player, cell):
        """
        Assuming a cell is valid to be placed in, change player ownership of cell, and
        check to see if square has been claimed
        :param player: Player making the move
        :param cell: index of the square to make move in
        :return: returns True, if Square is claimed after making move. Else False.
        """
        # Assuming move is valid, add marker and update containers
        self.board[cell] = player
        self.row_container[cell // 3] += 1
        self.col_container[cell % 3] += 1
        if cell % 4 == 0:
            self.diag_container += 1
        if cell % 2 == 0 and cell % 8 != 0:
            self.odiag_container += 1
        return self.check_claimed_cell(cell)

    def check_claimed_cell(self, cell):
        """
        Checks all possible ways for square to be claimed after making a move in the cell index
        :param cell: index of the move that was just made
        :return:true if square is claimed. False otherwise
        """
        # Updates claimed status after move is made
        board_claimed = False
        #Check rows
        if self.row_container[cell // 3] == 3:
            if self.check_players([3 * (cell // 3), 3 * (cell // 3) + 1, 3 * (cell // 3) + 2]):
                board_claimed = True
        #Check cols
        if not board_claimed and self.col_container[cell % 3] == 3:
            if self.check_players([cell % 3, (cell % 3) + 3, (cell % 3) + 6]):
                board_claimed = True
        #Check main diagonal
        if not board_claimed and self.diag_container == 3:
            if self.check_players([0, 4, 8]):
                board_claimed = True
        #Check opposite diagonal
        if not board_claimed and self.odiag_container == 3:
            if self.check_players([2, 4, 6]):
                board_claimed = True
        return board_claimed

    def check_players(self, cells):
        """
        Given an array of 3 players, if all of them are the same player, then update TTTBoard status to that Player
        :param cells: array of three Player Enum elems
        :return: True if board has been claimed
        """
        # If the 3 cells given have the same Player, then status is updated to that Player's win
        board_claimed = False
        if self.status == ClaimStatus.NONE and \
                self.board[cells[0]] == self.board[cells[1]] and \
                self.board[cells[1]] == self.board[cells[2]]:
            if self.board[cells[0]] == Players.X:
                self.status = ClaimStatus.X_CLAIM
            else:
                self.status = ClaimStatus.O_CLAIM
            board_claimed = True
        return board_claimed

    def get_claim_status(self):
        """
        Returns Games status
        """
        return self.status

    def get_cell_contents(self, cell):
        """
        Returns the player that occupies the given cell index
        :param cell: cell index
        :return:Player enum value for a given cell
        """
        return self.board[cell]


class UTTTBoard:
    """
    Ultimate Tic Tac Toe Board Model
    Has functionality to make moves, check if moves are valid, check game status, get contents of a square, restart game...
    Square Indices:         X WIN           O WIN
    [ 0, 1, 2]            [  \  / ]       [  ---- ]
    [ 3, 4, 5]            [   X   ]       [ |    |]
    [ 6, 7, 8]            [ /  \  ]       [ \___/ ]
    """

    def __init__(self):
        # Initiate Blank Board
        self.board = [TTTBoard() for _ in range(9)]
        self.status_board = TTTBoard()
        self.observers = []
        self.game_status = GameStatus.NOT_OVER

    def add_observer(self, observer):
        """
        Add observers to be notified when a change is made
        :param observer: object of the Observer class
        """
        # Add observers to list
        self.observers.append(observer)

    def notify_observers(self, string):
        """
        For all observers, send update on board state
        :param string: String that indicates information about move
        """
        # Update all observers
        for observer in self.observers:
            observer.update(self, string)

    def make_move(self, square, cell, player):
        """
        Given a square, cell, and player, attempt to add player marker to that square and cell combo
        :param square: the index of the square on the UTTTBoard
        :param cell:  the index of the cell on the TTTBoard
        :param player: the current player's Player Enum value
        :return: If game has been won, return true
        """
        # Add marker to the board
        game_win = False
        if self.is_valid_move(square, cell):
            if self.board[square].add_marker(player, cell):
                if self.status_board.add_marker(player, square):
                    if player == Players.X:
                        self.game_status = GameStatus.X_WIN
                    else:
                        self.game_status = GameStatus.O_WIN
                    #TODO: Add Stalemate condition check
                    game_win = True
            self.notify_observers(None)
        else:
            self.notify_observers("Invalid Move.")
        return game_win

    def is_valid_move(self, square, cell):
        """
        Checks if the given square and cells are valid and unclaimed
        :param square: the index of the square on the UTTTBoard
        :param cell:  the index of the cell on the TTTBoard
        :return: true, if a move can be made there. False, otherwise
        """
        if square < 0 or square > 8 or cell < 0 or cell > 8:
            return False
        else:
            return self.board[square].is_valid_move(cell)

    def get_content(self, square, cell):
        """
        Returns player enum value for a given square and cell combo
        :param square: the index of the square on the UTTTBoard
        :param cell:  the index of the cell on the TTTBoard
        :return: Player enum value
        """
        return self.board[square].board[cell]

    def __str__(self):
        ret = ""
        squares = \
            np.array([[[[i] * 3 for i in range(k, k + 3)] for _ in range(3)] for k in [0, 3, 6]]).reshape([1, 81])[0]
        cells = np.array([[0, 1, 2] * 3, [3, 4, 5] * 3, [6, 7, 8] * 3] * 3).flatten()
        for i in range(81):
            if i % 27 == 0 and i != 0: ret += "\n======================="
            if i % 9 == 0: ret += "\n"
            if i % 3 == 0 and i % 9 != 0: ret += "|| "
            ret += self.get_content(squares[i], cells[i]).value + ' '
        return ret
