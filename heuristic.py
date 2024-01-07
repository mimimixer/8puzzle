# calculateDistance
import time

#from BoardWrapper import BoardWrapper
# import puzzleSolver
from scipy.spatial.distance import hamming
from scipy.spatial.distance import cityblock


# endBoard = puzzleSolver.endBoard

def manhattan(board_wrapper, end_board):
    board = board_wrapper.board
    dist = 0
    for i in range(len(board)):
        element = board[i]
        if element != 0:
            should = end_board.index(element)
            dist_row = int(should / 3) - int(i / 3)
            dist_col = should % 3 - i % 3
            dist += abs(dist_col) + abs(dist_row)
    return board_wrapper.steps + dist


def hamming1(board_wrapper, end_board):
    board = board_wrapper.board
    dist = 0
    for i in range(len(board)):
        element = board[i]
        if element:
            should = end_board.index(element)
            if i != should:
                dist += 1
    return board_wrapper.steps + dist


def hamming2(board_wrapper, end_board):
    board = board_wrapper.board
    return board_wrapper.steps + hamming(board, end_board) * len(board)


def astar(board_wrapper, end_board):
    board = board_wrapper.board
    dist = 0
    for i in range(len(board)):
        element = board[i]
        if element != 0:
            should = end_board.index(element)
            dist_row = should / 3 - i / 3
            dist_col = should % 3 - i % 3
            dist += int(abs(dist_col + int(dist_row)))
    return board_wrapper.steps + dist * 1.2


if __name__ == '__main__':
    a = [1, 2, 3, 4, 5]
    a.insert(2,"a")
    print(a)
    """print(astar(BoardWrapper(tuple([8,6,7,2,5,4,3,0,1]),None, 0,9999), (1, 2, 3, 4, 5, 6, 7, 8, 0)))
    print(astar(BoardWrapper(tuple([6,4,7,8,5,0,3,2,1]),None, 0,9999), (1, 2, 3, 4, 5, 6, 7, 8, 0)))
    print(manhattan(BoardWrapper(tuple([8,6,7,2,5,4,3,0,1]),None, 0,9999), (1, 2, 3, 4, 5, 6, 7, 8, 0)))
    print(manhattan(BoardWrapper(tuple([6,4,7,8,5,0,3,2,1]),None, 0,9999), (1, 2, 3, 4, 5, 6, 7, 8, 0)))
    print(hamming1(BoardWrapper(tuple([8,6,7,2,5,4,3,0,1]),None, 0,9999), (1, 2, 3, 4, 5, 6, 7, 8, 0)))
    print(hamming1(BoardWrapper(tuple([6,4,7,8,5,0,3,2,1]),None, 0,9999), (1, 2, 3, 4, 5, 6, 7, 8, 0)))
    print(hamming2(BoardWrapper(tuple([8,6,7,2,5,4,3,0,1]),None, 0,9999), (1, 2, 3, 4, 5, 6, 7, 8, 0)))
    print(hamming2(BoardWrapper(tuple([6,4,7,8,5,0,3,2,1]),None, 0,9999), (1, 2, 3, 4, 5, 6, 7, 8, 0)))"""
    #for i in range(182000):
    #    print(i)