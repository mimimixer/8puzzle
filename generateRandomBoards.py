import random
import json
import heuristic
from BoardWrapper import BoardWrapper
# from https://www.tutorialspoint.com/How-to-generate-non-repeating-random-numbers-in-Python on 1.2.24 20:00

def create_random_board():
    random_board = [0, 1, 2, 3, 4, 5, 6, 7, 8] #board has 9 places
    random.shuffle(random_board) #numbers set randomly in list
    # traversing the loop 9 times
    board_wrapper = BoardWrapper(tuple(random_board), None, 0, 9999) #set random_board tuple so it cannot be edited
    board_wrapper.distance = heuristic.manhattan(board_wrapper, (1, 2, 3, 4, 5, 6, 7, 8, 0))
    return board_wrapper


def create_random_list(number):
    board_list = [] #how many boards should be created
    for i in range(number):
        new = create_random_board()
        if new not in board_list:
            board_list.append(new)
    return board_list


#if __name__ == "__main__":
    #print(create_random_list(10))
    """list_hundred = create_random_list(100)
    list_thousand = create_random_list(1000)
    list_ten_thousand = create_random_list(10000)
    with open("boards.json", "w") as file:
        file.write(json.dumps({"100": list_hundred, "1000": list_thousand, "10000": list_ten_thousand}))"""
