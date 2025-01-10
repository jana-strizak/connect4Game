from gameSetUp import Connect4Game
from boardStates import boardStateTest, boardStateA, boardStateB, boardStateC, boardStateD

"""
Set-up inital game states
"""
# select the search depth of the algorithm. Larger depth means the agent is able to search through 
# more turns of the game, but it will also take longer to decide a move. depth of 4 is recommended
depth = 4

# select the starting state of the board. boardStateA is hardest board
board = boardStateA

# select how each player plays. Availble are using the simple minimax algorhtm, or minimax with 
# alpha-beta prunning to weed out branches of the game that lead to worse than we've already seen
# results. Usng alpha-beta prunning will lead to faster agent decision making. It is also possible
# to play as the human against the agent. In this case you will be prompted to decide your next move.
player1Alg = "a-bpruning" # or "minimax" or "human"
player2Alg = "a-bpruning"

# the heuristic function is used to evaluate the 'goodness' of the game's state
heuristicFunc='improved'
#heuristicFunc='naive'

player1Ordered = True
Player2Ordered = True 

game = Connect4Game(player1Alg, depth, boardName = board, player2Type = player2Alg, heuristicFunc=heuristicFunc, player1Ordered = player1Ordered, player2Ordered = Player2Ordered)
nodesVisited = game.play()