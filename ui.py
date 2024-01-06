from tqdm import tqdm

#ToDo:
    # diagramme draw.io -> Angabe schauen
    # Moritz mein FinalProtocol in Neta schicken
class Loading():

    def loading_bar(self):
        for i in tqdm(range(100), desc="Loadig..."):
            pass

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
            print("Please enter your heuristic (H or M or aS): ", end="")
            heuristic_value = input()
            print()
            print("If you want to exit, please type 'exit'.")
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
            print("tada")
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
                heuristic_options()
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


if __name__ == "__main__":
    loading = Loading()
    # loading.loading_bar()
    loading.heuristic_options()
