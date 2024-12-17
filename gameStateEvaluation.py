'''
The heuristic function is used to quantify the 'goodness' of the game's state. There are 2 functions, a basic naive heuristic and a more 
complex heuistic.
'''
def countNBH(self, board, x, y, maxPlayer, same = False):
    """
    Counts the number of pawns around pawn in x, y location. 
    maxPlayer tells it if it is the max or min player's POV
    same indicates wheither to count the same of different pawns 
    """
    # determine pawn symbol
    if maxPlayer:
        player = self.player2_Character
        opponent = self.player1_Character
    else:
        player = self.player1_Character
        opponent = self.player2_Character
    
    # swaps pawn that's being counted 
    if same:
        opponent = player

    # initalize num of neigbourhood pieces
    ngb = 0

    for boarderX in range(x-1,x+2):
        for boarderY in range(y-1,y+2):
            # check it is within the board
            xInBoard = (boarderX >= 0) and (boarderX < len(self.board))
            yInBoard = (boarderY >= 0) and (boarderY < len(self.board[0]))
            # check if it's the location of itself
            notItself = not((boarderX == x) and (boarderY == y))
            if xInBoard and yInBoard and notItself: 
                # if boarder pawn is an opponent pawn
                if (board[x][y] == player) and (board[boarderX][boarderY] == opponent):
                    ngb += 1
        return ngb

# naive method of quantifying state of the board
def naiveHeurtistic(self, boardTest, maxPlayer):
    # count number of neightbours of same type 
    numSame = 0
    for y in range(0,len(boardTest[0])):
        for x in range(len(boardTest)):
            # count number of same pawns
            numSame += self.countNBH(boardTest, x, y, maxPlayer, same = True)
    #print("numSame = ", numSame)

    numOpponents = 0
    # loop through all points to find opponents in NBH
    for y in range(0,len(boardTest[0])):
        for x in range(len(boardTest)):
            # count number of opponent players
            numOpponents += self.countNBH(boardTest, x, y, maxPlayer, same = False)
    #print("numOpponents = ", numOpponents)

    # check if there is a win 
    winningPawn = self.check_win(boardTest)
    #if result:
    #    print("here")
    # wins case
    if (winningPawn == self.playerCharacter and maxPlayer) or (winningPawn == self.agentCharacter and not(maxPlayer)):
        valueNode = 15
    # max player looses case
    elif (winningPawn == self.agentCharacter and maxPlayer) or (winningPawn == self.playerCharacter and not(maxPlayer)):
        valueNode = -15
    else:
        valueNode = 2*numSame - numOpponents

    # make value negtive for minPlayer
    if not(maxPlayer):
        valueNode = -valueNode
    return valueNode