import time
import threading
import multiprocessing
from _heapq import heappush, heappop, _heappop_max
from multiprocessing.pool import ThreadPool
import json
import pickle
import generateRandomBoards
import heuristic
from BoardWrapper import BoardWrapper
from ui import Loading
from queue import PriorityQueue

end_board = (1, 2, 3, 4, 5, 6, 7, 8, 0)
swap_positions = {
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

results = [[], [], []]


def check_solvable(board_wrapper):
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


def add_to_pipeline(pipeline_list, board_wrapper, heuristics, list_of_moves):
    # alreadychecked = any(board in sublist for sublist in listOfMoves)
    board = board_wrapper.board
    # if board in list_of_moves:  # if board already checked, skip
    #    return
    board_wrapper.distance = heuristics(board_wrapper, end_board)  # calculate remaining distance to endboard
    dist = board_wrapper.distance
    if dist == board_wrapper.steps:
        dist = 0
    # start = time.time()
    heappush(pipeline_list, (dist, board_wrapper))
    # print(time.time() - start)
    # pipeline_list.put((dist, board_wrapper))
    return pipeline_list
    """if pipeline_list:  # if list not empty
        for i in range(len(pipeline_list)):  # enter neighbours into pipelinelist, ordered after cost
            if pipeline_list[i].distance > dist:
                """"""for j in range(i, len(pipeline_list)):
                    if pipeline_list[j].board is board:  # Todo: mabey chack steps
                        pipeline_list.pop(j)""""""
                pipeline_list.insert(i, board_wrapper)
                return pipeline_list
    pipeline_list.append(board_wrapper)
    return pipeline_list"""


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
    list_of_moves.append(board)  # put it into the already-checked-boards-list to not check again
    # pipeline_list.pop(0)

    if board == end_board:  # Makes the code run 10000 times faster (or so :) )
        return board_wrapper, True

    for position in range(len(board)):
        if board[position] == 0:
            for swap_position in swap_positions[position]:
                # start = time.time()
                if board_wrapper.previous_board and board_wrapper.previous_board.board[swap_position] == 0:
                    continue
                new_board = swap(board_wrapper, position, swap_position)
                if new_board.steps > 32:
                    continue
                b = new_board.previous_board
                for i in range(new_board.steps - 1):  # looks at all previous boards to eliminate duplicates
                    if new_board.board == b.board:
                        # print(time.time()-start)
                        break
                    b = b.previous_board
                else:
                    # print(time.time()-start)
                    add_to_pipeline(pipeline_list, new_board, heuristics, list_of_moves)
            break
    return board_wrapper, False


def slide(start_board_wrapper, current_heuristic,
          index):  # finally the searching method: start is the the board to be checked with certain
    # heuristic
    start = time.time()
    list_of_moves = []
    pipeline_list = PriorityQueue()
    pipeline_list = []
    add_to_pipeline(pipeline_list, start_board_wrapper, current_heuristic,
                    list_of_moves)  # add the first board to the pipeline
    current_board_wrapper, done = search_step(pipeline_list, current_heuristic,
                                              list_of_moves)  # introduce neighbours into pipeline
    for counter in range(1820000):
        # print(counter)
        if done:
            results[index].append([current_board_wrapper, len(list_of_moves), time.time() - start])
            # print(len(results[index]))
            return current_board_wrapper, len(list_of_moves)
        current_board_wrapper, done = search_step(pipeline_list, current_heuristic,
                                                  list_of_moves)  # repeat introducing boards into pipeline
    else:
        print("too many moves")


def run_puzzle_solver(board_wrapper_list, current_heuristic, index):
    # run the solving algorithm for a whole list of board while cheing the time for fining solution. check for
    # solvability first. return number of unsolvable puzzles in list, number of solvable puzzles and time for
    # finding solution
    pool = ThreadPool()
    num_of_unsolvable = 0
    for board_wrapper_index in range(len(board_wrapper_list)):
        # print(end=str(board_wrapper_index) + " ")
        start_board_wrapper = board_wrapper_list[board_wrapper_index]
        # print(check_solvable(start_board_wrapper))
        if check_solvable(start_board_wrapper):
            start = time.time()
            # print(time.time())
            # slide(start_board_wrapper, current_heuristic, index)
            # print(time.time()-start)
            # print(board_wrapper_index)
            pool.apply_async(slide, (start_board_wrapper, current_heuristic, index))
        else:
            # print("unsolvable")
            num_of_unsolvable += 1
            # results[index].append(("unsolvable", 0))
    pool.close()
    # pool.join()
    # print(multiprocessing.cpu_count())

    # print("done", (time.time() - starting_time), current_heuristic.__name__, num_of_unsolvable)
    # print(results)
    # print(results[index][0][0].previous_board.board)
    # print(num_of_unsolvable, "unsolvable puzzles found")
    # print(current_heuristic.__name__, "solution for the other", 100 - num_of_unsolvable, "puzzles found in",
    # (time.time() - starting_time), "seconds")
    # print("with a total of", totalMoves, "steps")
    # print()
    # return solved


def handle_start(input_letter, num_of_boards):
    print("Loading, please wait...")

    if num_of_boards == -1:
        with open("boards.txt", "rb") as file:  # loads pregenerated boards for testing
            boards100 = pickle.load(file)
        num_of_boards = 100
    else:
        boards100 = generateRandomBoards.create_random_list(num_of_boards)

    boards100 = sorted(boards100, key=lambda x: x.distance, reverse=True)

    results[0] = []
    results[1] = []
    results[2] = []
    unsolv = 0
    for board in boards100:  # calculate number of unsolvable boards
        if not check_solvable(board):
            unsolv += 1

    test = {"H": 0, "M": 0, "aS": 0}
    start_time = time.time()

    if "H" in input_letter:
        test["H"] = num_of_boards - unsolv
        # print(num_of_boards - unsolv)
        h_time = time.time()
        run_puzzle_solver(boards100, heuristic.hamming1, 2)
        while len(results[2]) != num_of_boards - unsolv:
        # print(len(results[2]))
            pass
        results[2].append([None, unsolv, (time.time() - h_time), "hamming"])
        print("Hamming has finished!")

    if "M" in input_letter:
        test["M"] = num_of_boards - unsolv
        m_time = time.time()
        run_puzzle_solver(boards100, heuristic.manhattan, 1)
        while len(results[1]) != num_of_boards - unsolv:
        # print(len(results[1]))
            pass
        results[1].append([None, unsolv, (time.time() - m_time), "manhattan"])
        print("Manhattan has finished!")

    if "aS" in input_letter:
        test["aS"] = num_of_boards - unsolv
        aS_time = time.time()
        run_puzzle_solver(boards100, heuristic.astar, 0)
        while len(results[0]) != num_of_boards - unsolv:
        # print(len(results[0]))
            pass
        results[0].append([None, unsolv, (time.time() - aS_time), "astar"])
        print("aStar has finished!")
    # print(unsolv)
    # print()

    # print(time.time() - start_time)
    result = results
    # return result
    ui = Loading()
    ui.heuristic_options(result)


"""if __name__ == '__main__':
    # define how endboard has to look like - 2 versions
    # boards are constructed as tupels: ordered, not changeble (just to be sure we don't mess it up :D)
    # endBoard = (0,1,2,3,4,5,6,7,8)

    # empty helper lists
    list_of_moves = []  # list of already checked boards
    pipelineList = []  # pipeline is neighbourings boards to already checked boards
    shortest_path = []  # list of boards in shortest path
    distances_list = []  # list of distances for visualisation, not necessary
    totalMoves = 0

    # methods

    # check if a board has a solution for our endboards (their solv is even): solv has to be even/odd as endboards
    # solv is calculated as number of smaller integers following each integer

    # test the code:

    # test solvability
    tryboard1 = (7, 2, 4, 5, 0, 6, 8, 3, 1)
    tryboard2 = (4, 6, 1, 2, 0, 3, 7, 5, 8)
    tryboard3 = (1, 2, 3, 4, 5, 6, 8, 7, 0)

    print("try1", check_solvable(tryboard1))
    print("try2", check_solvable(tryboard2))
    print("try3", check_solvable(tryboard3))

    # generate a certain number of boards, here 100 boards
    start_time = time.time()
    num_of_boards = 100
    boards100 = generateRandomBoards.create_random_list(num_of_boards)
    # print("boards were generated in ", (time.time() - start_time), " seconds")
    # for k in range(len(boards100)):
    # print(k + 1, " ", boards100[k])
    unsolv = 0
    for board in boards100:
        if not check_solvable(board):
            unsolv += 1
    test = BoardWrapper((1, 2, 3, 4, 5, 6, 7, 0, 8), None, 0, 0)
    print(check_solvable(test))
    print(boards100[0])
    # print("manhattan", calculateDistanceManhattan(startBoard))
    # print("manhattan2", calculateDistanceManhattan2(startBoard))
    # print("hamming", calculateDistanceHamming(startBoard))
    # print("hamming2", calculateDistanceHamming2(startBoard))
    # print("simple", calculateDistanceSimple(startBoard))
    # print("dist list index", calculateDistanceList(startBoard))
    # print("A* ", calculateDistanceASTAR(startBoard))
    # print()
    print(unsolv)
    # run the puzzlesolver on the created random list
    run_puzzle_solver(boards100, heuristic.manhattan, 1)
    print("a", len(results[1]) - 1)
    while len(results[1]) - 1 != num_of_boards - unsolv:
        print(("a", len(results[1]) - 1), end="\r")

    print("a2", len(results[1]) - 1)

    run_puzzle_solver(boards100, heuristic.astar, 0)
    print("b", len(results[0]) - 1)
    while len(results[0]) - 1 != num_of_boards - unsolv:
        print(("b", len(results[0]) - 1), end="\r")

    print("b2", len(results[0]) - 1)

    run_puzzle_solver(boards100, heuristic.hamming1, 2)
    print("c", len(results[2]) - 1)
    while len(results[2]) - 1 != num_of_boards - unsolv:
        print(("c", len(results[2]) - 1), end="\r")
    print("c2", len(results[2]) - 1)

    for i in results[2]:
        try:
            print(i[0].board, i[0].steps)
        except:
            pass
    # todo ui = threading.Thread()
    astar = multiprocessing.Process(target=run_puzzle_solver, args=(boards100, heuristic.astar, 0))
    manhattan = multiprocessing.Process(target=run_puzzle_solver, args=(boards100, heuristic.manhattan, 1))
    hamming = multiprocessing.Process(target=run_puzzle_solver, args=(boards100, heuristic.hamming, 2))

    astar.start()
    manhattan.start()
    hamming.start()

    astar.join()
    manhattan.join()
    hamming.join()

    print(len(results[0]))
    print(len(results[1]))
    print(len(results[2]))
    print(results[0])
    print(results[1])
    print(results[2])

    with open("test_data.json", "wb") as file:
        pickle.dump(results, file, pickle.HIGHEST_PROTOCOL)
    # b=[]
    # s=0
    # while a.previous_board:
    # if a in b:
    # s += 1
    # b.append(a.board)
    # print(a.board)
    # a = a.previous_board

    # print(s)
    '''
    start_time = time.time()
    for k in range(len(boards100)):
        print(k)
        startBoard = boards100[k]
        slide(startBoard, calculateDistanceASTAR)
        clearLists()
    print ("A* solution was found in", ( time.time()-start_time), " seconds")
    print()

    start_time = time.time()
    for i in range(len(boards100)):
        startBoard = boards100[i]
        slide(startBoard, calculateDistanceManhattan)
        clearLists()
    print ("Manhattan solution was found in", ( time.time()-start_time), " seconds")
    print()
    clearLists()

    start_time = time.time()
    for i in range(len(boards100)):
        startBoard = boards100[i]
        slide(startBoard, calculateDistanceHamming2)
        clearLists()
    print("Hamming solution was found in", (time.time() - start_time), " seconds")
    print()
    clearLists()
    '''

    # print("distances list:")
    # print(distances_list)
    # print("und die liste war")
    # print(list_of_moves)
    # print()
# print(pipelineList)
# print(pipelineList[0])
# print(pipelineList[1][1])
# prettyPrint(endBoard)
"""
