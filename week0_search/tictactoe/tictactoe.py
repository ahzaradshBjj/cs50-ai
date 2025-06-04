"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]


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

    # Board's first state(all None)

    # if board == initial_state():
    #     next_turn_player = X
    # else:
    #     x_quantity = sum(column is X for row in board for column in row)
    #     o_quantity = sum(column is O for row in board for column in row)

    #     if x_quantity > o_quantity:
    #         next_turn_player = O
    #     else:
    #         next_turn_player = X
    flat_board = [cell for row in board for cell in row]

    if flat_board.count(X) > flat_board.count(O):
        return O
    return X
    # return next_turn_player
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = {(row_index, column_index) for row_index, row in enumerate(board)
                        for column_index, _ in enumerate(row) if board[row_index][column_index] == EMPTY}

    return possible_actions
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    board_aux = copy.deepcopy(board)

    # Check negatives
    if (action[0] < 0 or action[1] < 0):
        raise (NotImplementedError)

    # Checks if cell is already occupied
    if board_aux[action[0]][action[1]]:
        raise (NotImplementedError)
    else:
        board_aux[action[0]][action[1]] = player(board)

    return board_aux


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    is_there_winner, winner = three_subsequents(board)

    if is_there_winner:
        return winner
    else:
        return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    is_there_winner, _ = three_subsequents(board)

    # If there is a winner or all elements are not empty
    if is_there_winner or (all(element is not None for row in board for element in row)):
        return True
    else:
        return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    is_there_winner, winner = three_subsequents(board)

    if is_there_winner:
        if winner == X:
            return 1
        else:
            return -1
    else:
        return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    current_player = player(board)

    if current_player == X:
        opt_action, _ = min_value(board)
        return opt_action
    else:
        opt_action, _ = min_value(board)
        print(opt_action)
        return opt_action

    raise NotImplementedError


def three_subsequents(board):
    """
    Returns true if there are three elements in a subsequent order and what player did it
    """

    # Check rows
    for row in board:
        # If all elements of a row are the same and not None
        if (len(set(row)) == 1) and row[0]:
            return True, row[0]

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return True, board[0][j]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return True, board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return True, board[0][2]

    return False, None


def max_value(board):

    # If game ended, return no action
    if terminal(board):
        return None, utility(board)

    v = float('-inf')
    best_action = None

    for action in actions(board):
        aux_action, score = min_value(result(board, action))
        v = max(v, score)
        # if v > score:
        #     return aux_action, v
        if v < score:
            v = score
            best_action = action

    # return action, v
    return best_action, v


def min_value(board):

    # If game ended, return no action
    if terminal(board):
        return None, utility(board)

    v = float('inf')
    best_action = None

    for action in actions(board):
        aux_action, score = max_value(result(board, action))
        v = min(v, score)
        # if v < score:
        #     # print(aux_action, v)
        #     return aux_action, v
        if v > score:
            v = score
            best_action = action

    # return action, v
    return best_action, v


# board = [[EMPTY, X, O],
#          [O, X, X],
#          [X, EMPTY, O]]

board = [[X, EMPTY, O],
         [X, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

minimax(board)
