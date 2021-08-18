import Observer.py
import numpy as np
from enum import Enum


class Players(Enum):
    NONE=0
    X=1
    O=2

class Game_Status(Enum):
    NOT_OVER=0
    X_WIN=1
    O_WIN=2
    STALEMATE=3

class Claim_Status(Enum):
    NONE=0
    X_CLAIM=1
    O_CLAIM=2


class TTT_Board:
    """
    Tic Tac Toe Board to be contained within a UTTT board square
    """
    def __init__(self):
        self.board=np.array([Players.NONE] *9)
        self.status = Claim_Status.NONE

    def Add_Marker(self,Player, cell):
        self.board[cell]=Player

    def Is_Claimed(self):
        return Claim_Status.NONE

    def Get_Cell_Contents(self, cell: int) -> Players:
        return self.board[cell]




class UTTT_Board:
    """
    Ultimate Tic Tac Toe Board Model
    Has functionality to make moves, check if moves are valid, check game status, get contents of a square, restart game...
    """

    def __init__(self):
        #Initate Blank Board
        self.board=[TTT_Board()] *9
        self.observers=[]
        self.game_status=Game_Status.NOT_OVER

    def Add_Observer(self,observer):
        #Add observers to list
        self.observers.append(observer)

    def Notify_Observers(self, string):
        #Update all observers
        for observer in self.observers:
            observer.update(self,string)

    def Make_Move(self, square, cell):
        # Add marker to the board
        if(self.Is_Valid_Move(square, cell)):
            return None
        else:
            self.Notify_Observers("Invalid Move.")

    def Is_Valid_Move(self, square, cell):
        if square<0 or square>8 or cell<0 or cell>9:
            return False
        else:
            sqr=self.board[square]
            return sqr.board[cell] ==Players.NONE

