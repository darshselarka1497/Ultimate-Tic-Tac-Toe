import math
import random 
import copy

class BasePlayer:
    def __init__(self,piece,maxDepth):
        self.maxDepth = maxDepth
        self.piece = piece
        #TODO: remove self.piece?

    P1_WIN_SCORE = 1000
    P2_WIN_SCORE = -1000
    TIE_SCORE = 0

class ManualPlayer(BasePlayer):
    def __init__(self,piece,maxDepth=None):
        BasePlayer.__init__(self,piece,maxDepth)
        self.piece = piece
        #TODO: remove self.piece?
    
    
    def pickBoard(self,board):
        """
        Utility method for self.pickMove
        Call this function when they have a choice of board to play in
        
        PARAMETERS: 
        board: a Board object

        RETURNS:
        (outerRow,outerCol), a tuple of indices [0,2]
        """
        outerRow = None
        outerCol = None
        while(outerRow == None or outerCol == None):
            print("Enter the coordinates of the board you wish to play")
            outerRow = int(input("Row [0,2]: "))
            if (outerRow < 0 or outerRow > 2):#invalid choice
                print("invlaid Row")
                outerRow = None
                continue
            outerCol = int(input("Column [0,2]: "))
            if (outerCol < 0 or outerCol > 2):#invalid choice
                print("invlaid Row")
                outerRow = None
                continue
            if board.metaBoard[outerRow][outerCol] != 0:#only now can we use indices
                print("This board is not playable! Choose another")
                outerRow = None
                outerCol = None
        return (outerRow,outerCol)

    
    def pickMove(self,board):
        """
        To be called after choosing board by game runner
        Checks if move is valid
        NOTE: does not place move in board
        Calls self.pickBoard to choose outer board if need be

        PARAMETERS: board
        RETURNS: move: a 4-tuple (piece,outerRow,outerCol,innerRow,innerCol)
        
        
        """
        print(str(board))
        if not (board.prevMove is None):
            outerRow,outerCol,innerRow,innerCol = board.prevMove
            if (board.metaBoard[innerRow][innerCol] != 0): #the case we need to prompt user for a board to play in
                moveRow,moveCol = self.pickBoard(board)
            else: #forced to play in this spot
                moveRow,moveCol = innerRow,innerCol
        else: #prompt for a board
            moveRow,moveCol = self.pickBoard(board)
        print("You're playing in board ({0},{1})".format(moveRow,moveCol))
        moveRow1 = int(input("Enter the row of your move: "))
        moveCol1 = int(input("Enter a column to move: "))
        return moveRow, moveCol, moveRow1,moveCol1


