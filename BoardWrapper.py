#Todo: create Board object
# change logic to work with boards
# add trace to board object
#  previous board
#  number of steps

#Todo if fun:
# add matplotlib diagrams
# add possibility to view certain boards and their traces
# add possibility to solve your own boards

import generateRandomBoards
import pickle



class BoardWrapper:

    def __init__(self, board, previous_board, steps, distance):
        self.board = board
        self.previous_board = previous_board
        self.steps = steps
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance


if __name__ == '__main__':
    list = generateRandomBoards.create_random_list(100)
    with open("boards.txt", "wb") as file:
        pickle.dump(list, file, pickle.HIGHEST_PROTOCOL)