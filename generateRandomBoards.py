import random
from BoardWrapper import BoardWrapper


# from https://www.tutorialspoint.com/How-to-generate-non-repeating-random-numbers-in-Python on 1.2.24 20:00

def create_random_board():
    random_board = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # board has 9 places
    random.shuffle(random_board)  # numbers set randomly in list
    # traversing the loop 9 times
    board_wrapper = BoardWrapper(tuple(random_board), None, 0, 9999)  # set random_board tuple so it cannot be edited
    return board_wrapper


def create_random_list(number):
    board_list = []  # how many boards should be created
    for i in range(number):
        new = create_random_board()
        board_list.append(new)
    return board_list
