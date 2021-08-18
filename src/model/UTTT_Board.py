import numpy as np
import Observer
from enum import Enum


class Players(Enum):
    NONE=0
    X=1
    O=2

class Game_Status(Enum):
    NOT_OVER=0
    X_WIN=1
    0_WIN=2
    STALEMATE=3


class TTT_Board:
    """
    Tic Tac Toe Board to be contained within a UTTT board square
    """


    def __init__(self):
        self.board=np.array([Players.NONE] *9)


class UTTT_Board:
    """
    Ultimate Tic Tac Toe Board Model
    Has functionality to make moves, check if moves are valid, check game status, get contents of a square, restart game...
    """

    def __init__(self):
        #Initate Blank Board
        self.board=[[TTT_Board] *9]
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
        return True