class PlayerMM(BasePlayer):
    #TODO minimax with given depth
    #returns best move a
    # nd best score as tuple:
    def __init__(self,piece,maxDepth=1):
        BasePlayer.__init__(self,piece,maxDepth)
        self.piece = piece
        self.maxDepth = maxDepth
        #TODO: remove self.piece?
            
    def myHeuristic(self,board):
        sumv = 0
        for row in range(len(board.metaBoard)):
            for col in range(len(board.metaBoard[row])):
                if not (board.metaBoard[row][col] is None):
                    sumv += board.metaBoard[row][col]

        return sumv*100
    
    def numPiece(self,board):
        num = [[0 for _ in range(3)] for _ in range(3)]
        for outerRow in range(len(board.board)):
            for outerCol in range(len(board.board[outerRow])):
                for innerRow in range(len(board.board[outerRow][outerCol])):
                    for innerCol in range(len(board.board[outerRow][outerCol][innerRow])):
                        if board.board[outerRow][outerCol][innerRow][innerCol] == 0: #playable
                            num[innerRow][innerCol] += 1
        return num

    def betterHeuristic(self,board):
        p1BigThreats,p2BigThreats = self.getBigThreats(board)
        p1lilThreats = [[ 0 for _ in range(3)] for _ in range(3)]
        p2lilThreats = [[ 0 for _ in range(3)] for _ in range(3)]
        for outerRow in range(len(board.metaBoard)):
            for outerCol in range(len(board.metaBoard[outerRow])):
                lilThreats = self.getLittleThreats(board.board[outerRow][outerCol])
                p1lilThreats[outerRow][outerCol] = lilThreats[0]
                p2lilThreats[outerRow][outerCol] = lilThreats[1]
        bigThreatScore=0
        lilThreatScore = 0
        optionalWeight = 1
        numPieces = self.numPiece(board)
        currentPiece = board.piece
        if board.prevMove is None:
            return 0 #no advantage
        else: #safe to do this
            outerRow,outerCol,innerRow,innerCol = board.prevMove
        if board.metaBoard[innerRow][innerCol] != 0: #not playable, so next player can play anywhere
            if currentPiece ==1:
                for p1Threat in p1BigThreats:
                    threatx, threaty = p1Threat
                    bigThreatScore += 100*currentPiece
                    if len(p1lilThreats[threatx][threaty]) > 0:#theres an immediate loss
                        return self.P1_WIN_SCORE
                for p2Threat in p2BigThreats:
                    threatx, threaty = p2Threat
                    bigThreatScore += 100*-1
                    if len(p2lilThreats[threatx][threaty]) > 0:
                        lilThreatScore += len(lilThreats)*-1*numPieces[threatx][threaty]
            else:
                for p2Threat in p2BigThreats:
                    threatx, threaty = p2Threat
                    bigThreatScore += 100*currentPiece
                    if len(p2lilThreats[threatx][threaty]) > 0:#theres an immediate loss
                        return self.P2_WIN_SCORE
                for p1Threat in p1BigThreats:
                    threatx, threaty = p1Threat
                    bigThreatScore += 100*1
                    if len(p1lilThreats[threatx][threaty]) > 0:
                        lilThreatScore += len(lilThreats)*numPieces[threatx][threaty]
            return bigThreatScore + lilThreatScore


        else:#must play here
            if currentPiece == 1:
                danger = p1lilThreats[innerRow][innerCol]
            else:
                danger = p2lilThreats[innerRow][innerCol]
            if len(danger) > 0:
                return currentPiece*self.P1_WIN_SCORE #a positive number
            if currentPiece ==1:
                for p1Threat in p1BigThreats:
                    threatx, threaty = p1Threat
                    bigThreatScore += 100*currentPiece
                    if len(p1lilThreats[threatx][threaty]) > 0:#theres an immediate loss
                        lilThreatScore += len(lilThreats)*numPieces[threatx][threaty]
                for p2Threat in p2BigThreats:
                    threatx, threaty = p2Threat
                    bigThreatScore += 100*-1
                    if len(p2lilThreats[threatx][threaty]) > 0:
                        lilThreatScore += len(lilThreats)*-1*numPieces[threatx][threaty]
            else:
                for p2Threat in p2BigThreats:
                    threatx, threaty = p2Threat
                    bigThreatScore += 100*currentPiece
                    if len(p2lilThreats[threatx][threaty]) > 0:#theres an immediate loss
                        lilThreatScore += len(lilThreats)*-1*numPieces[threatx][threaty]
                for p1Threat in p1BigThreats:
                    threatx, threaty = p1Threat
                    bigThreatScore += 100*1
                    if len(p1lilThreats[threatx][threaty]) > 0:
                        lilThreatScore += len(lilThreats)*numPieces[threatx][threaty]
            return lilThreatScore+bigThreatScore



    def getBigThreats(self,board):
        """
        threat: an open cell (outerRow,outerCol) in a line in {row/col/diagonal} where sum(line) == 2 or sum == -2, depending on player (1 or -1, respectively)
        a threat for player1 is good for player1

        PARAMETERS: board, a Board object
        RETURNS: 
        a list of a list of threats for each player:
        [[player1threat0,...,player1threatN],[player2threat0,...,player2threatM]]
        where a threat is 
        """
        threatLst = [[],[]]
        col0 = 0
        zerosCol0 = []
        col1 = 0
        zerosCol1 = []
        col2 = 0
        zerosCol2 = []
        colLst = [[col0,zerosCol0],[col1,zerosCol1],[col2,zerosCol2]]#TODO account for tuple change
        row0 = 0
        zerosRow0 = []
        row1 = 0
        zerosRow1 = []
        row2 = 0
        zerosRow2 = []
        rowLst = [[row0,zerosRow0],[row1,zerosRow1],[row2,zerosRow2]]
        diag1 = 0
        zerosDiag1 = []
        diag2 = 0
        zerosDiag2 = []
        diagLst = [[diag1,zerosDiag1],[diag2,zerosDiag2]]
        allLst = [colLst,rowLst,diagLst]
        for col in range(board.WIDTH):
            for row in range(board.HEIGHT):
                current = board.metaBoard[row][col]
                if current == None: #so we can sum, we replace the ties with playable spots
                    current = 0

                rowLst[row][0] += current #the sum
                colLst[col][0] += current

                if current == 0: #playable
                    rowLst[row][1] += [(row,col)] #this is a playable space
                    colLst[col][1] += [(row,col)]

                if row == col: #UL to LR diagonal
                    diagLst[0][0] += current
                    if current == 0: #playable
                        diagLst[0][1] += [(row,col)]
                if (row + col) == (board.HEIGHT - 1): #LL to UR diagonal
                    diagLst[1][0] += current
                    if current == 0: #playable
                        diagLst[1][1] += [(row,col)]
                # if current == 0: #means game not finished if not won
                #     areZeros = True
        for category in allLst: #check the sums
            for line in category:
                if line[0] == 2: #threat for 1
                    #TODO
                    threatLst[0] += line[1]
                elif line[0] == -2: #threat for -1
                    threatLst[1] += line[1]
        return (set(threatLst[0]),set(threatLst[1])) #should be a set to avoid repeat cells       
        

    def getLittleThreats(self,innerBoard):
        """
        NOTE: does not test if this board is playable

        threat: an open cell (innerRow,innerCol) in a line in {row/col/diagonal} where sum(line) == 2 or sum == -2, depending on player (1 or -1, respectively)
        a threat for player1 is good for player1

        PARAMETERS: 
        innerBoard: a 3x3 matrix from board.board[outerRow][outerCol]

        RETURNS:
        a list of a list of threats for each player:
        [[player1threat0,...,player1threatN],[player2threat0,...,player2threatM]]
        """
        threatLst = [[],[]]
        col0 = 0
        zerosCol0 = []
        col1 = 0
        zerosCol1 = []
        col2 = 0
        zerosCol2 = []
        colLst = [[col0,zerosCol0],[col1,zerosCol1],[col2,zerosCol2]]#TODO account for tuple change
        row0 = 0
        zerosRow0 = []
        row1 = 0
        zerosRow1 = []
        row2 = 0
        zerosRow2 = []
        rowLst = [[row0,zerosRow0],[row1,zerosRow1],[row2,zerosRow2]]
        diag1 = 0
        zerosDiag1 = []
        diag2 = 0
        zerosDiag2 = []
        diagLst = [[diag1,zerosDiag1],[diag2,zerosDiag2]]
        allLst = [colLst,rowLst,diagLst]
        for col in range(3):
            for row in range(3):
                current = innerBoard[row][col]

                rowLst[row][0] += current #the sum
                colLst[col][0] += current

                if current == 0: #playable
                    rowLst[row][1] += [(row,col)] #this is a playable space
                    colLst[col][1] += [(row,col)]

                if row == col: #UL to LR diagonal
                    diagLst[0][0] += current
                    if current == 0: #playable
                        diagLst[0][1] += [(row,col)]
                if (row + col) == (3 - 1): #LL to UR diagonal
                    diagLst[1][0] += current
                    if current == 0: #playable
                        diagLst[1][1] += [(row,col)]
                # if current == 0: #means game not finished if not won
                #     areZeros = True
        for category in allLst: #check the sums
            for line in category:
                if line[0] == 2: #threat for 1
                    #TODO
                    threatLst[0] += line[1]
                elif line[0] == -2: #threat for -1
                    threatLst[1] += line[1]
        return (set(threatLst[0]),set(threatLst[1])) #should be a set to avoid repeat cells
    def minimax(self,board,depth):
        board = copy.deepcopy(board)
        """
        PARAMETERS: 
        self
        board: a Board object
        depth: int representing current depth (decreasing)
               by convention, the 'deepest' depth is 0

        RETURNS: (move,score) best move and best score where 
        (move,score) 
        move = (piece,outerRow,outerCol,innerRow,innerCol)
        NOTE: if deeper than maxDepth move is None
        """
        heuristic = self.betterHeuristic(board)
        if depth == 0:
            return (None,heuristic)
        end = board.returnWinner()
        if end == 1:#means game is over
            return (None,self.P1_WIN_SCORE,heuristic)
        if end == -1:
            return (None,self.P2_WIN_SCORE)
        if end == 0:
            return (None,self.TIE_SCORE)
        if board.piece == 1: #Player 1
            return self.max_v(board,depth)
        else: #Player 2
            return self.min_v(board,depth)
        
        return
    
    def max_v(self,board,depth):
        """
        finds the best move for Player1
        PARAMETERS:
        board: a Board object
        depth: int representing current depth (decreasing)
        RETURNS: 
        (bestMove,bestScore)
        where bestMove = (piece,)
        """
        #TODO? check if terminal state?
        bestScore = self.P2_WIN_SCORE #the worst possible score
        bestMove = None
        for child in board.getAllValidMoves():
            move = board.getChild(child)
            mm = self.minimax(move,depth-1)
            bestChildScore = mm[-1]#the last element of tuple
            if bestChildScore >= bestScore or bestMove is None:
                bestScore = bestChildScore
                bestMove = child
        
        return (bestMove,bestScore)

    def min_v(self,board,depth):
        """
        finds the best move for Player2
        PARAMETERS:
        board: a Board object
        depth: int representing current depth (decreasing)

        """
        #TODO? check if terminal state?
        bestScore = self.P1_WIN_SCORE #the worst possible score
        bestMove = None
        for child in board.getAllValidMoves():
            move = board.getChild(child)
            mm = self.minimax(move,depth-1)
            bestChildScore = mm[-1]#the last element of tuple
            if bestChildScore <= bestScore or bestMove is None:
                bestScore = bestChildScore
                bestMove = child
        return (bestMove,bestScore)

    def pickMove(self,board):
        move,score = self.minimax(board,self.maxDepth)
        #TODO: what to do with score
        return move
    
