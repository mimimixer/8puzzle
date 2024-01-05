import time


def read_board():
    start = int(input("Enter board row by row like 123456780: "))
    startBoard = (
    int(start / 100000000), int((start / 10000000) % 10), int((start / 1000000) % 10), int((start / 100000) % 10),
    int((start / 10000) % 10),
    int((start / 1000) % 10), int(start / 100 % 10), int((start / 10) % 10), int(start % 10))
    return startBoard
# second_row = int(input("Enter second row: "))
# third_row = int(input("Enter third row: "))
# startBoard = readBoard()


if __name__ == "__main__":
    start = time.time()
    for i in range(100000000):
        pass
    print("for loop duration", time.time()-start)
    start = time.time()
    i=0
    while i <100000000:
        i+=1
    print("while loop duration", time.time()-start)