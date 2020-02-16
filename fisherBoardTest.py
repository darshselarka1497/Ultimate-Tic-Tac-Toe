from FisherBoard import Board



if __name__ == '__main__':
    #give a list and the previous move, check if placing a move in that board gives a move in the list of expected moves
    #expected moves: board_template[1]
    egPiece = -1
    egOuterRow = 0
    egOuterCol = 0
    egInnerRow = 0
    egInnerCol = 0
    expectedMove = (egPiece,egOuterRow,egOuterCol,egInnerRow,egInnerCol)

    prevPiece = 1
    prevOuterRow = 1
    prevOuterCol = 0
    prevInnerRow = 0
    prevInnerCol = 0
    previousMove = (prevPiece,prevOuterRow,prevOuterCol,prevInnerRow,prevInnerCol)
    board_template = Board(fromList=[[[[0, 0, 0], 
                                        [0, 0, 0], 
                                        [0, 0, 0]], [[0, 0, 0], 
                                                    [0, 0, 0], 
                                                    [0, 0, 0]], [[0, 0, 0], 
                                                                [0, 0, 0], 
                                                                [0, 0, 0]]],
                                        [[[0, 0, 0], 
                                        [0, 0, 0], 
                                        [0, 0, 0]], [[0, 0, 0], 
                                                    [0, 0, 0], 
                                                    [0, 0, 0]], [[0, 0, 0], 
                                                                [0, 0, 0], 
                                                                [0, 0, 0]]], 
                                        [[[0, 0, 0], 
                                        [0, 0, 0], 
                                        [0, 0, 0]], [[0, 0, 0], 
                                                    [0, 0, 0], 
                                                    [0, 0, 0]], [[0, 0, 0], 
                                                                [0, 0, 0], 
                                                                [0, 0, 0]]]],prevMove=previousMove),[expectedMove]
    near_end_board_1 = Board(fromList=[[[[0, 0, 0], 
                                        [0, 0, -1], 
                                        [0, 0, 0]], [[0, 0, 0], 
                                                    [-1, -1, -1], 
                                                    [0, 0, 0]], [[0, 0, 0], 
                                                                [0, -1, -1], 
                                                                [0, 0, 0]]], 
                                        [[[0, 0, 0], 
                                        [1, 0, 1], 
                                        [-1, 0, 0]], [[0, 0, 1], 
                                                    [0, 1, 0], 
                                                    [1, 0, 0]], [[1, 1, 1], 
                                                                [0, 0, 0], 
                                                                [0, 0, 0]]], 
                                        [[[0, 1, 0], 
                                        [-1, 0, 0], 
                                        [0, 0, 0]], [[0, 0, 0], 
                                                    [0, 0, 0], 
                                                    [0, 0, 0]], [[0, 0, 0], 
                                                                [0, 0, 0],      
                                                                [0, 0, 0]]]],prevMove=(-1,2,0,1,0)),[(1,1,0,1,1)]#expect a 1 at [1][0][1][1]
    near_end_board_2 = Board(fromList=[[[[0, 0, 0], 
                                        [0, -1, -1], 
                                        [0, 0, 0]], [[0, 0, 0], 
                                                    [-1, -1, -1], 
                                                    [0, 0, 0]], [[0, 0, 0], 
                                                                [-1, -1, -1], 
                                                                [0, 0, 0]]], 
                                        [[[0, -1, 0], 
                                        [1, 0, 1], 
                                        [-1, 0, 0]], [[0, 0, 1], 
                                                    [0, 1, 0], 
                                                    [1, 0, 0]], [[1, 1, 1], 
                                                                [0, 0, 0], 
                                                                [0, 0, 0]]], 
                                        [[[0, 1, 0], 
                                        [-1, 0, 0], 
                                        [0, 0, 0]], [[0, 0, 0], 
                                                    [1, 0, 0], 
                                                    [0, 0, 0]], [[0, 0, 0], 
                                                                [0, 0, 0],      
                                                                [0, 0, 0]]]],prevMove=(-1,2,0,1,0)),[(1,1,0,1,1)] 
    near_end_board_3 = Board(fromList=[[[[0, -1, 0], 
                                        [0, 1, 1], 
                                        [0, 0, 0]], [[0, -1, 1], 
                                                    [0, 0, 1], 
                                                    [0, 0, 1]], [[0, -1, 1], 
                                                                [0, 1, 0], 
                                                                [1, 0, -1]]], 
                                        [[[0, 0, 0], 
                                        [0, 0, 0], 
                                        [0, 1, 0]], [[-1, -1, -1], 
                                                    [0, 0, 0], 
                                                    [1, 0, 0]], [[1, 0, 0], 
                                                                [-1, 0, 0], 
                                                                [-1, -1, 0]]], 
                                        [[[-1, -1, 0], 
                                        [0, 0, 1], 
                                        [0, -1, 1]], [[0, -1, 0], 
                                                    [0, 1, 0], 
                                                    [0, 0, 1]], [[0, 1, -1], 
                                                                [0, 1, -1], 
                                                                [-1, 0, 0]]]],prevMove=(-1,2,0,0,0)),[(1,0,0,1,0)]
    #TODO test case where player can move anywhere
    height = 3
    width = 3
    testBoards = [near_end_board_1,near_end_board_2,near_end_board_3]
    x = Board()
    #print(x.metaBoard)
    one = near_end_board_1[0]
    #print(one.metaBoard)
    #print(one.isLittleEnd(one.board[1][1]),one.board[1][1])
    for test in testBoards:
        boardObject = test[0]
        expectedMove = test[1]
        print(test[0].metaBoard)
    for test in testBoards:
        boardObject = test[0]
        print(boardObject)
        print("Previous move: ",boardObject.prevMove)
        print("All valid moves: ",boardObject.getAllValidMoves())
        

