
import time
import generateRandomBoards
import heuristic

if __name__ == '__main__':

#define how endboard has to look like - 2 versions
#boards are constructed as tupels: ordered, not changeble (just to be sure we don't mess it up :D)
    endBoard = (1,2,3,4,5,6,7,8,0)
    #endBoard = (0,1,2,3,4,5,6,7,8)

#empty helper lists
    listOfMoves = []        #list of already checked boards
    pipelineList = []       #pipeline is neighbourings boards to already checked boards
    shortestPath = []       # list of boards in shortest path
    distancesList = []      #list of distances for visualisation, not necessary
    totalMoves =0
    #[[startBoard,calculateDistance(startBoard)]]

# test numbers,please delete upon completion
# 724506831
# 461203758

#methods

    #check if a board has a solution for our endboards (their solv is even): solv has to be even/odd as endboards
        #solv is calculated as number of smaller integers following each integer
    def checkSolvable(board):
        solv = 0
        for i in range(len(board)):
            if board[i] != 0:
                for j in range(i, len(board)):
                    if board[j] != 0:
                        if board[j] < board[i]:
                            solv = solv + 1
        return solv

    '''
    addToPipeline - when board is checked, its neighbours are added to the pipeline with their respective weight/cost
    needs:
        - pipelinelist (why again? should work without addressing it, no?), 
        - the nieghbouring board of the current checked board to add into list, and 
        - the used heuristics '''
    def addToPipeline(pipelineList, board, heuristics):
        #alreadychecked = any(board in sublist for sublist in listOfMoves)
        if board in listOfMoves:                    #if board already checked, skip
            return
        dist = heuristics(board, endBoard)          #calculate remaining distance to endboard
        if pipelineList:                            #if list not empty
            for i in range (len(pipelineList)):     #enter neighbours into pipelinelist, ordered after cost
                if pipelineList[i][1] > dist:
                    for j in range(i, len(pipelineList)):
                        if pipelineList[j][0] is board:
                            pipelineList.pop(j)
                    pipelineList.insert(i, [board, dist])
                    return pipelineList
        pipelineList.append([board, dist])
        return pipelineList

    #method for creating neighbouring boards, as tupels are not changeble
    def swap(board, x, y):
        tmp=[]
        tmp = list(x for x in board)
        tmp[x] = board [y]
        tmp[y] = board [x]
        return tuple(tmp)

    #method to search for the neighbours of the current board, depending of the location of the empty cell (=0)
    def searchStep(pipelineList, heuristics):
        board = pipelineList[0][0]                  #take first item of pipelinelist, that is element with smallest cost
        #mothernode = pipelineList[0][2]             #note the number of the node it came from
        #prettyPrint(board)
        #print(pipelineList[0][1])
        #print()
        #listOfMoves.append([board, mothernode])     #put it into the already-checked-boards-list to not check again
        listOfMoves.append(board)                       #put it into the already-checked-boards-list to not check again
        #indexCurrentNode = len(listOfMoves)-1

        distancesList.append(pipelineList[0][1])    #append cost of current board in pipeline
        pipelineList.pop(0)                         #and delete the element from the pipeline
        #und dann hardcoden, aber irgendwas kann mir da schon einfallen für jede größe?
        if board[4] == 0:
            addToPipeline(pipelineList, swap(board, 4, 1), heuristics)
            addToPipeline(pipelineList, swap(board, 4, 3), heuristics)
            addToPipeline(pipelineList, swap(board, 4, 5), heuristics)
            addToPipeline(pipelineList, swap(board, 4, 7), heuristics)
            return pipelineList
        if board[0] == 0:
            addToPipeline(pipelineList,swap(board,0,1), heuristics)
            addToPipeline(pipelineList,swap(board,0,3), heuristics)
        if board[2] == 0:
            addToPipeline(pipelineList,swap(board,2,1), heuristics)
            addToPipeline(pipelineList,swap(board,2,5), heuristics)
        if board[6] == 0:
            addToPipeline(pipelineList,swap(board,6,3), heuristics)
            addToPipeline(pipelineList,swap(board,6,7), heuristics)
        if board[8] == 0:
            addToPipeline(pipelineList,swap(board,8,5), heuristics)
            addToPipeline(pipelineList,swap(board,8,7), heuristics)
        if board[1] == 0:
            addToPipeline(pipelineList,swap(board,1,4), heuristics)
            addToPipeline(pipelineList,swap(board,1,0), heuristics)
            addToPipeline(pipelineList,swap(board,1,2), heuristics)
        if board[3] == 0:
            addToPipeline(pipelineList, swap(board, 3, 4), heuristics)
            addToPipeline(pipelineList, swap(board, 3, 0), heuristics)
            addToPipeline(pipelineList, swap(board, 3, 6), heuristics)
        if board[5] == 0:
            addToPipeline(pipelineList,swap(board,5,4), heuristics)
            addToPipeline(pipelineList,swap(board,5,8), heuristics)
            addToPipeline(pipelineList,swap(board,5,2), heuristics)
        if board[7] == 0:
            addToPipeline(pipelineList,swap(board,7,4), heuristics)
            addToPipeline(pipelineList,swap(board,7,6), heuristics)
            addToPipeline(pipelineList,swap(board,7,8), heuristics)

    #method for printing board in 3 rows
    def prettyPrint(board):
        for i in range(3):
            for j in range(3):
                print(board[i*3+j], end = " ")
                if j == 2:
                    print()

    #finally the searching method: start is the the board to be checked with certain heuristic
    def slide(start, heuristic):
        counter=0
        addToPipeline(pipelineList, start, heuristic)           #add the first board to the pipeline
        searchStep(pipelineList, heuristic)                     #introduce neighbours into pipeline
        while listOfMoves[-1] != endBoard and counter < 10000:  #as long as the first board in pipeline is not solution
            searchStep(pipelineList, heuristic)                 #repeat introducing boards into pipeline
            counter = counter+1
        if len(listOfMoves) > 10000:                            #but stop after 10000 moves, too long or something is wrong
            print("already ", counter, "moves done, stopping search")
            return
        else:
            print("found after ", len(listOfMoves)-1, "moves")

    #trace back the shortest path
    def trace(listOfMoves):
        next = listOfMoves[-1][1]
        shortestPath.append(listOfMoves[-1][0])
        while next != 0:
            shortestPath.append(listOfMoves[next][0])
            next = listOfMoves[next][1]
        return shortestPath


    #method to clear lists for next bord to check
    def clearLists():
        listOfMoves.clear()
        pipelineList.clear()
        distancesList.clear()
        shortestPath.clear()
    #listOfMoves.append(endBoard)
    #addToPipeline(pipelineList,startBoard)
    #addToPipeline(pipelineList, endBoard)

    #run the solving algorithm for a whole list of board while cheing the time for fining solution. check for solvability first.
        #return number of unsolvable puzzles in list, number of solvable puzzles and time for finding solution
    def runPuzzleSolver(list, heuristic):
        start_time = time.time()
        unsolvable=0

        for k in range(len(list)):
            print(k)
            startBoard = list[k]
            if checkSolvable(startBoard)%2 == 0:
                slide(startBoard, heuristic)
                #trace(listOfMoves)
                print ("shortest path was ", len(shortestPath), "with : ", shortestPath)
                #totalMoves=totalMoves+len(listOfMoves)
                clearLists()
            else:
                unsolvable=unsolvable+1
        print(unsolvable, " unsolvable puzzles found")
        print(heuristic.__name__, " solution for the other ", 100-unsolvable, "puzzles found in", (time.time() - start_time), " seconds")
        print("with a total of ", totalMoves, "steps")
        print()


    #test the code:

    #test solvability
    tryboard1=(7,2,4,5,0,6,8,3,1)
    tryboard2=(4,6,1,2,0,3,7,5,8)
    tryboard3=(1,2,3,4,5,6,8,7,0)

    print("try1", checkSolvable(tryboard1))
    print("try2", checkSolvable(tryboard2))
    print("try3", checkSolvable(tryboard3))

    #generate a certain number of boards, here 100 boards
    start_time = time.time()
    boards100 = generateRandomBoards.createRandomList(100)
    print("boards were generated in ", (time.time() - start_time), " seconds")
    for k in range(len(boards100)):
        print(k+1, " ", boards100[k])

    # print("manhattan", calculateDistanceManhattan(startBoard))
    # print("manhattan2", calculateDistanceManhattan2(startBoard))
    # print("hamming", calculateDistanceHamming(startBoard))
    # print("hamming2", calculateDistanceHamming2(startBoard))
    # print("simple", calculateDistanceSimple(startBoard))
    # print("dist list index", calculateDistanceList(startBoard))
    # print("A* ", calculateDistanceASTAR(startBoard))
    # print()

    #run the puzzlesolver on the created random list

    runPuzzleSolver(boards100, heuristic.ASTAR)
    runPuzzleSolver(boards100, heuristic.Manhattan)
    runPuzzleSolver(boards100, heuristic.Hamming2)

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
    print(distancesList)
    print("und die liste war")
    print(listOfMoves)
    print ()
    #print(pipelineList)
    #print(pipelineList[0])
    #print(pipelineList[1][1])
    #prettyPrint(endBoard)



