import copy
#convention: X plays first
# X represented by 1
# O represented by -1
# open cell rep by 0
#
# Data Structure: 4-d list
# self.board[i] is a row i
# self.board[i][j] is an inner tic tac toe game at row i column j
# self.board[i][j][k] is a row k in an inner game
# self.board[i][j][k][l] is a cell at row k column l in an inner game
#
# self.metaBoard is a 3x3 representation of the outer board, whose values are:
#   1   if won by first player
#   -1  if won by second player
#   None if draw 
#   0   if inner game not over 
#    
class Board():
    #TODO getAllValidMoves(self)
    #TODO getChild 
    #TODO getChildState?

    HEIGHT = 3
    WIDTH = 3

    def __init__(self, orig=None,fromList=None,prevMove=None, winner=None):
        if not orig is None:
            self.board = copy.deepcopy(orig.board)
            self.numMoves = orig.numMoves
            self.prevMove = orig.prevMove
            #self.state = orig.state
            self.piece = 1
            self.metaBoard = orig.metaBoard
            self.winner = winner
            return
        if not fromList is None:
            self.board = fromList
            self.prevMove = prevMove #a 5-tuple of form (piece,outerRow,outerCol,innerRow,innerCol)
            self.numMoves = self.countMoves()
            self.piece = 1
            self.metaBoard = self.buildMetaBoard()
            self.winner = winner
        else:
            self.board = [[[[0 for _ in range(self.HEIGHT)]
                                for _ in range(self.HEIGHT)]
                                    for _ in range(self.WIDTH)]
                                        for _ in range(self.WIDTH)]
            self.piece = 1
            self.prevMove = None
            self.numMoves = 0
            self.metaBoard = [[0 for _ in range(self.HEIGHT)]
                                    for _ in range(self.HEIGHT)]
            self.winner = winner
        #self.state = 0

    def __str__(self):
        boardStr = ""
        for j in range(17):
            for k in range(34):
                if(k % 2 == 0 and j % 2 == 0):
                    boardStr += " "
                elif(k % 4 == 1 and j % 2 == 0):
                    outerRow = int(j / 6)
                    outerCol = int(k / 12)
                    innerRow = int((j % 6) / 2)
                    innerCol = int((k % 12) / 4)
                    marker = self.board[outerRow][outerCol][innerRow][innerCol]
                    if (marker == 0):
                        boardStr += " "
                    elif (marker == 1):
                        boardStr += "X"
                    else:
                        boardStr += "O"
                elif(k % 4 == 3 and k != 11 and k != 23 and j != 5 and j != 11):
                    boardStr += "|"
                elif(k % 4 != 3 and j % 2 == 1 and k != 11 and k != 23 and j != 5 and j != 11):
                    boardStr += "-"
                elif(k == 11 or k == 23 and j != 5 and j != 11):
                    boardStr += " "
            if(j == 5 or j == 11):
                boardStr += "\n"
            boardStr += "\n"
        return boardStr


    #RETURNS : a list of tuples (outerRow,outerCol,innerRow,innerCol), each tuple is a valid move
    def getAllValidMoves(self):
        #if previous move is None, then 
        validMoves = []
        if self.prevMove is None: #all moves are valid
            for outerRow in range(self.HEIGHT):
                for outerCol in range(self.WIDTH):
                    for innerRow in range(self.HEIGHT):
                        for innerCol in range(self.WIDTH):
                            validMoves += [(outerRow,outerCol,innerRow,innerCol)]
            return validMoves
        #elif self.prevMove led to an unplayable inner board
        outerRow,outerCol,innerRow,innerCol = self.prevMove
        if self.metaBoard[innerRow][innerCol] != 0: #can't be played, so player can play in any open location
            for oRow in range(self.HEIGHT):
                for oCol in range(self.WIDTH):
                    if self.metaBoard[oRow][oCol] == 0: #this innerBoard can be played
                        for iRow in range(self.HEIGHT):
                            for iCol in range(self.WIDTH):
                                if self.board[oRow][oCol][iRow][iCol] == 0: #open space
                                    validMoves += [(oRow,oCol,iRow,iCol)]
            return validMoves
        else: #inner board can be played, so player must go in this inner board, ie self.board[innerRow][innerCol]
            for iRow in range(self.HEIGHT):
                for iCol in range(self.WIDTH):
                    #innerRow,innerCol refers to previous move
                    if self.board[innerRow][innerCol][iRow][iCol] == 0: #open space
                        validMoves += [(innerRow,innerCol,iRow,iCol)]
            return validMoves



    #utility method for fromList
    def countMoves(self):
        count = 0
        for outerRow in self.board:
            for outerCell in outerRow:
                for row in outerCell:
                    for cell in row:
                        if cell != 0:
                            count += 1
        return count

    #utility method for fromList
    def buildMetaBoard(self):
        metaBoard = [[0 for _ in range(self.HEIGHT)]
                                    for _ in range(self.HEIGHT)]
        #check each inner board for end
        for outerRow in range(self.HEIGHT):
            for outerCol in range(self.WIDTH):
                outerCell = self.board[outerRow][outerCol]
                metaBoard[outerRow][outerCol] = self.isLittleEnd(outerCell)

        return metaBoard
        
    #NOTE: does not check if a move is valid
    def getChild(self,move):
        '''PARAMETERS: move - a 4-tuple (piece,outerRow,outerCol,innerRow,innerCol)
           RETURNS: Board object resulting from placing move[0] in move[1],move[2],move[3],move[4]'''
        child = Board(self)
        child.placeMove(move)
        return child


    #PARAMETERS:
    #(optional) innerBoard : a 3x3 list
    #                       if not present, will calculate based on last move to save time
    #RETURNS: -1 or 1 if won
    #          0 if not complete
    #          None if draw
    def isLittleEnd(self,innerBoard=None):
        areZeros = False #if there are zeros, the game is not a draw
        if innerBoard is None: #we need to check win for either player
            innerBoard = self.board[self.prevMove[2]][self.prevMove[3]] 
        col0 = 0
        col1 = 0
        col2 = 0
        colLst = [col0,col1,col2]
        row0 = 0
        row1 = 0
        row2 = 0
        rowLst = [row0,row1,row2]
        diag1 = 0
        diag2 = 0
        diagLst = [diag1,diag2]
        allLst = [colLst,rowLst,diagLst]
        for col in range(self.WIDTH):
            for row in range(self.HEIGHT):
                current = innerBoard[row][col]

                rowLst[row] += current
                colLst[col] += current

                if row == col: #UL to LR diagonal
                    diagLst[0] += current
                if (row + col) == (self.HEIGHT - 1): #LL to UR diagonal
                    diagLst[1] += current
                if current == 0: #means game not finished if not won
                    areZeros = True
        for category in allLst: #check the sums
            for line in category:
                if line == 3: #win for 1
                    return 1
                elif line == -3: #win for -1
                    return -1
        if areZeros: #game not finished
            return 0
        else:
            return None #draw

        
    #TODO make so if 1 won, return 1, else if -1 won return -1, else if draw, return None, else return 0
    def isEnd(self):
        return self.hasWon(1) or self.hasWon(-1) or self.isDraw()

    def returnWinner(self):
        if(self.hasWon(1)):
            return 1
        elif(self.hasWon(-1)):
            return -1
        elif(self.isDraw()):
            return 0
        else:
            return None

    def hasWon(self, marker):
        return self.hasWonVertical(marker) or self.hasWonHorizontal(marker) or self.hasWonDiag1(marker) or self.hasWonDiag2(marker)

    def hasWonHorizontal(self, marker):
        hasWon = False
        for row in range(self.WIDTH):
            if(self.metaBoard[row][0] == marker and self.metaBoard[row][1] == marker and self.metaBoard[row][2] == marker):
                hasWon = True
        return hasWon

    def hasWonVertical(self, marker):
        hasWon = False
        for col in range(self.HEIGHT):
            if (self.metaBoard[0][col] == marker and self.metaBoard[1][col] == marker and self.metaBoard[2][col] == marker):
                hasWon = True
        return hasWon

    def hasWonDiag1(self, marker):
        return self.metaBoard[0][0] == marker and self.metaBoard[1][1] == marker and self.metaBoard[2][2] == marker

    def hasWonDiag2(self, marker):
        return self.metaBoard[0][2] == marker and self.metaBoard[1][1] == marker and self.metaBoard[2][0] == marker

    def isDraw(self):
        if(self.hasWon(1) or self.hasWon(-1)):
            return False
        for row in range(self.WIDTH):
            for col in range(self.HEIGHT):
                if(self.metaBoard[row][col] == 0):
                    return False
        return True


    #Parameters:
    #move : a 5-tuple (piece,outerRow,outerCol,innerRow,innerCol)
    #TODO test
    def isValidMove(self,move):
        outerRow = move[0]
        outerCol = move[1]
        innerRow = move[2]
        innerCol = move[3]
        if(outerRow <0 or outerRow > (self.HEIGHT-1) or outerCol < 0 or outerCol > (self.WIDTH-1) or innerRow < 0 or innerRow > (self.HEIGHT-1) or innerCol < 0 or innerCol > (self.WIDTH - 1)):
            return False #out of bounds
        if(self.prevMove is None):
            return True
        if(self.board[outerRow][outerCol][innerRow][innerCol] != 0):
            return False
        if (self.metaBoard[self.prevMove[2]][self.prevMove[3]] != 0): #means previous move led to littleEnd
            if (self.metaBoard[outerRow][outerCol] == 0): #as long as outer board is open
                if (self.board[outerRow][outerCol][innerRow][innerCol] == 0):#as long as inner cell is open
                    return True
                else:
                    return False #inner cell not open
            else:
                return False #outer board not open
        else: #need to play in inner cell
            if (outerRow == self.prevMove[2] and outerCol == self.prevMove[3]): #if the previous inner row/col matches move's outer row outer col
                if self.board[outerRow][outerCol][innerRow][innerCol] == 0: #cell is open
                    return True
                else:
                    return False
            else: #wrong outer row or outer col
                return False
                

    #NOTE: does not check if move is valid
    #updates self.Board
    #checks for isLittleEnd
    #if so, then checks isEnd
    #RETURNS:
    #0 if game not over
    #1 if 1 won 
    #-1 if -1 won
    #None if tie
    def placeMove(self, move):
        self.board[move[0]][move[1]][move[2]][move[3]] = self.piece
        self.prevMove = move
        self.numMoves += 1
        littleWin = self.isLittleEnd(self.board[move[0]][move[1]])
        if littleWin != 0: #either win, lose or draw
            #update metaBoard
            self.metaBoard[move[0]][move[1]] = littleWin
            self.winner = self.returnWinner()
            self.piece = self.piece * -1
            return self.winner#TODO this won't work until we change isEnd
        self.piece = self.piece * -1
        return littleWin #0 since ongoing

    def __hash__(self):
        return hash(str(self))
            



if __name__ == '__main__':
    pass

