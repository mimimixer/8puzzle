import time
import threading

import generateRandomBoards
import heuristic
from BoardWrapper import BoardWrapper

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


def add_to_pipeline(pipeline_list, board_wrapper, heuristics):
    # alreadychecked = any(board in sublist for sublist in listOfMoves)
    board = board_wrapper.board
    if board in list_of_moves:  # if board already checked, skip
        return
    board_wrapper.distance = heuristics(board_wrapper, end_board)  # calculate remaining distance to endboard
    dist = board_wrapper.distance
    if pipeline_list:  # if list not empty
        for i in range(len(pipeline_list)):  # enter neighbours into pipelinelist, ordered after cost
            if pipeline_list[i].distance > dist:
                for j in range(i, len(pipeline_list)):
                    """if pipeline_list[j].board is board: #Todo: mabey chack steps
                        pipeline_list.pop(j)"""
                pipeline_list.insert(i, board_wrapper)
                return pipeline_list
    pipeline_list.append(board_wrapper)
    return pipeline_list


def swap(board_wrapper, x, y):  # method for creating neighbouring boards, as tupels are not changeble
    board = board_wrapper.board
    tmp = list(board)
    tmp[x] = board[y]
    tmp[y] = board[x]

    swaped_board = BoardWrapper(tuple(tmp), board_wrapper, board_wrapper.steps + 1, board_wrapper.distance)

    return swaped_board


def search_step(pipeline_list, heuristics):
    # method to search for the neighbours of the current board, depending of the location of the empty cell (=0)
    board_wrapper = pipeline_list[0]  # take first item of pipelinelist, that is element with smallest cost
    wrappers.append(board_wrapper)
    # mothernode = pipelineList[0][2]             #note the number of the node it came from
    # prettyPrint(board)
    # print(pipelineList[0][1])
    # print()
    # listOfMoves.append([board, mothernode])     #put it into the already-checked-boards-list to not check again
    board = board_wrapper.board
    list_of_moves.append(board)  # put it into the already-checked-boards-list to not check again
    # indexCurrentNode = len(listOfMoves)-1

    #distances_list.append(pipeline_list[0][1])  # append cost of current board in pipeline
    pipeline_list.pop(0)  # and delete the element from the pipeline
    # und dann hardcoden, aber irgendwas kann mir da schon einfallen für jede größe?
    if board[4] == 0:
        add_to_pipeline(pipeline_list, swap(board_wrapper, 4, 1), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 4, 3), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 4, 5), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 4, 7), heuristics)
    elif board[0] == 0:
        add_to_pipeline(pipeline_list, swap(board_wrapper, 0, 1), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 0, 3), heuristics)
    elif board[2] == 0:
        add_to_pipeline(pipeline_list, swap(board_wrapper, 2, 1), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 2, 5), heuristics)
    elif board[6] == 0:
        add_to_pipeline(pipeline_list, swap(board_wrapper, 6, 3), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 6, 7), heuristics)
    elif board[8] == 0:
        add_to_pipeline(pipeline_list, swap(board_wrapper, 8, 5), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 8, 7), heuristics)
    elif board[1] == 0:
        add_to_pipeline(pipeline_list, swap(board_wrapper, 1, 4), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 1, 0), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 1, 2), heuristics)
    elif board[3] == 0:
        add_to_pipeline(pipeline_list, swap(board_wrapper, 3, 4), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 3, 0), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 3, 6), heuristics)
    elif board[5] == 0:
        add_to_pipeline(pipeline_list, swap(board_wrapper, 5, 4), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 5, 8), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 5, 2), heuristics)
    elif board[7] == 0:
        add_to_pipeline(pipeline_list, swap(board_wrapper, 7, 4), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 7, 6), heuristics)
        add_to_pipeline(pipeline_list, swap(board_wrapper, 7, 8), heuristics)
    return board_wrapper


def pretty_print(board):  # method for printing board in 3 rows
    for i in range(3):
        for j in range(3):
            print(board[i * 3 + j], end=" ")
            if j == 2:
                print()


def slide(start_board_wrapper, current_heuristic):  # finally the searching method: start is the the board to be checked with certain
    # heuristic
    counter = 0
    add_to_pipeline(pipelineList, start_board_wrapper, current_heuristic)  # add the first board to the pipeline
    current_board_wrapper = search_step(pipelineList, current_heuristic)  # introduce neighbours into pipeline
    for counter in range(182000):
        if list_of_moves[-1] == end_board:
            print("found after ", len(list_of_moves) - 1, "moves")
            return current_board_wrapper, len(list_of_moves)
        current_board_wrapper = search_step(pipelineList, current_heuristic)  # repeat introducing boards into pipeline
    print("already ", counter, "moves done, stopping search")


