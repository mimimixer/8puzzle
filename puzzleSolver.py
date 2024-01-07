import time
from _heapq import heappush, heappop
from multiprocessing.pool import ThreadPool
import pickle
import generateRandomBoards
import heuristic
from BoardWrapper import BoardWrapper
from ui import Loading

end_board = (1, 2, 3, 4, 5, 6, 7, 8, 0)
swap_positions = { # possible positions for swaping
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7]
}

results = [[], [], []] # list where different heuristics save the results


def check_solvable(board_wrapper): #checks if a board is solvable
    board = board_wrapper.board
    solvable = True
    for cell in board:
        if cell:
            for next_cell in board[board.index(cell):]:
                if next_cell < cell and next_cell:
                    solvable = not solvable
    return solvable


'''
addToPipeline - when board is checked, its neighbours are added to the pipeline with their respective weight/cost
needs:
    - pipelinelist (why again? should work without addressing it, no?), 
    - the nieghbouring board of the current checked board to add into list, and 
    - the used heuristics '''


def add_to_pipeline(pipeline_list, board_wrapper, heuristics):
    # alreadychecked = any(board in sublist for sublist in listOfMoves)
    board_wrapper.distance = heuristics(board_wrapper, end_board)  # calculate remaining distance to endboard
    dist = board_wrapper.distance
    heappush(pipeline_list, (dist, board_wrapper)) #adds current board to pipeline list depending on distance
    return pipeline_list


def swap(board_wrapper, x, y):  # method for creating neighbouring boards, as tupels are not changeble
    board = board_wrapper.board
    tmp = list(board)
    tmp[x] = board[y]
    tmp[y] = board[x]

    swaped_board = BoardWrapper(tuple(tmp), board_wrapper, board_wrapper.steps + 1, board_wrapper.distance)

    return swaped_board


def search_step(pipeline_list, heuristics, list_of_moves):
    # method to search for the neighbours of the current board, depending of the location of the empty cell (=0)
    board_wrapper = heappop(pipeline_list)[1]  # take first item of pipelinelist, that is element with smallest cost
    board = board_wrapper.board
    list_of_moves.append(board)  # put it into the list_of_moves which is also how number of nodes is calculated

    if board == end_board:  # stops of end board is found
        return board_wrapper, True

    for position in range(len(board)):
        if board[position] == 0:
            for swap_position in swap_positions[position]:
                # stopps calculating backwards
                if board_wrapper.previous_board and board_wrapper.previous_board.board[swap_position] == 0:
                    continue
                new_board = swap(board_wrapper, position, swap_position)
                if new_board.steps > 32: # as every board is possible to be solved in less than 31 moves it doesn't consider boards with more steps
                    continue
                prev = board_wrapper
                for _ in range(new_board.steps - 1):  # looks at all previous boards to eliminate duplicates
                    if new_board.board == prev.board:
                        break
                    prev = prev.previous_board
                else:
                    add_to_pipeline(pipeline_list, new_board, heuristics)
            break
    return board_wrapper, False


def slide(start_board_wrapper, current_heuristic, index):
    # finally the searching method: start is the the board to be checked with certain
    # heuristic
    start = time.time()
    list_of_moves = [] # initializes list of moves and pipeline
    pipeline_list = []
    add_to_pipeline(pipeline_list, start_board_wrapper, current_heuristic) # add first to pipeline
    current_board_wrapper, done = search_step(pipeline_list, current_heuristic, list_of_moves) # calculate first steps
    for counter in range(1820000):
        if done: # if program is done save current board and infos to result list
            results[index].append([current_board_wrapper, len(list_of_moves), time.time() - start])
            return current_board_wrapper, len(list_of_moves)
        # repeat introducing boards into pipeline
        current_board_wrapper, done = search_step(pipeline_list, current_heuristic, list_of_moves)
    else:
        print("too many moves")


def run_puzzle_solver(board_wrapper_list, current_heuristic, index):
    # run the solving algorithm for a whole list of board while cheing the time for fining solution. check for
    # solvability first. return number of unsolvable puzzles in list, number of solvable puzzles and time for
    # finding solution
    pool = ThreadPool() # start multithreading
    num_of_unsolvable = 0
    for board_wrapper_index in range(len(board_wrapper_list)):
        start_board_wrapper = board_wrapper_list[board_wrapper_index]
        if check_solvable(start_board_wrapper): # only looks at solvable
            pool.apply_async(slide, (start_board_wrapper, current_heuristic, index))
        else:
            num_of_unsolvable += 1
    pool.close()
    pool.join() # waits till all threads have finished


def handle_start(input_letter, num_of_boards):
    print("Loading, please wait...")

    if num_of_boards == -1:
        with open("boards.txt", "rb") as file:  # loads pregenerated boards for testing
            boards100 = pickle.load(file)
        num_of_boards = 100
    else:
        boards100 = generateRandomBoards.create_random_list(num_of_boards) # generates n number of boards

    #clears results
    results[0] = []
    results[1] = []
    results[2] = []

    unsolv = 0

    for board in boards100:  # calculate number of unsolvable boards
        if not check_solvable(board):
            unsolv += 1

    if "H" in input_letter: # start each heuristic seperatly
        h_time = time.time()
        run_puzzle_solver(boards100, heuristic.hamming1, 2)
        results[2].append([None, unsolv, (time.time() - h_time), "hamming"]) # append additional info
        print("Hamming has finished!")

    if "M" in input_letter:
        m_time = time.time()
        run_puzzle_solver(boards100, heuristic.manhattan, 1)
        results[1].append([None, unsolv, (time.time() - m_time), "manhattan"]) # append additional info
        print("Manhattan has finished!")

    if "aS" in input_letter:
        aS_time = time.time()
        run_puzzle_solver(boards100, heuristic.astar, 0)
        results[0].append([None, unsolv, (time.time() - aS_time), "astar"]) # append additional info
        print("aStar has finished!")

    result = results
    ui = Loading()
    ui.heuristic_options(result)
