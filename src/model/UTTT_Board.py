# import Observer.py
import numpy as np
from enum import Enum


class Players(Enum):
    NONE='_'
    X='X'
    O='O'

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
        self.RowContainer=[0]*3
        self.ColContainer = [0] * 3
        self.DiagContainer = 0
        self.ODiagContainer = 0

    def Is_Valid_Move(self,cell):
        if self.status==Claim_Status.NONE:
            return self.board[cell] == Players.NONE
        else:
            return False

    def Add_Marker(self,Player, cell):
        #Assuming move is valid, add marker and update containers
        self.board[cell]=Player
        self.RowContainer[cell // 3]+=1
        self.ColContainer[cell % 3]+=1
        if cell%4==0:
            self.DiagContainer+=1
        if cell%2==0 and cell%8!=0 :
            self.ODiagContainer += 1
        self.Check_Claimed(cell)

    def Check_Claimed(self,cell):
        #Updates claimed status after move is made
        if self.RowContainer[cell//3]==3:
            self.Check_Players([cell//3, (cell//3) +1, (cell//3)+2])
        if self.ColContainer[cell%3]==3:
            self.Check_Players([cell % 3, (cell % 3) + 3, (cell % 3) + 3])
        if self.DiagContainer==3:
            self.Check_Players([2,4,6])
        if self.ODiagContainer==3:
            self.Check_Players([0,4,8])

    def Check_Players(self,cells):
        #If the 3 cells given have the same Player, then status is updated to that Player's win
        if self.status == Claim_Status.NONE: # Added in case multiple Check_Claimed ifs are triggered
            for i in range(3):
                if self.board[cells[i]] != self.board[cells[(i+1) %3]]:
                    return
            self.status=self.board[cells[0]]

    def Get_Cell_Contents(self, cell: int) -> Players:
        return self.board[cell]




class UTTT_Board:
    """
    Ultimate Tic Tac Toe Board Model
    Has functionality to make moves, check if moves are valid, check game status, get contents of a square, restart game...
    """
    def __init__(self):
        #Initate Blank Board
        self.board=[]
        [self.board.append(TTT_Board()) for i in range(9)]
        # self.board=[TTT_Board()] *9
        self.observers=[]
        self.game_status=Game_Status.NOT_OVER

    def Add_Observer(self,observer):
        #Add observers to list
        self.observers.append(observer)

    def Notify_Observers(self, string):
        #Update all observers
        for observer in self.observers:
            observer.update(self,string)

    def Make_Move(self, square, cell, player):
        # Add marker to the board
        if self.Is_Valid_Move(square, cell):
            self.board[square].board[cell] = player
        else:
            self.Notify_Observers("Invalid Move.")

    def Is_Valid_Move(self, square, cell):
        if square<0 or square>8 or cell<0 or cell>9:
            return False
        else:
            return self.board[square].Is_Valid_Move(cell)

    def Get_Content(self,square, cell):
        return self.board[square].board[cell]

    def To_String(self):
        squares = np.array([[[[i]*3 for i in range(k,k+3)] for j in range(3)] for k in[0,3,6]]).reshape([1,81])[0]
        cells = np.array([[0,1,2]*3,[3,4,5]*3,[6,7,8]*3]*3).flatten()
        for i in range(81):
            if i % 27 == 0 and i!=0: print("\n================================",end='')
            if i % 9 == 0: print()
            if i % 3 ==0 and i%9 !=0: print("|| ",end='')
            print(self.Get_Content(squares[i],cells[i]).value,' ', end='')

