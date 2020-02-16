import math
import pickle
import random

# MONTE CARLO SEARCH ALGORITHM
# use pickle - copy of board and parent is needed
# select, expand, simulate, backpropagate

# node: a board state
# each node has two counts
#   - number of times a node has been seen
#   - number of wins for the given player

# SELECT
# pick the best node
# tries to find an unexpanded node
# selection is diff than random legal moves
# formula for picking best node: number of wins / number of times it was seen
# + sqrt(2) * sqrt(natural log(parent nodes times it was seen) / current nodes times it was seen)

# EXPANSION
# expands the selected node

# SIMULATE
# starts at the spot u just expanded, picks random legal moves, comes up with winner

# BACKPROPAGATE
# updates the information based on winner

class MCNode:
    # making a tree
    # MCNode = node in that tree
    def __init__(self, parent, move, state, unexpanded_moves, winner, piece):
        self.move = move
        self.parent = parent
        self.state = state
        self.winner = winner
        self.nplays = 0 # number of times the board position has been simulated
        self.nwins = 0 # num of times this board has led to a win
        self.children = dict()
        self.piece = piece
        for p in unexpanded_moves:
            self.children[p] = None

    def __str__(self):
        return "{} {} {}".format(self.move, self.nwins, self.nplays)

    def all_moves(self):
        return self.children.keys()

    def all_children(self):
        return self.children.values()

    def child_node(self, move):
        return self.children[move]

    def expand(self, move):
        reconst = pickle.loads(self.state) # turns saved string back into MCNode object
        reconst.placeMove(move)
        pick = pickle.dumps(reconst) # turn MCNode object back into string
        cn = MCNode(self, move, pick, reconst.getAllValidMoves(), reconst.winner, reconst.piece)
        self.children[move] = cn
        return (hash(reconst), cn)

    def unexpanded_moves(self):
        retval = list()
        for(move, node) in self.children.items():
            if node == None:
                retval.append(move)
        return retval

    def is_fully_expanded(self):
        for p in self.children.values():
            if p == None:
                return False
        return True

    def is_leaf(self):
        return len(self.children) == 0

    def ucb1(self): #MC equation
        return self.nwins / self.nplays + (2 * math.log(self.parent.nplays / self.nplays))

class MCTSPlayer:
    def __init__(self, board, piece):
        self.board = board
        self.piece = piece
        self.nodes = dict()

    def make_node(self):
        if hash(self.board) not in self.nodes:
            unexpanded_moves = self.board.getAllValidMoves()
           # print("T: " + str(self.board.turn))
            node = MCNode(None, None, pickle.dumps(self.board),  unexpanded_moves, self.board.winner, self.board.piece)
            self.nodes[hash(self.board)] = node

    def run_search(self):
        self.make_node()

        for _ in range(1000):
            node = self.select()
            winner = node.winner
            if not node.is_leaf() and winner == None:
                node = self.expand(node)
                winner = self.simulate(node)
            self.backpropagate(node, winner)

        #for c in self.nodes[hash(self.board)].all_children():
            #print (c)

    def select(self):
        node = self.nodes[hash(self.board)]
        while node.is_fully_expanded() and not node.is_leaf():
            moves = node.all_moves()
            best_ucb1 = -1000000
            best_move = None
            for p in moves:
                child_ucb1 = node.child_node(p).ucb1()
                # print ("ucb ", p, child_ucb1)
                if child_ucb1 > best_ucb1:
                    best_move = p
                    best_ucb1 = child_ucb1
            node = node.child_node(best_move)
        return node

    def pickMove(self, board):
        self.run_search()
        return self.best_move().move

    def best_move(self):
        node = self.nodes[hash(self.board)]
        if not node.is_fully_expanded():
            print("Error: Not enough information")
        max = -1000000
        best_move = None
        for p in node.all_children():
            # print (p)
            if(p.nwins == 0):
                ratio = 0
            else:
                ratio = p.nwins / p.nplays
            if ratio > max:
                best_move = p
                max = ratio
        # print ("best ", best_move)
        return best_move


    def expand(self, node):
        #print ("Num unexpanded: ", len(node.unexpanded_moves()))
        move = random.choice(node.unexpanded_moves())
        (h, cn) = node.expand(move)
        self.nodes[h] = cn
        return cn

    def simulate(self, node):
        reconst = pickle.loads(node.state)
        winner = reconst.winner
        while winner == None:
            move = random.choice(reconst.getAllValidMoves())
            reconst.placeMove(move)
            winner = reconst.winner
        return winner

    def backpropagate(self, node, winner):
        while (node != None):
            node.nplays += 1
            if node.piece == 1 and winner == -1 or node.piece == -1 and winner == 1:
                node.nwins += 1
            node = node.parent
