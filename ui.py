import puzzleSolver

class Loading:

    def start(self): #acts like a homescreen
        puzzle = puzzleSolver
        try:
            num_of_boards = int(
                input("Hello, how many boards would you like to have solved?[1-1000] ").replace(" ", ""))
        #user can choose how many boards should be displayed
        except:
            num_of_boards = 0
        while not (1 <= num_of_boards <= 1000):
            try:
                num_of_boards = int(
                    input("Your input was invalid, how many boards would you like to have solved?[1-1000] ").replace(
                        " ", ""))
                #if input is invalid user is in while loop
            except:
                pass
        valid_before = False
        while not valid_before:
            print("Do you want to load all Heuristics [all] or just a specific one [specific]? ", end="")
            heuristic_value = input().replace(" ", "")
            #user has the option to list all or a specific heuristic
            if heuristic_value == "all":
                puzzle.handle_start("H&M&aS", num_of_boards)
                valid_before = True
                #if input is all then call handle_start
            elif heuristic_value == "specific":
                valid_before = True
                #if input is specific as which heuristic should be displayed
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
                        #if input is one of the heuristics then call handle_start method with input and number of boards
                    elif heuristic_value == "exit":
                        valid = True
                        #if input is exit then end while loop
                    else:
                        print("Input is invalid. Please try again.")
                        #input was invalid - user has to enter a valid input

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
        #prints informs user what to enter for the specific heuristics
        valid = False
        while not valid:
            print("If you want to exit, enter 'exit'.  If you want to start again enter 'start'.")
            heuristic_value = input("Please enter your heuristic (H or M or aS): ").replace(" ", "")
            #user can choose between different heuristic
            if heuristic_value == "H":
                valid = ui.display_heuristic(2, results)
            elif heuristic_value == "M":
                valid = ui.display_heuristic(1, results)
            elif heuristic_value == "aS":
                valid = ui.display_heuristic(0, results)
                #with every heuristic call display method with suitable index
            elif heuristic_value == "exit":
                print("Thanks for trying this program!")
                exit()
                #when use types exit, end ui
            elif heuristic_value == "start":
                self.start()
                #when start is typed then call start method
            else:
                print("Input is invalid. Please try again.")
            #user is in while loop until the input is valid
    def display_heuristic(self, heuristic_index, results):
        if results[heuristic_index]: #if there is a heuristic execute if statement
            ui = Loading()
            result = results[heuristic_index]
            avg_nodes = 0
            avg_time = 0
            variance_nodes = 0
            variance_time = 0
            c = 0
            #set all values
            for res in result:
                if res[0]: #if there is a heuristic execute if statement
                    c += 1
                    avg_nodes += res[1] #caclulate average nodes
                    avg_time += res[2] #calculate average time
            avg_nodes = avg_nodes / c #average nodes divided by steps
            avg_time = avg_time / c #average time divided by steps

            for res in result:
                if res[0]:  # if there is a heuristic execute if statement

                    variance_nodes += ((res[1] - avg_nodes) ** 2) # caclulate difference nodes to average ^2
                    variance_time += ((res[2] - avg_time) ** 2)  # calculate difference time to average ^2
            variance_nodes = variance_nodes / (c - 1)
            variance_time = variance_time / (c - 1)
            standard_deviation_nodes = variance_nodes ** 0.5
            standard_deviation_time = variance_time ** 0.5

            for index in range(len(result)):
                if result[index][0] == None: #if puzzle is unsolvable print following information
                    print(result[index][1], "unsolvable puzzles found.")
                    print("It took", result[index][2], "seconds to find all solutions.")
                    print("On average it took", "{:.1f}".format(avg_nodes), "nodes and", "{:.3f}".format(avg_time),
                          "seconds to find one solution, with \na variance of", "{:.1f}".format(variance_nodes), "nodes with a standard deviaton of", "{:.1f}".format(standard_deviation_nodes),
                          "nodes, and \na variance of", "{:.3f}".format(variance_time), "seconds and a standard deviation of", "{:.3f}".format(standard_deviation_time), "seconds.")
                    print("\n")
                else: #if puzzle is solvable print the following information
                    print(str(index + 1), "solutions were found after", result[index][1], "nodes were looked at.")
                    print("Fastest solution took", result[index][0].steps, "moves.")
                    print()
            valid = False

            print("If you want more information on a specific solution, please enter its number.")
            print("If you want to exit, please enter \"exit\".")
            #user has option to inspect a specific board
            choice = input().replace(" ", "")
            if choice == "exit":
                ui.heuristic_options(results)
                valid = True
                #user can exit and heuristic_option method is called to do so
            while not valid:
                if choice == "exit":
                    ui.display_heuristic(heuristic_index, results)
                elif choice.isdigit():
                    choice = int(choice)
                    if 0 < choice <= len(result): #is input choice in range
                        print("Chosen solution", str(choice))
                        print()
                        #information which board was chosen
                        path = [] #clear path
                        board_wrapper = result[choice - 1][0]
                        current = board_wrapper
                        while current.previous_board:
                            path.append(current.board) #store information about the board
                            current = current.previous_board
                            #reverse the order of the path to be in the correct sequence
                        path = path[::-1]
                        c = 1
                        #iterate through the path and print each step
                        for i in path:
                            a = ""
                            if c <= 9:
                                a = " "
                            print("Step", str(c) + ":" + a)
                            ui.pretty_print(i) #display the board
                            c += 1 #increase step counter

                        print("This solution took", result[choice - 1][2], "seconds and", result[choice - 1][1],
                              "nodes to compute.")
                print("If you want more information on a specific solution, please enter its number.")
                print("If you want to exit, please enter \"exit\".")
                choice = input().replace(" ", "")
                #user gets information and can choose another board or exit
                if choice == "exit":
                    valid = True
                    ui.display_heuristic(heuristic_index, results)
                    #if user wants to exit call display method
        else:
            print("Please select a different Heuristic as this one wasn't computed.")
            #if user want to execute a "false" heuristic
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
