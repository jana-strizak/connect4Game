from additionalFunctions import check_win

'''
The heuristic function is used to quantify the 'goodness' of the game's state. There are 2 functions, a basic naive heuristic and a more 
complex heuistic.
'''
def countNBH(game, board, x, y, maxPlayer, same = False):
    """
    Counts the number of pawns around pawn in x, y location. 
    maxPlayer tells it if it is the max or min player's POV
    same indicates wheither to count the same of different pawns 
    """
    # determine pawn symbol
    if maxPlayer:
        player = game.player2_Character
        opponent = game.player1_Character
    else:
        player = game.player1_Character
        opponent = game.player2_Character
    
    # swaps pawn that's being counted 
    if same:
        opponent = player

    # initalize num of neigbourhood pieces
    ngb = 0

    for boarderX in range(x-1,x+2):
        for boarderY in range(y-1,y+2):
            # check it is within the board
            xInBoard = (boarderX >= 0) and (boarderX < len(game.board))
            yInBoard = (boarderY >= 0) and (boarderY < len(game.board[0]))
            # check if it's the location of itself
            notItself = not((boarderX == x) and (boarderY == y))
            if xInBoard and yInBoard and notItself: 
                # if boarder pawn is an opponent pawn
                if (board[x][y] == player) and (board[boarderX][boarderY] == opponent):
                    ngb += 1
        return ngb

# naive method of quantifying state of the board
def naiveHeurtistic(game, boardTest, maxPlayer):
    # count number of neightbours of same type for each pawn
    numSame = 0
    for y in range(0,len(boardTest[0])):
        for x in range(len(boardTest)):
            # count number of same pawns
            numSame += countNBH(boardTest, x, y, maxPlayer, same = True)
    #print("numSame = ", numSame)

    numOpponents = 0
    # loop through all points to find opponents in NBH
    for y in range(0,len(boardTest[0])):
        for x in range(len(boardTest)):
            # count number of opponent players
            numOpponents += countNBH(boardTest, x, y, maxPlayer, same = False)
    #print("numOpponents = ", numOpponents)

    # check if there is a win 
    winningPawn = check_win(boardTest)
    #if result:
    #    print("here")
    # wins case
    if (winningPawn == game.player2_Character and maxPlayer) or (winningPawn == game.player1_Character and not(maxPlayer)):
        valueNode = 100
    #  player looses case
    elif (winningPawn == game.player1_Character and maxPlayer) or (winningPawn == game.player2_Character and not(maxPlayer)):
        valueNode = -100
    else:
        valueNode = 2*numSame - numOpponents

    # make value negtive for minPlayer
    if not(maxPlayer):
        valueNode *= -1
    return valueNode

def findPlayerPawns(pawn, board):
        """
        gives location of all player pawns
        """
        players = []

        # loop through entire board and find where the pawn is
        for y in range(0,len(board[0])):
            for x in range(len(board)):
                if board[x][y] == pawn:
                    players.append((x,y))
        return players

def findL(playerPawn, board):
    """
    find if there are L shaped with an open board position 
    An open position in the corner of the board is bad because we can't easily move anything there
    """
    for y in range(0,len(board[0])-1):
        for x in range(len(board)-1):
            # check neightbours y, y+1, and x,x+1
            pawn1, pawn2, pawn3, pawn4 = board[x][y], board[x+1][y], board[x][y+1], board[x+1][y+1]
            # keep track of which pawns are corner pieces
            cornerP = [ 0, 0, 0, 0]
            if x == 0 and y == 0:
                cornerP[0] = 1 # pawn1 is corner 
            elif x == len(board[0])-2 and y == len(board[0])-2:
                cornerP[3] = 1 # pawn4 is corner
            elif x == len(board[0])-2 and y == 0:
                cornerP[1] = 1 # pawn 2 is a corner piece 
            elif x == 0 and y == len(board[0])-2:
                cornerP[2] = 1 #pawn3 is a corner

            countPlayerPawn = 0
            countBlankSpace = 0

            checkPawns = [pawn1, pawn2, pawn3, pawn4]
            check = zip(checkPawns, cornerP)

            for P, c in check:
                if P == playerPawn:
                    countPlayerPawn += 1
                elif (P == " ") and not(c) : # is empty square and not a corner piece
                    countBlankSpace += 1
            
            if countPlayerPawn == 3 and countBlankSpace == 1:
                return 1 # there is an L 
    return 0 # there is no L shape for the maxplayer

def possession(pawn, board):
    """
    quantify the possession of the board
    if more of the pawns are in the center of the board, there is more freedom in movement
    """
    playerPawns = findPlayerPawns(pawn, board)
    score = 0 

    for x, y in playerPawns:
        if (x >= 1 and x <= 5) and (y >= 1 and y <= 5):
            score += 1 # 1 point 
            if (x >= 2 and x <= 4) and (y >= 2 and y <= 4):
                score += 1 # 2 points 
    return score

# more complex heuristic function for determining the 'goodness' of the game state 
def improvedHeurtistic(game, boardTest, maxPlayer):

    # count number of neightbours of same type for each pawn
    numSame = 0
    for y in range(0,len(boardTest[0])):
        for x in range(len(boardTest)):
            # count number of same pawns
            numSame += countNBH(boardTest, x, y, maxPlayer, same = True)

    numOpponents = 0
    # loop through all points to find opponents in NBH
    for y in range(0,len(boardTest[0])):
        for x in range(len(boardTest)):
            # count number of opponent players
            numOpponents += countNBH(boardTest, x, y, maxPlayer, same = False)

    # find if there is anywhere on the board where 3 pawns are already connected (need just one more pawn to finish it)
    playerPawn = game.player2_character if maxPlayer else game.player1_character
    opponentPawn = game.player1_character if maxPlayer else game.player2_character

    LScore_Player = findL(playerPawn, boardTest) # output is binary (Yes/No)
    LScore_Opponent = findL(opponentPawn, boardTest)

    # find how many pawns can actually be played  
    PossessionScore_player = possession(playerPawn, boardTest)
    PossessionScore_Opponent = possession(opponentPawn, boardTest)

   # check if there is a win 
    winningPawn = check_win(boardTest)
    # wins case
    if (winningPawn == game.player2_Character and maxPlayer) or (winningPawn == game.player1_Character and not(maxPlayer)):
        valueNode = 100
    #  player looses case
    elif (winningPawn == game.player1_Character and maxPlayer) or (winningPawn == game.player2_Character and not(maxPlayer)):
        valueNode = -100
    else:
        valueNode = 2*numSame - numOpponents + 5*LScore_Player - 3*LScore_Opponent + PossessionScore_player - 0.5*PossessionScore_Opponent

    # make value negtive for minPlayer
    if not(maxPlayer):
        valueNode *= -1
    return valueNode