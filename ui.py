from tqdm import tqdm
from time import sleep
#ToDo:
    # diagramme draw.io -> Angabe schauen
    # Moritz mein FinalProtocol in Neta schicken
class Loading():

    def loading_bar(self):
        results = []
        heuristic = Loading()
        bar = tqdm(range(0, 100), total=100, desc="Loadig...")
        for i in bar:
            if self.display_heuristic(0, results):
                sleep(.1)
            elif self.display_heuristic(1, results):
                sleep(.1)
            elif self.display_heuristic(2, results):
                sleep(.1)
            if i == len(bar)-1:
                bar.set_description(desc="Loaded successfully")
            sleep(.1)


    def heuristic_options(self):
        results = []
        heuristic = Loading()
        print("")
        print("        Choose a heuristic")
        print("    'H'   ", end="")
        print("      'M'    ", end="")
        print("   'aS'    ")
        print(" [Hamming] ", end="")
        print(" [Manhattan] ", end="")
        print(" [aStar] ")
        print("")
        valid = False
        while not valid:
            print("If you want to exit, enter 'exit'.")
            print("Please enter your heuristic (H or M or aS): ", end="")
            heuristic_value = input()
            if heuristic_value == "H":
                heuristic.display_heuristic(2, results)
                valid = True
            elif heuristic_value == "M":
                heuristic.display_heuristic(1, results)
                valid = True
            elif heuristic_value == "aS":
                heuristic.display_heuristic(0, results)
                valid = True
            elif heuristic_value == "exit":
                valid = True
            else:
                print("Input is invalid. Please try again.")

    def display_heuristic(self, heuristic_index, results):
        heuristic = Loading()
        if results == []:
            #print("tada")
            return
        result = results[heuristic_index]
        for index in range(len(result)):
            if result[index][0] == None:
                print(result[index][1], "unsolvable puzzles found.")
                print("It took", result[index][2], "seconds to find all solutions.")
                print("\n")
            elif result[index][0] == "unsolvable":
                print(str(index + 1), "unsolvable")
                print()
            else:
                print(str(index + 1), "Solution was found after", result[index][1], "moves were looked at.")
                print("Fastest solution took", result[index][0].steps, "moves.")
                print()
        valid = False
        while not valid:
            print("If you want more information on a specific solve, please enter its number.")
            print("If you want to exit, please enter \"exit\".")
            choice = input()
            if choice == "exit":
                self.heuristic_options()
            elif choice.isdigit():
                choice = int(choice)
                if 0 < choice <= 100:
                    print("Chosen solution", str(choice))
                    print()

                    path = []
                    board_wrapper = result[choice - 1][0]
                    current = board_wrapper
                    while current.previous != None:
                        path.append(current.board)
                        current = current.previous
                    path = path[::-1]
                    c=1
                    for i in path:
                        print("Step", str(c) + ":", i)

                print("If you want to exit, please enter \"exit\".")
                heuristic.display_heuristic(heuristic_index, results)

    def pretty_print(self, board):  # method for printing board in 3 rows
        for i in range(3):
            for j in range(3):
                print(board[i * 3 + j], end=" ")
                if j == 2:
                    print()


if __name__ == "__main__":
    loading = Loading()
    loading.loading_bar()
    loading.heuristic_options()
