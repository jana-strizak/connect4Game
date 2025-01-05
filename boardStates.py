def boardStateA(board):
    board[1][0] = 'X'
    board[2][0] = 'X'
    board[4][0] = 'O'
    board[6][1] = 'X'
    board[0][2] = 'O'
    board[0][3] = 'O'
    board[6][3] = 'O'
    board[6][4] = 'O'
    board[0][5] = 'X'
    board[2][6] = 'O'
    board[4][6] = 'X'
    board[5][6] = 'X'

    return board

def boardStateB(board):
    board[1][0] = 'O'
    board[0][3] = 'O'
    board[5][1] = 'O'
    board[6][5] = 'O'
    board[0][6] = 'O'
    board[1][6] = 'O'

    board[4][0] = 'X'
    board[5][0] = 'X'
    board[6][0] = 'X'
    board[4][1] = 'X'
    board[6][1] = 'X'
    board[6][6] = 'X'

    return board

def boardStateC(board):
    board[5][0] = 'O'
    board[5][3] = 'O'
    board[5][5] = 'O'
    board[1][5] = 'O'
    board[2][6] = 'O'
    board[3][6] = 'O'

    board[5][1] = 'X'
    board[4][2] = 'X'
    board[5][2] = 'X'
    board[5][4] = 'X'
    board[0][6] = 'X'
    board[1][6] = 'X'

    return board

def boardStateD(board):
    board[5][0] = 'O'
    board[6][0] = 'O'
    board[4][1] = 'O'
    board[5][3] = 'O'
    board[6][5] = 'O'
    board[6][6] = 'O'

    board[5][1] = 'X'
    board[6][1] = 'X'
    board[1][5] = 'X'
    board[5][5] = 'X'
    board[1][6] = 'X'
    board[2][6] = 'X'
    return board

def boardStateTest(board):
    board[3][0] = 'O'
    board[4][0] = 'O'
    board[4][1] = 'O'
    board[4][3] = 'O'

    board[0][0] = 'X'
    board[0][2] = 'X'
    board[0][4] = 'X'
    board[2][5] = 'X'
    
    return board