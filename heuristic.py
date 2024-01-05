# calculateDistance

# import puzzleSolver
from scipy.spatial.distance import hamming
from scipy.spatial.distance import cityblock


# endBoard = puzzleSolver.endBoard

def manhattan(board, end_board):
    dist = 0
    for i in range(len(board)):
        element = board[i]
        if element != 0:
            should = end_board.index(element)
            dist_row = int(should / 3) - int(i / 3)
            dist_col = should % 3 - i % 3
            dist += abs(dist_col) + abs(dist_row)
    return dist


def manhattan2(board, end_board):
    return cityblock(board, end_board)


def hamming(board, end_board):
    dist = 0
    for i in range(len(board)):
        element = board[i]
        if element:
            should = end_board.index(element)
            if i != should:
                dist += 1
    return dist


def hamming2(board, end_board):
    return hamming(board, end_board) * len(board)


def calculate_distance_simple(board, end_board):
    dist = 0
    for i in range(len(board)):
        dist += abs(end_board[i] - board[i])
    return dist


def calculate_distance_list(board, end_board):
    dist = 0
    for i in range(len(board)):
        element = board[i]
        dist += abs(end_board.index(element) - i)
    return dist


def astar(board, end_board):
    dist = 0
    for i in range(len(board)):
        element = board[i]
        if element != 0:
            should = end_board.index(element)
            dist_row = should / 3 - i / 3
            dist_col = should % 3 - i % 3
            dist += int(abs(dist_col + int(dist_row)) * 1.2)
    return dist