def trace(list_of_moves):  # trace back the shortest path
    next_move = list_of_moves[-1][1]
    shortest_path.append(list_of_moves[-1][0])
    while next_move != 0:
        shortest_path.append(list_of_moves[next_move][0])
        next_move = list_of_moves[next_move][1]
    return shortest_path


def clear_lists():  # method to clear lists for next bord to check
    list_of_moves.clear()
    pipelineList.clear()
    distances_list.clear()
    shortest_path.clear()


def run_puzzle_solver(board_wrapper_list, current_heuristic, result, index):
    # run the solving algorithm for a whole list of board while cheing the time for fining solution. check for
    # solvability first. return number of unsolvable puzzles in list, number of solvable puzzles and time for
    # finding solution
    starting_time = time.time()
    num_of_unsolvable = 0
    solved = []
    for board_wrapper_index in range(len(board_wrapper_list)):
        print(end=str(board_wrapper_index) + " ")
        start_board_wrapper = board_wrapper_list[board_wrapper_index]
        if check_solvable(start_board_wrapper):
            solved_board_wrapper = slide(start_board_wrapper, current_heuristic)
            # trace(listOfMoves)
            result[index].append(solved_board_wrapper)

            shortest = 99999
            for wrapper in wrappers:
                if wrapper.board == end_board:
                    if shortest > wrapper.steps:
                        a = wrapper
                        shortest = min(shortest, wrapper.steps)
            print("shortest path took", shortest)

            wrappers.clear()
            # totalMoves=totalMoves+len(listOfMoves)
            clear_lists()
        else:
            print("unsolvable")
            num_of_unsolvable += 1
            result[index].append(("unsolvable", 0))
    result[index].append([None, num_of_unsolvable,(time.time() - starting_time)])
    print(num_of_unsolvable, "unsolvable puzzles found")
    print(current_heuristic.__name__, "solution for the other", 100 - num_of_unsolvable, "puzzles found in",
          (time.time() - starting_time), "seconds")
    #print("with a total of", totalMoves, "steps")
    print()
    #return solved


if __name__ == '__main__':

    # define how endboard has to look like - 2 versions
    # boards are constructed as tupels: ordered, not changeble (just to be sure we don't mess it up :D)
    end_board = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    # endBoard = (0,1,2,3,4,5,6,7,8)

    # empty helper lists
    list_of_moves = []  # list of already checked boards
    pipelineList = []  # pipeline is neighbourings boards to already checked boards
    shortest_path = []  # list of boards in shortest path
    distances_list = []  # list of distances for visualisation, not necessary
    totalMoves = 0


    wrappers = []

    # methods

    # check if a board has a solution for our endboards (their solv is even): solv has to be even/odd as endboards
    # solv is calculated as number of smaller integers following each integer

    # test the code:

    # test solvability
    tryboard1 = (7, 2, 4, 5, 0, 6, 8, 3, 1)
    tryboard2 = (4, 6, 1, 2, 0, 3, 7, 5, 8)
    tryboard3 = (1, 2, 3, 4, 5, 6, 8, 7, 0)

    """print("try1", check_solvable(tryboard1))
    print("try2", check_solvable(tryboard2))
    print("try3", check_solvable(tryboard3))"""

    # generate a certain number of boards, here 100 boards
    start_time = time.time()
    boards100 = generateRandomBoards.create_random_list(100)
    print("boards were generated in ", (time.time() - start_time), " seconds")
    for k in range(len(boards100)):
        print(k + 1, " ", boards100[k])

    # print("manhattan", calculateDistanceManhattan(startBoard))
    # print("manhattan2", calculateDistanceManhattan2(startBoard))
    # print("hamming", calculateDistanceHamming(startBoard))
    # print("hamming2", calculateDistanceHamming2(startBoard))
    # print("simple", calculateDistanceSimple(startBoard))
    # print("dist list index", calculateDistanceList(startBoard))
    # print("A* ", calculateDistanceASTAR(startBoard))
    # print()

    # run the puzzlesolver on the created random list
    results = [[], [], []]
    #todo ui = threading.Thread()
    astar = threading.Thread(target=run_puzzle_solver, args=(boards100, heuristic.astar, results, 0))
    manhattan = threading.Thread(target=run_puzzle_solver, args=(boards100, heuristic.manhattan, results, 1))
    hamming = threading.Thread(target=run_puzzle_solver, args=(boards100, heuristic.hamming, results, 2))

    astar.start()
    manhattan.start()
    hamming.start()

    b=[]
    s=0
    while a.previous_board:
        if a in b:
            s += 1
        b.append(a.board)
        print(a.board)
        a = a.previous_board

    print(s)
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

    print("distances list:")
    print(distances_list)
    print("und die liste war")
    print(list_of_moves)
    print()
# print(pipelineList)
# print(pipelineList[0])
# print(pipelineList[1][1])
# prettyPrint(endBoard)
