
class ManualPlayer():
    def __init__(self,piece):
        self.piece = piece
    
    #TODO: correct to full 5-tuple move
    #TODO: check valid
    #to be called by game runner with the board to be played in 
    def pickMove(self,outerRow,outerCol):
        moveRow = input("Enter the row of your move: ")
        moveCol = input("Enter a column to move: ")
        return self.piece,moveRow,moveCol
        