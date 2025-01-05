
import math 
import copy
import multiprocessing

from boardStates import boardStateTest, boardStateA, boardStateB, boardStateC, boardStateD

from additionalFunctions import check_win, display_board, findPlayerPawns, findMaxSteps
from gameStateEvaluation import improvedHeurtistic, naiveHeurtistic, countNBH

# defining the game play flow
class Connect4Game:
    def __init__(self, player1Type, depth, boardName = boardStateA, player2Type = 0, heuristicFunc = 0, player1Ordered = False, player2Ordered = False):

        # avaible decision making functions
        agent_dict = {
            "human": self.human_play,
            "a-bpruning": self.alphabetaPruning_play,
            "minimax": self.minimax_play,
        }
        
        # choose how each player in 2 player game will play
        # one must always be the autonomous agent
        self.player1Type = agent_dict.get(player1Type)
        # should state search be ordered by best to worst states 
        self.player1Ordered = player1Ordered

        # other could be autonomous agent or user
        self.player2Type = agent_dict.get(player2Type) 
        self.player2Ordered = player2Ordered

        # choose the Heuristic function which determines desirable board states
        self.heuristicFunc = improvedHeurtistic if heuristicFunc == "improved" else naiveHeurtistic

        # Initialize the game board
        self.board = [[' ' for _ in range(7)] for _ in range(7)]

        # the search depth 
        self.depth = depth
        
        # keeping track of nodes visited
        self.numNodes = []

        # board specified
        self.board = boardName(self.board)

    """
    Avaible Playing Methods are shown bellow, these include: --------------------------------------------------------------------------------
    - human decides the move
    - minimax algorithm decides the move
    - alpha-beta prunning algorithm decides the move 
    The 2 above algorithms also have an ordered option where they board states are evaluated at a shallow depth first, and the search continues
    based on which states are most likely to produce better game outcomes for that player.
    """
    def human_play(self, maxPlayer):
        """
        The human will be prompted to decide the next move, no algorithm is performed
        """
        # Make a move on the board
        # prompt user for move 
        inputString = input('What\'s the AGENT\'s next move? Write in xyDirecStep (eg: 21W1)\n') 
        if len(inputString) < 4:
            print("not enough inputs!")
            return 0
        elif len(inputString) > 4:
            print("too many inputs!")
            return 0

        # package into the active pawn's location, direction we want it to move, and the amount of steps to take
        x, y, direction, steps = int(inputString[0])-1, int(inputString[1])-1, inputString[2], int(inputString[3])
        return x, y, direction, steps
    
    def minimax_play(self, maxPlayer, ordered = 0):
        """
        MiniMax algorithm is used the dermine next best move for the player. Depending on which player's turn it 
        is (based on the bool value of maxPlayer), the score of the board state will either be minimized or maximized
        """
        # call minimax to find best move 
        eval, move, nodes = self.minimax(self.board, self.depth, maxPlayer)
        self.numNodes.append(nodes)
        x, y, direction, steps = move[0], move[1], move[2], move[3] 
        return x, y, direction, steps

    def alphabetaPruning_play(self, maxPlayer):
        """
        The alpha-beta prunning algorithm is used to determine the next move, which is similar but faster than the minimax alg
        """
        # call minimax to find best move 
        alpha = -math.inf
        beta = math.inf

        v, move, nodes = self.alphabetaPruning(self.board, self.depth, alpha, beta, maxPlayer)
        self.numNodes.append(nodes)

        x, y, direction, steps = move[0], move[1], move[2], move[3] 
        return x, y, direction, steps
    """
    ------------------------------------------------------------------------------------------------------------------------------------------
    """
    def findChildern(self, board, maxPlayer):
        '''
        finds all possible board states spawning from the input variable board
        '''
        childern = []

        # determine pawn symbol
        playerPawn = self.player2_Character if maxPlayer else self.player1_Character
        

        # find all possibble pawns that can be played
        playerPawns = findPlayerPawns(board, playerPawn)

        directions = ["N", "S", "E", "W"]

        # for each of player's pawn
        for pawn in playerPawns:
            # coordinates of pawn
            xPawn, yPawn = pawn

            # count other player's neighbours of pawn at (x,y) to determine max steps 
            ngb = countNBH(self, board, xPawn, yPawn, maxPlayer)

            # What is the largest amount of steps that pawn can take?
            maxSteps = findMaxSteps(ngb)
            
            # don't check if pawn can't move
            if not(maxSteps == 0):
                # make each possible move
                for step in range(1, maxSteps+1): # for each step 
                    for direction in directions: # for each direction (N,S,E,W)
                        boardChild = self.action(board, xPawn, yPawn, direction, step, maxPlayer, show=0)
                        if boardChild:
                            childern.append((boardChild, xPawn, yPawn, direction, step))
        
        if childern == []: # no moves avaible here 
            print('here')

        return childern
    
    def minimax(self, board, depth, maxPlayer, maxDepth = -1, count = 0, prune = False, alpha = -math.inf, beta = math.inf):
        '''
        The minimax algorithm to determine move with best board state
        alpha-beta prunning is possible with the prune function
        '''
        # check if this is a winning board
        result = check_win(board)
        win = (result == "X") or (result == "O")
        # return heuristic if it's a win or an end depth
        if depth == 0 or win:
            v = self.heuristicFunc(board, maxPlayer)
            count += 1
            return v, None, count
        
        # determine which moves to do first by ordering the board states
        ordered = self.player2Ordered if maxPlayer else self.player1Ordered
        if ordered and depth > maxDepth: # will only be updated at the first depth
            maxDepth = depth
            allChildBoards = [c[0] for c in childern]
            boardEvals = [abs(self.heuristicFunc(b, maxPlayer)) for b in allChildBoards]
            checkOrder = sorted(enumerate(boardEvals), key = lambda x:x[1], reverse = True)
            index = [c[0] for c in checkOrder]
            childern_ordered = [childern[i] for i in index]
            childern = childern_ordered

        bestEval = - math.inf if maxPlayer else math.inf
        minSteps = -1
        
        # get all possible board moves from this state
        childern =  self.findChildern(board, maxPlayer)

        for child in childern:
            childBoard = child[0]
            eval, _, ccount, minSteps = self.minimax(childBoard, depth-1, not(maxPlayer), alpha=alpha, beta=beta) # since this turn was maxPlayer, next is not
            count += ccount + 1

            eval_update = eval > bestEval if maxPlayer else eval < bestEval
            if eval_update or ((eval == bestEval) and (child[4] > minSteps)):
                bestEval = eval
                minSteps = child[4]
                bestMove = (child[1], child[2], child[3], child[4]) # x, y, dir, steps

            if prune: # don't bother checking all nodes if better results exist
                if maxPlayer:
                        alpha = max(alpha, eval)
                    else:
                        beta = min(beta, eval)

                    if beta <= alpha:
                        break
            
        return bestEval, bestMove, count, minSteps

    """
    ______________________________________________________________________________________________________________________
    """
    # make a turn of the game, depending on which player is playing 
    def takeTurn(self, maxPlayer):
        """
        A game turn is played
        """

        # determine next move ---------------------------------------------
        # the decision making algorithm is different based on player
        playType = self.player2TypeType if maxPlayer else self.player1TypeType

        x, y, direction, steps = playType(maxPlayer, playType)
        #------------------------------------------------------------------

        # make move -------------------------------------------------------
        # calc new board
        self.action(x, y, direction, steps, False)
        #------------------------------------------------------------------

        # return print statment showing what move took place
        msg = str(x)+str(y) + direction + str(steps)

        return msg
    
    def action(self, x, y, direction, steps, maxPlayer, show=1):
        if show:
            print(str(x+1)+str(y+1)+direction+str(steps))

        # check correct pawn is chosen 
        if maxPlayer and (self.board[x][y] == self.agentCharacter or self.board[x][y] == " "):
            print('max player must choose '+ self.playerCharacter +' to move')
            return 0
        elif not(maxPlayer) and (self.board[x][y] == self.playerCharacter or self.board[x][y] == " "):
            print('min player must choose' + self.agentCharacter + 'to move')
            return 0

        # count neighbours or pawn at (x,y) to determine max steps 
        ngb = self.countNBH(self.board, x, y, maxPlayer)
        maxSteps = self.findMaxSteps(ngb)

        # checking steps don't exeed limit
        if steps > maxSteps:
            print("Too many steps! That pawn can only move %d steps"%maxSteps)
            return 0

        # step through all points in between to make sure nothing is in the way
        for step in range(1,steps+1):
            if direction == "W":
                xNew, yNew = x - step, y
            elif direction == "E":
                xNew, yNew = x + step, y
            elif direction == "N":
                xNew, yNew = x, y - step
            elif direction == "S":
                xNew, yNew = x, y + step
            else:
                print("Unavailible move direction")
                return 0

            # check new value is on board
            if (xNew > len(self.board)-1) or (xNew < 0) or (yNew > len(self.board[0])-1) or (yNew < 0):
                if show:
                    print("You moved too far off the board!")
                return 0 
            # check new value isn't overlapping another pawn 
            if (self.board[xNew][yNew] == "X") or (self.board[xNew][yNew] == "O"):
                if show:
                    print("There is another pawn in the way!")
                return 0 
        
        self.board[xNew][yNew] = self.board[x][y]
        self.board[x][y] = ' '

        return 
    
    def play(self, stopItter = math.inf, show = 1):
        """
        game play flow
        """
        # assign character
        self.player1_Character = "O" # this will be the min player
        self.player2_Character = "X" # this will be the max player

        # keep track of count
        turnCount = 0

        # tracking if game is won
        result = 0 

        while result == 0: # no winner yet

            # display board
            if show:
                display_board(self.board)

            # determining max or min player
            maxPlayer = turnCount%2

            if show:
                currentPawn = self.player2_Character if maxPlayer else self.player1_Character
                print("Now " + currentPawn + " agent will move...")

            # make a move
            msg = self.takeTurn(maxPlayer)

            # check who won
            result = check_win(self.board)# records who wins, 0 for noone, 1 or player2, 2 for player1

            # announce winner
            if not(result == 0) and show:
                display_board(self.board)
                print(result + " player won!")
                return self.numNodes
            elif stopItter == turnCount: # stop early condition
                print("game reached max number of turns, GAME OVER.")
                return self.numNodes
            else:
                # do another round of the game
                turnCount += 1

# You can create an instance of Connect4Game and start the game
if __name__ == "__main__":
    '''
    game = Connect4Game("a-bpruning", 2, boardName = boardStateC, agent2Type = "a-bpruning")
    nodesVisited = game.play()
    print("nodesVisited = ", nodesVisited)
    '''
    depth = 3
    game = Connect4Game("a-bpruning", depth, boardName = boardStateA, player2Type = "a-bpruning", heuristicFunc='improved', player1Ordered = False, player2Ordered = False)
    nodesVisited = game.play()