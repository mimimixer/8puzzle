import puzzleSolver


#ToDo:
# diagramme draw.io -> Angabe schauen


class Loading:

    def start(self):
        puzzle = puzzleSolver
        try:
            num_of_boards = int(
                input("Hello, how many boards would you like to have solved?[1-1000] ").replace(" ", ""))
        except:
            num_of_boards = 0
        while not (1 <= num_of_boards <= 1000):
            try:
                num_of_boards = int(
                    input("Your input was invalid, how many boards would you like to have solved?[1-1000] ").replace(
                        " ", ""))
            except:
                pass
        valid_before = False
        while not valid_before:
            print("Do you want to load all Heuristics [all] or just a specific one [specific]? ", end="")
            heuristic_value = input().replace(" ", "")
            if heuristic_value == "all":
                puzzle.handle_start("H&M&aS", num_of_boards)
                valid_before = True
            elif heuristic_value == "specific":
                valid_before = True
                print()
                print("H = Hamming, M = Manhattan, aS = aStar")
                valid = False
                input_choice = ["H", "M", "aS", "H&M", "H&aS", "M&aS", "H&M&aS"]
                while not valid:
                    print("If you want to exit, enter 'exit'.")
                    print("Please enter your heuristic [H/M/aS/H&M/H&aS/M&aS/H&M&aS]: ", end="")
                    heuristic_value = input().replace(" ", "")
                    if heuristic_value in input_choice:
                        puzzle.handle_start(heuristic_value, num_of_boards)
                        valid = True
                    elif heuristic_value == "exit":
                        valid = True
                    else:
                        print("Input is invalid. Please try again.")

    def heuristic_options(self, results):
        ui = Loading()
        print()
        print("        Choose a heuristic")
        print("    'H'   ", end="")
        print("      'M'    ", end="")
        print("   'aS'    ")
        print(" [Hamming] ", end="")
        print(" [Manhattan] ", end="")
        print(" [aStar] ")
        print()
        valid = False
        while not valid:
            print("If you want to exit, enter 'exit'.  If you want to start again enter 'start'.")
            heuristic_value = input("Please enter your heuristic (H or M or aS): ").replace(" ", "")
            if heuristic_value == "H":
                valid = ui.display_heuristic(2, results)
            elif heuristic_value == "M":
                valid = ui.display_heuristic(1, results)
            elif heuristic_value == "aS":
                valid = ui.display_heuristic(0, results)
            elif heuristic_value == "exit":
                print("Thanks for trying this program!")
                exit()
            elif heuristic_value == "start":
                self.start()
            else:
                print("Input is invalid. Please try again.")

    def display_heuristic(self, heuristic_index, results):
        if results[heuristic_index]:
            ui = Loading()
            result = results[heuristic_index]
            avg_nodes = 0
            avg_time = 0
            max_nodes = 0
            min_nodes = 19000000
            min_time = 1000000
            max_time = 0
            c = 0
            for res in result:
                if res[0]:
                    c += 1
                    min_nodes = min(min_nodes, res[1])
                    max_nodes = max(max_nodes, res[1])

                    min_time = min(min_time, res[2])
                    max_time = max(max_time, res[2])

                    avg_nodes += res[1]
                    avg_time += res[2]
            avg_nodes = avg_nodes / c
            avg_time = avg_time / c

            variance_nodes = max(abs(min_nodes - avg_nodes), abs(max_nodes - avg_nodes))
            variance_time = max(abs(min_time - avg_time), abs(max_time - avg_time))

            for index in range(len(result)):
                if result[index][0] == None:
                    print(result[index][1], "unsolvable puzzles found.")
                    print("It took", result[index][2], "seconds to find all solutions.")
                    print("On average it took", avg_nodes, "nodes and", avg_time,
                          "seconds to find one solution, with a variance of", variance_nodes, "nodes and",
                          variance_time,
                          "seconds.")
                    print("\n")
                else:
                    print(str(index + 1), "Solution was found after", result[index][1], "nodes were looked at.")
                    print("Fastest solution took", result[index][0].steps, "moves.")
                    print()
            valid = False

            print("If you want more information on a specific solve, please enter its number.")
            print("If you want to exit, please enter \"exit\".")

            choice = input().replace(" ", "")
            if choice == "exit":
                ui.heuristic_options(results)
                valid = True
            while not valid:
                if choice == "exit":
                    ui.display_heuristic(heuristic_index, results)
                elif choice.isdigit():
                    choice = int(choice)
                    if 0 < choice <= len(result):
                        print("Chosen solution", str(choice))
                        print()

                        path = []
                        board_wrapper = result[choice - 1][0]
                        current = board_wrapper
                        while current.previous_board:
                            path.append(current.board)
                            current = current.previous_board
                        path = path[::-1]
                        c = 1
                        for i in path:
                            a = ""
                            if c <= 9:
                                a = " "
                            print("Step", str(c) + ":" + a)
                            ui.pretty_print(i)
                            c += 1

                        print("This solution took", result[choice - 1][2], "seconds and", result[choice - 1][1],
                              "nodes to compute.")
                print("If you want more information on a specific solve, please enter its number.")
                print("If you want to exit, please enter \"exit\".")
                choice = input().replace(" ", "")
                if choice == "exit":
                    valid = True
                    ui.display_heuristic(heuristic_index, results)
        else:
            print("Please select a different Heuristic as this one wasn't computed.")
            return False
        return True

    def pretty_print(self, board):  # method for printing board in 3 rows
        for i in range(3):
            for j in range(3):
                print(board[i * 3 + j], end=" ")
                if j == 2:
                    print()


if __name__ == "__main__":
    # with open("test_data.json", "rb") as file:
    # results = pickle.load(file)
    # print(results)
    """result = puzzleSolver.handle_start("M", 100)
    path = "result_data" + str(4) + ".json"
    print(path)
    with open(path, "wb") as file:
        pickle.dump(result, file, pickle.HIGHEST_PROTOCOL)
        file.close()"""
    loading = Loading()
    loading.start()
    # loading.loading_bar()
    # loading.heuristic_options(results)
