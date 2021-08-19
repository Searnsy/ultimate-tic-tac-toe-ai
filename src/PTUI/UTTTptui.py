import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Users/keege/OneDrive/Documents/GitHub/ultimate-tic-tac-toe-ai/src/model/') # TODO: How to grab locally???
from Observer import *
from UTTTBoard import *

class UTTTptui(Observer):
    def __init__(self):
        self.model=UTTTBoard()
        self.message=""
        self.curr_player=Players.X
        self.initialize_view()

    """ ********* View Section ********* """
    def initialize_view(self):
        self.model.add_observer(self)

    def update(self, Subject: UTTTBoard, Client_Data: str) -> None:
        print(self.model)
        print("Status: "+ self.model.game_status.name)
        self.message=Client_Data

    def run(self):
        print("Welcome to Ultimate Tic Tac Toe!")
        self.update(self.model, None)
        square=-1
        while self.model.game_status==GameStatus.NOT_OVER:
            # Continue based off if next square is claimed
            while True:
                if square>=0 and square<9 and self.model.board[square].get_claim_status() is ClaimStatus.NONE :
                    print("Player " + self.curr_player.value + " place your next marker in square " + str(square))
                else:
                    square = int(input("Player " + self.curr_player.value + ", enter the square to add your marker: "))
                cell = int(input("Enter the cell to add your marker: "))
                self.model.make_move(square,cell,self.curr_player)
                if self.message != "Invalid Move.": break
                else: print(self.message)
            square=cell
            #Switch Player
            if self.curr_player == Players.X:
                self.curr_player = Players.O
            else:
                self.curr_player = Players.X

        update(self.model, None)



if __name__ == '__main__':
    ptui = UTTTptui()
    ptui.run()