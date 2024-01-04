#calculateDistance

#import puzzleSolver
from scipy.spatial.distance import hamming
from scipy.spatial.distance import cityblock

#endBoard = puzzleSolver.endBoard

def Manhattan(board, endBoard):
    dist = 0
    for i in range (len(board)):
        element = board[i]
        if element != 0:
            shouldBe = endBoard.index(element)
            distRow = int(shouldBe/3)-int(i/3)
            distCol = shouldBe%3-i%3
            dist = dist + abs(distCol)+abs(distRow)
    return dist

def Manhattan2(board, endBoard):
    return cityblock(board, endBoard)

def Hamming(board,endBoard):
    dist = 0
    for i in range (len(board)):
        element = board[i]
        if element != 0:
            shouldBe = endBoard.index(element)
            if i != shouldBe:
                dist = dist +1
    return dist

def Hamming2(board,endBoard):
    return hamming(board, endBoard)*len(board)

def calculateDistanceSimple(board,endBoard):
    dist = 0
    for i in range (len(board)):
        dist = dist + abs(endBoard[i]-board[i])
    return dist

def calculateDistanceList(board,endBoard):
    dist = 0
    for i in range (len(board)):
        element = board[i]
        dist = dist + abs(endBoard.index(element)-i)
    return dist

def ASTAR(board,endBoard):
    dist = 0
    for i in range (len(board)):
        element = board[i]
        if element != 0:
            shouldBe = endBoard.index(element)
            distRow = shouldBe/3-i/3
            distCol = shouldBe%3-i%3
            dist = dist + int(abs((distCol)+int(distRow))*1.2)
    return dist