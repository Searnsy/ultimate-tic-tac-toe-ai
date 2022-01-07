from src.model.Observer import *
from src.model.UTTTBoard import *
import random

class UTTTptui(Observer):
    def __init__(self):
        self.square = -1
        self.model = UTTTBoard()
        self.message = ""
        self.curr_player = Players.X
        self.initialize_view()

    """ ********* View Section ********* """
    def initialize_view(self):
        self.model.add_observer(self)

    def update(self, subject, client_data):
        print(self.model)
        print("Status: " + self.model.game_status.name)
        self.message = client_data

    """ ********* Controller Section ********* """
    def run(self):
        print("Welcome to Ultimate Tic Tac Toe!")
        self.update(self.model, None)
        while self.model.game_status == GameStatus.NOT_OVER:
            if self.curr_player == Players.X:
                self.HumanInput()
            else:
                self.RandomInput()
            # Switch Player
            if self.curr_player == Players.X:
                self.curr_player = Players.O
            else:
                self.curr_player = Players.X

        self.update(self.model, None)

    def HumanInput(self):
        """
        Allow Human to input their move
        """
        # Continue based off if next square is claimed
        while True:
            if 0 <= self.square < 9 and self.model.board[self.square].get_claim_status() is ClaimStatus.NONE:
                print("Player " + self.curr_player.value + " place your next marker in square " + str(self.square))
            else:
                self.square = int(input("Player " + self.curr_player.value + ", enter the square to add your marker: "))
            cell = int(input("Enter the cell to add your marker: "))
            self.model.make_move(self.square, cell, self.curr_player)
            if self.message != "Invalid Move.":
                break
            else:
                print(self.message)
        self.square = cell

    def RandomInput(self):
        """
        AI randomly selects available move
        """
        while True:
            if 0 <= self.square < 9 and self.model.board[self.square].get_claim_status() is ClaimStatus.NONE:
                pass
            else:
                #Select Square to place marker
                squares=[]
                [ squares.append(x) for x in range(0,9) if self.model.board[x].get_claim_status()==ClaimStatus.NONE]
                self.square = random.choice(squares)
            #Select Cell to place marker
            cells =[]
            [ cells.append(x) for x in range(0,9) if self.model.board[self.square].board[x]==Players.NONE ]
            cell=random.choice(cells)
            print("Player {} placed their marker in square {} and cell {}\n".format(self.curr_player.value, self.square, cell))
            self.model.make_move(self.square, cell, self.curr_player)
            if self.message != "Invalid Move.":
                break
            else:
                print(self.message)
        self.square = cell

if __name__ == '__main__':
    ptui = UTTTptui()
    ptui.run()
