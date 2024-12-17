""" Defining aditional functions which will be used to play the 'Connect 4' game."""

# displaying the board in the terminal for the user to see
def display_board(board):
    # Display the game board in a user-friendly format
    for y in range(0,len(board[0])):
        for x in range(len(board)):
            print(board[x][y], end="")
            if x != len(board)-1:
                print(',',end="")
        print(end="\n")

def check_win(board):
    # Check if there's a win condition
    winner = 0 # no winner 
    for y in range(0,len(board[0])-1):
        for x in range(len(board)-1):
            # check neightbours y, y+1, and x,x+1
            pawn1, pawn2, pawn3, pawn4 = board[x][y], board[x+1][y], board[x][y+1], board[x+1][y+1]
            # winning condition
            if (pawn1 == pawn2) and (pawn3 == pawn4) and (pawn1 == pawn4) and not(pawn1 ==" "):
                winner = pawn1
                return winner # loop can end when win is found 
    # return winner pawn, or 0 for no wins yet
    return winner