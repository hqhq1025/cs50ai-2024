"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                actions.add((i,j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not isinstance(action, tuple) or len(action) != 2:
        raise ValueError("Invalid action")
    
    i,j = action
    
    if i < 0 or i > 2 or j < 0 or j > 2:
        raise ValueError("Invalid action")
        
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action: cell already occupied")
    
    new_board = copy.deepcopy(board)
    symbol = player(board)
    new_board[i][j] = symbol
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    symbol = board[0][0]
    if symbol is not EMPTY and symbol == board[1][1] and symbol == board[2][2]:
        return symbol
    symbol = board[0][2]
    if symbol is not EMPTY and symbol == board[1][1] and symbol == board[2][0]:
        return symbol
    for i in range(3):
        row_symbol = board[i][0]
        col_symbol = board[0][i]
        if row_symbol is not EMPTY and row_symbol == board[i][1] and row_symbol == board[i][2]:
            return row_symbol
        if col_symbol is not EMPTY and col_symbol == board[1][i] and col_symbol == board[2][i]:
            return col_symbol
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] is EMPTY:
                    return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result is X:
        return 1
    elif result is O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    possible_actions = actions(board)
    best_action = None
    
    if terminal(board):
        return None
    if current_player is X:
        best_value = float('-inf')
        for action in actions(board):
            value = min_value(result(board,action))
            if value > best_value:
                best_value = value
                best_action = action
    
    if current_player is O:
        best_value = float('inf')
        for action in actions(board):
            value = min_value(result(board,action))
            if value < best_value:
                best_value = value
                best_action = action
    
    return best_action

def max_value(board):
    v =  float('-inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board,action)))
    return v

def min_value(board):
    v = float('inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board,action)))
    return v