
import math 
import copy
import multiprocessing

from boardStates import boardStateTest, boardStateA, boardStateB, boardStateC, boardStateD

from additionalFunctions import check_win, display_board
from gameStateEvaluation import improvedHeurtistic, naiveHeurtistic

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
        boardNew = self.action(self.board, x, y, direction, steps, False)
        # update game board
        if boardNew:
            self.board = copy.deepcopy(boardNew)
        #------------------------------------------------------------------

        # return print statment showing what move took place
        msg = str(x)+str(y) + direction + str(steps)

        return boardNew, msg
    
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
            newBoard, msg = self.takeTurn(maxPlayer)

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