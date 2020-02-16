from pip._vendor.distlib.compat import raw_input
import performancePlotter

from GameClient import GameClient

class GameClientRunner:

    def __init__(self):
        self.p1Count = 0
        self.p2Count = 0
        self.drawCount = 0
        print("Player One: Type 1 for Manual Player, 2 for Random Player, 3 for AB Pruning, 4 for MiniMax, 5 for Monte Carlo")
        self.player1 = int(raw_input("Enter number here: "))
        print("Player Two: Type 1 for Manual Player, 2 for Random Player, 3 for AB Pruning, 4 for MiniMax, 5 for Monte Carlo")
        self.player2 = int(raw_input("Enter number here: "))
        self.playAmount = int(raw_input("How many times would you like to play?: "))
        self.names = ["ManualPlayer","Random","AlphaBeta","MiniMax","MonteCarlo"]

    def getStats(self):
        print("Player One won " + str(self.p1Count) + " time(s).")
        print("Player Two won " + str(self.p2Count) + " time(s).")
        print("There were " + str(self.drawCount) + " draws.")
    
        


if __name__ == "__main__":
    g = GameClientRunner()
    for index in range(g.playAmount):
        gc = GameClient(g.player1, g.player2)
        winner = gc.playGame()
        if(winner == 1):
            g.p1Count += 1
        elif(winner == -1):
            g.p2Count += 1
        else:
            g.drawCount += 1
        print(index)
    performancePlotter.plotMatchup((g.p1Count,g.p2Count,g.drawCount,g.names[g.player1-1],g.names[g.player2-1]))
    g.getStats()

