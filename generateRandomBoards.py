import random

# from https://www.tutorialspoint.com/How-to-generate-non-repeating-random-numbers-in-Python on 1.2.24 20:00

def createRandomBoard():
    # resultant random numbers list
    randomBoard = []
    # traversing the loop 9 times
    i = 0
    while i < 9:
        # generating a random number in the range 0 to 8
        r = random.randint(0, 8)
        # checking whether the generated random number is not in the randomList
        if r not in randomBoard:
            # appending the random number to the resultant list, if the condition is true
            randomBoard.append(r)
            i = i + 1
    # printing the resultant random numbers list to tupel
    return tuple(randomBoard)


def createRandomList():
    list = []
    i = 0
    while i < 100:
        new = createRandomBoard()
        if new not in list:
            list.append(new)
            i = i + 1
    return list

