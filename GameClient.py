from pip._vendor.distlib.compat import raw_input

from AIplayer import ManualPlayer
from FisherBoard import Board
from MonteCarlo import MCTSPlayer
from AIplayer import RandomPlayer
from AIplayer import PlayerMM
from AIplayer import PlayerAB

class GameClient:
    # NEED RESTRICTIONS ON MOVES SO U JUST CHOOSE INNER UNLESS WIN OR FIRST MOVE

    def __init__(self, gPlayer1, gPlayer2):
        self.board = Board()
        self.player1 = None
        self.player2 = None
        if(gPlayer1 == 1):
            self.player1 = ManualPlayer(1)
        elif(gPlayer1 == 2):
            self.player1 = RandomPlayer(1)
        elif(gPlayer1 == 3):
            self.player1 = PlayerAB(1,81)
        elif(gPlayer1 == 4):
            self.player1 = PlayerMM(1,81)
        else:
            self.player1 = MCTSPlayer(self.board, 1)

        if (gPlayer2 == 1):
            self.player2 = ManualPlayer(-1)
        elif (gPlayer2 == 2):
            self.player2 = RandomPlayer(-1)
        elif (gPlayer2 == 3):
            self.player2 = PlayerAB(-1,81)
        elif(gPlayer2 == 4):
            self.player2 = PlayerMM(-1,81)
        else:
            self.player2 = MCTSPlayer(self.board, -1)


    def playGame(self):
        p = (self.player1, self.player2)
        while not self.board.isEnd():
            move = p[0].pickMove(self.board)
            while not self.board.isValidMove(move):
                print("That move is not valid")
                move = p[0].pickMove(self.board)
            self.board.placeMove(move)
            p = (p[1], p[0])
        print(self.board)
        winner = self.board.returnWinner()
       # if(winner == 1):
       #     print("Winner: Player One")
       # elif(winner == -1):
       #     print("Winner: Player Two")
       # else:
       #     print("Winner: TIE")
        return winner
       # print("Winner: " + str(self.board.returnWinner()))


if __name__ == "__main__":
    print("Welcome to Ultimate Tic Tac Toe")
    g = GameClient(gPlayer1=3, gPlayer2=4)
    g.playGame()