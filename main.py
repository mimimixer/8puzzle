# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from scipy.spatial.distance import hamming
from scipy.spatial.distance import cityblock
import time
import generateRandomBoards



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    def readBoard():
        start = int(input("Enter board row by row like 123456780: "))
        startBoard = (int(start/100000000), int((start/10000000)%10), int((start/1000000)%10), int((start/100000)%10), int((start/10000)%10),
                      int((start/1000)%10), int(start/100%10), int((start/10)%10), int(start%10))
        return startBoard
    #second_row = int(input("Enter second row: "))
    #third_row = int(input("Enter third row: "))
    #startBoard = readBoard()
    endBoard = (1,2,3,4,5,6,7,8,0)
    #endBoard = (0,1,2,3,4,5,6,7,8)



    def calculateDistanceManhattan(board):
        dist = 0
        for i in range (len(board)):
            element = board[i]
            if element != 0:
                shouldBe = endBoard.index(element)
                distRow = int(shouldBe/3)-int(i/3)
                distCol = shouldBe%3-i%3
                dist = dist + abs(distCol)+abs(distRow)
        return dist

    def calculateDistanceManhattan2(board):
        return cityblock(board, endBoard)

    def calculateDistanceHamming(board):
        dist = 0
        for i in range (len(board)):
            element = board[i]
            if element != 0:
                shouldBe = endBoard.index(element)
                if i != shouldBe:
                    dist = dist +1
        return dist

    def calculateDistanceHamming2(board):
        return hamming(board, endBoard)*len(board)

    def calculateDistanceSimple(board):
        dist = 0
        for i in range (len(board)):
            dist = dist + abs(endBoard[i]-board[i])
        return dist

    def calculateDistanceList(board):
        dist = 0
        for i in range (len(board)):
            element = board[i]
            dist = dist + abs(endBoard.index(element)-i)
        return dist

    def calculateDistanceASTAR(board):
        dist = 0
        for i in range (len(board)):
            element = board[i]
            if element != 0:
                shouldBe = endBoard.index(element)
                distRow = shouldBe/3-i/3
                distCol = shouldBe%3-i%3
                dist = dist + int(abs((distCol)+int(distRow))*1.2)
        return dist

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
    listOfMoves = []
    pipelineList = []
    distancesList = []
    #[[startBoard,calculateDistance(startBoard)]]

# 724506831
# 461203758
    def addToPipeline(pipelineList, board, heuristics):
        if board in listOfMoves:
            return
        dist = heuristics(board)
        if pipelineList:
            for i in range (len(pipelineList)):
                if pipelineList[i][1] > dist:
                    pipelineList.insert(i, [board, dist])
                    return pipelineList
        pipelineList.append([board, dist])
        return pipelineList

    def swap(board, x, y):
        tmp=[]
        tmp = list(x for x in board)
        tmp[x] = board [y]
        tmp[y] = board [x]
        return tuple(tmp)

    def searchStep(pipelineList, heuristics):
        board = pipelineList[0][0]
        #prettyPrint(board)
        #print(pipelineList[0][1])
        #print()
        listOfMoves.append(board)
        distancesList.append(pipelineList[0][1])
        pipelineList.pop(0)
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


    def prettyPrint(board):
        for i in range(3):
            for j in range(3):
                print(board[i*3+j], end = " ")
                if j == 2:
                    print()

    def slide(start, heuristic):
        counter=0
        addToPipeline(pipelineList, start, heuristic)
        searchStep(pipelineList, heuristic)
        while listOfMoves[-1] != endBoard and counter < 10000:
            searchStep(pipelineList, heuristic)
            counter = counter+1
        if len(listOfMoves) > 10000:
            print("already ", counter, "moves done, stopping search")
            return
        else:
            print("found after ", len(listOfMoves)-1, "moves")

    def clearLists():
        listOfMoves.clear()
        pipelineList.clear()
        distancesList.clear()
    #listOfMoves.append(endBoard)
    #addToPipeline(pipelineList,startBoard)
    #addToPipeline(pipelineList, endBoard)

    def checkSolvable(board):
        solv=0
        for i in range(len(board)):
            if board[i] != 0:
                for j in range(i, len(board)):
                    if board[j] != 0:
                        if board[j] < board[i]:
                            solv = solv +1
        return solv

    tryboard1=(7,2,4,5,0,6,8,3,1)
    tryboard2=(4,6,1,2,0,3,7,5,8)
    tryboard3=(1,2,3,4,5,6,8,7,0)

    print("try1", checkSolvable(tryboard1))
    print("try2", checkSolvable(tryboard2))
    print("try3", checkSolvable(tryboard3))


    start_time = time.time()
    boards100 = generateRandomBoards.createRandomList()
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

    def runPuzzleSolver(list, heuristic):
        start_time = time.time()
        unsolvable=0
        for k in range(len(list)):
            print(k)
            startBoard = list[k]
            if checkSolvable(startBoard)%2 == 0:
                slide(startBoard, heuristic)
                clearLists()
            else:
                unsolvable=unsolvable+1
        print(unsolvable, " unsolvable puzzles found")
        print(heuristic.__name__, " solution for the other ", 100-unsolvable, "puzzles found in", (time.time() - start_time), " seconds")
        print()

    runPuzzleSolver(boards100, calculateDistanceASTAR)
    runPuzzleSolver(boards100, calculateDistanceManhattan)
    runPuzzleSolver(boards100, calculateDistanceHamming2)

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