class RandomPlayer(BasePlayer):
    def __init__(self,piece,maxDepth=None):
        BasePlayer.__init__(self,piece,maxDepth)
        self.piece = piece
        """
        Chooses a random valid Move for testing our AI
        """
    def pickMove(self,board):
        """
        randomly chooses a valid move
        """
        validMoves = board.getAllValidMoves()
        return random.choice(validMoves)

class PlayerAB(BasePlayer):
    def __init__(self, piece, maxDepth=1000):
        BasePlayer.__init__(self,piece,maxDepth)
    def __init__(self, piece, maxDepth):
        BasePlayer.__init__(self,piece,maxDepth)  
        self.piece = piece

    def my_heuristic(self,board):
        sumv = 0
        for row in range(len(board.metaBoard)):
            for col in range(len(board.metaBoard[row])):
                if not (board.metaBoard[row][col] is None):
                    sumv += board.metaBoard[row][col]
        return sumv*100

    def numPiece(self,board):
        num = [[0 for _ in range(3)] for _ in range(3)]
        for outerRow in range(len(board.board)):
            for outerCol in range(len(board.board[outerRow])):
                for innerRow in range(len(board.board[outerRow][outerCol])):
                    for innerCol in range(len(board.board[outerRow][outerCol][innerRow])):
                        if board.board[outerRow][outerCol][innerRow][innerCol] == 0: #playable
                            num[innerRow][innerCol] += 1
        return num

    def betterHeuristic(self,board):
        p1BigThreats,p2BigThreats = self.getBigThreats(board)
        p1lilThreats = [[ 0 for _ in range(3)] for _ in range(3)]
        p2lilThreats = [[ 0 for _ in range(3)] for _ in range(3)]
        for outerRow in range(len(board.metaBoard)):
            for outerCol in range(len(board.metaBoard[outerRow])):
                lilThreats = self.getLittleThreats(board.board[outerRow][outerCol])
                p1lilThreats[outerRow][outerCol] = lilThreats[0]
                p2lilThreats[outerRow][outerCol] = lilThreats[1]
        bigThreatScore=0
        lilThreatScore = 0
        optionalWeight = 1
        numPieces = self.numPiece(board)
        currentPiece = board.piece
        if board.prevMove is None:
            return 0 #no advantage
        else: #safe to do this
            outerRow,outerCol,innerRow,innerCol = board.prevMove
        if board.metaBoard[innerRow][innerCol] != 0: #not playable, so next player can play anywhere
            if currentPiece ==1:
                for p1Threat in p1BigThreats:
                    threatx, threaty = p1Threat
                    bigThreatScore += 100*currentPiece
                    if len(p1lilThreats[threatx][threaty]) > 0:#theres an immediate loss
                        return self.P1_WIN_SCORE
                for p2Threat in p2BigThreats:
                    threatx, threaty = p2Threat
                    bigThreatScore += 100*-1
                    if len(p2lilThreats[threatx][threaty]) > 0:
                        lilThreatScore += len(lilThreats)*-1*numPieces[threatx][threaty]
            else:
                for p2Threat in p2BigThreats:
                    threatx, threaty = p2Threat
                    bigThreatScore += 100*currentPiece
                    if len(p2lilThreats[threatx][threaty]) > 0:#theres an immediate loss
                        return self.P2_WIN_SCORE
                for p1Threat in p1BigThreats:
                    threatx, threaty = p1Threat
                    bigThreatScore += 100*1
                    if len(p1lilThreats[threatx][threaty]) > 0:
                        lilThreatScore += len(lilThreats)*numPieces[threatx][threaty]
            return bigThreatScore + lilThreatScore


        else:#must play here
            if currentPiece == 1:
                danger = p1lilThreats[innerRow][innerCol]
            else:
                danger = p2lilThreats[innerRow][innerCol]
            if len(danger) > 0:
                return currentPiece*self.P1_WIN_SCORE #a positive number
            if currentPiece ==1:
                for p1Threat in p1BigThreats:
                    threatx, threaty = p1Threat
                    bigThreatScore += 100*currentPiece
                    if len(p1lilThreats[threatx][threaty]) > 0:#theres an immediate loss
                        lilThreatScore += len(lilThreats)*numPieces[threatx][threaty]
                for p2Threat in p2BigThreats:
                    threatx, threaty = p2Threat
                    bigThreatScore += 100*-1
                    if len(p2lilThreats[threatx][threaty]) > 0:
                        lilThreatScore += len(lilThreats)*-1*numPieces[threatx][threaty]
            else:
                for p2Threat in p2BigThreats:
                    threatx, threaty = p2Threat
                    bigThreatScore += 100*currentPiece
                    if len(p2lilThreats[threatx][threaty]) > 0:#theres an immediate loss
                        lilThreatScore += len(lilThreats)*-1*numPieces[threatx][threaty]
                for p1Threat in p1BigThreats:
                    threatx, threaty = p1Threat
                    bigThreatScore += 100*1
                    if len(p1lilThreats[threatx][threaty]) > 0:
                        lilThreatScore += len(lilThreats)*numPieces[threatx][threaty]
            return lilThreatScore+bigThreatScore



    def getBigThreats(self,board):
        """
        threat: an open cell (outerRow,outerCol) in a line in {row/col/diagonal} where sum(line) == 2 or sum == -2, depending on player (1 or -1, respectively)
        a threat for player1 is good for player1

        PARAMETERS: board, a Board object
        RETURNS: 
        a list of a list of threats for each player:
        [[player1threat0,...,player1threatN],[player2threat0,...,player2threatM]]
        where a threat is 
        """
        threatLst = [[],[]]
        col0 = 0
        zerosCol0 = []
        col1 = 0
        zerosCol1 = []
        col2 = 0
        zerosCol2 = []
        colLst = [[col0,zerosCol0],[col1,zerosCol1],[col2,zerosCol2]]#TODO account for tuple change
        row0 = 0
        zerosRow0 = []
        row1 = 0
        zerosRow1 = []
        row2 = 0
        zerosRow2 = []
        rowLst = [[row0,zerosRow0],[row1,zerosRow1],[row2,zerosRow2]]
        diag1 = 0
        zerosDiag1 = []
        diag2 = 0
        zerosDiag2 = []
        diagLst = [[diag1,zerosDiag1],[diag2,zerosDiag2]]
        allLst = [colLst,rowLst,diagLst]
        for col in range(board.WIDTH):
            for row in range(board.HEIGHT):
                current = board.metaBoard[row][col]
                if current == None: #so we can sum, we replace the ties with playable spots
                    current = 0

                rowLst[row][0] += current #the sum
                colLst[col][0] += current

                if current == 0: #playable
                    rowLst[row][1] += [(row,col)] #this is a playable space
                    colLst[col][1] += [(row,col)]

                if row == col: #UL to LR diagonal
                    diagLst[0][0] += current
                    if current == 0: #playable
                        diagLst[0][1] += [(row,col)]
                if (row + col) == (board.HEIGHT - 1): #LL to UR diagonal
                    diagLst[1][0] += current
                    if current == 0: #playable
                        diagLst[1][1] += [(row,col)]
                # if current == 0: #means game not finished if not won
                #     areZeros = True
        for category in allLst: #check the sums
            for line in category:
                if line[0] == 2: #threat for 1
                    #TODO
                    threatLst[0] += line[1]
                elif line[0] == -2: #threat for -1
                    threatLst[1] += line[1]
        return (set(threatLst[0]),set(threatLst[1])) #should be a set to avoid repeat cells       
        

    def getLittleThreats(self,innerBoard):
        """
        NOTE: does not test if this board is playable

        threat: an open cell (innerRow,innerCol) in a line in {row/col/diagonal} where sum(line) == 2 or sum == -2, depending on player (1 or -1, respectively)
        a threat for player1 is good for player1

        PARAMETERS: 
        innerBoard: a 3x3 matrix from board.board[outerRow][outerCol]

        RETURNS:
        a list of a list of threats for each player:
        [[player1threat0,...,player1threatN],[player2threat0,...,player2threatM]]
        """
        threatLst = [[],[]]
        col0 = 0
        zerosCol0 = []
        col1 = 0
        zerosCol1 = []
        col2 = 0
        zerosCol2 = []
        colLst = [[col0,zerosCol0],[col1,zerosCol1],[col2,zerosCol2]]#TODO account for tuple change
        row0 = 0
        zerosRow0 = []
        row1 = 0
        zerosRow1 = []
        row2 = 0
        zerosRow2 = []
        rowLst = [[row0,zerosRow0],[row1,zerosRow1],[row2,zerosRow2]]
        diag1 = 0
        zerosDiag1 = []
        diag2 = 0
        zerosDiag2 = []
        diagLst = [[diag1,zerosDiag1],[diag2,zerosDiag2]]
        allLst = [colLst,rowLst,diagLst]
        for col in range(3):
            for row in range(3):
                current = innerBoard[row][col]

                rowLst[row][0] += current #the sum
                colLst[col][0] += current

                if current == 0: #playable
                    rowLst[row][1] += [(row,col)] #this is a playable space
                    colLst[col][1] += [(row,col)]

                if row == col: #UL to LR diagonal
                    diagLst[0][0] += current
                    if current == 0: #playable
                        diagLst[0][1] += [(row,col)]
                if (row + col) == (3 - 1): #LL to UR diagonal
                    diagLst[1][0] += current
                    if current == 0: #playable
                        diagLst[1][1] += [(row,col)]
                # if current == 0: #means game not finished if not won
                #     areZeros = True
        for category in allLst: #check the sums
            for line in category:
                if line[0] == 2: #threat for 1
                    #TODO
                    threatLst[0] += line[1]
                elif line[0] == -2: #threat for -1
                    threatLst[1] += line[1]
        return (set(threatLst[0]),set(threatLst[1])) #should be a set to avoid repeat cells

    def alphabeta(self,board,depth,alpha,beta):
        board = copy.deepcopy(board)
        heuristic = self.betterHeuristic(board)

        end = board.returnWinner()

        if depth <= 0 and end == None:
            return None, heuristic

        bm = None

        if end == -1:
            return None, self.P2_WIN_SCORE
        if end == 0:
            return None, self.TIE_SCORE
        if end == 1:
            return None, self.P1_WIN_SCORE

        if board.piece is 1:
            bs = -math.inf
        else:
            bs = math.inf

        for child in board.getAllValidMoves():
            curr_val = self.alphabeta(board.getChild(child), depth - 1, alpha, beta)[1]
            if board.piece == -1:
                if bm == None or curr_val < bs:
                    bm = child
                    bs = curr_val
                    beta = min(beta, curr_val)
                    if bs >= alpha:
                        break  # pruning
            elif board.piece == 1:
                if bm == None or curr_val > bs:
                    bm = child
                    bs = curr_val
                    alpha = max(alpha, curr_val)
                    if alpha >= beta:
                        break
        return bm, bs

    def pickMove(self,board):
        move,score = self.alphabeta(board, self.maxDepth, -math.inf, math.inf)
        return move