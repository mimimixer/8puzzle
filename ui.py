import math
from tqdm import tqdm
from time import sleep
import pickle
import puzzleSolver
import os


# ToDo:
# diagramme draw.io -> Angabe schauen
# Moritz mein FinalProtocol in Neta schicken


class Loading():

    """ def loading_bar(self):
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
            if i == len(bar) - 1:
                bar.set_description(desc="Loaded successfully")
            sleep(.1)"""

    def start(self):    #UI to display different heuristics
        heuristic = Loading()
        puzzle = puzzleSolver
        try:
            num_of_boards = int(
                input("Hello, how many boards would you like to have solved?[1-1000] ").replace(" ", ""))
        except: #ask user how many board should be solved, however 0 is not option, as you have to display at least one board
            num_of_boards = 0
        while not (1 <= num_of_boards <= 1000): #if input was smaller than zero or higher than one thousand boards, you get redirected
            try: #while loop ends as soon as the input is valid
                num_of_boards = int(
                    input("Your input was invalid, how many boards would you like to have solved?[1-1000] ").replace(
                        " ", ""))
            except:
                pass
        valid_before = False
        while not valid_before:
            print("Do you want to load all Heuristics [all] or just a specific one [specific]? ", end="")
            heuristic_value = input().replace(" ", "") #ask if user wants to display all heuristics or just a specific
            if heuristic_value == "all": #display all heuristics
                puzzle.handle_start("H&M&aS", num_of_boards)
                valid_before = True #set valid true so that while loop ends
            elif heuristic_value == "specific": #ony display a specific heuristic
                valid_before = True
                print("")
                print("H = Hamming, M = Manhattan, aS = aStar")
                valid = False
                input_choice = ["H", "M", "aS", "H&M", "H&aS", "M&aS", "H&M&aS"]
                while not valid:
                    print("If you want to exit, enter 'exit'.")

                    print("Please enter your heuristic [H/M/aS/H&M/H&aS/M&aS/H&M&aS]: ", end="") #ask which one should be displayed
                    heuristic_value = input().replace(" ", "") # a combination of more than one heuristic can be made
                    if heuristic_value in input_choice:
                        puzzle.handle_start(heuristic_value, num_of_boards) #call handle_start function in puzzlesolver
                        valid = True
                    elif heuristic_value == "exit": #possability to exit while loop without displaying a heuristic
                        valid = True
                    else:
                        print("Input is invalid. Please try again.") #input invalid


    def heuristic_options(self, results):
        heuristic = Loading()
        print("")
        print("")
        print("        Choose a heuristic")
        print("    'H'   ", end="")
        print("      'M'    ", end="")
        print("   'aS'    ")
        print(" [Hamming] ", end="")
        print(" [Manhattan] ", end="")
        print(" [aStar] ")
        print("") #prints for layout purposes
        valid = False
        while not valid:
            print("If you want to exit, enter 'exit'.  If you want to start again enter 'start'.")
            print("Please enter your heuristic (H or M or aS): ", end="") #which heuristic should be displayed
            heuristic_value = input().replace(" ", "")
            if heuristic_value == "H": #calls display method to display correct heuristic
                valid = heuristic.display_heuristic(2, results)
            elif heuristic_value == "M":
                valid = heuristic.display_heuristic(1, results)
            elif heuristic_value == "aS":
                valid = heuristic.display_heuristic(0, results)
            elif heuristic_value == "exit":
                print("Thanks for trying this program!")
                exit()
            elif heuristic_value == "start": #if input = 'start' then call start method
                self.start()
            else:
                print("Input is invalid. Please try again.") #input is invalid

    def display_heuristic(self, heuristic_index, results):
        if results[heuristic_index]: #if results inclued a heuristic
            heuristic = Loading()
            result = results[heuristic_index]
            avg_nodes = 0
            avg_time = 0
            max_nodes = 0
            min_nodes = 190000
            min_time = 1000000  #set range
            max_time = 0
            c = 0
            for res in result: #go through results
                if res[0]:
                    c += 1 #increase counter/steps
                    min_nodes = min(min_nodes, res[1]) #set min nodes
                    max_nodes = max(max_nodes, res[1]) #set max nodes

                    min_time = min(min_time, res[2]) #set min time
                    max_time = max(max_time, res[2]) #set max time

                    avg_nodes += res[1] #add nodes to average
                    avg_time += res[2] #add time to average
            avg_nodes = avg_nodes / c #calculate nodes by dividing by step
            avg_time = avg_time / c #calculate time by dividing by step

            variance_nodes = max(abs(min_nodes - avg_nodes), abs(max_nodes - avg_nodes)) #calculate nodes
            variance_time = max(abs(min_time - avg_time), abs(max_time - avg_time)) #calculate time

            for index in range(len(result)): #iterates over each element in list
                if result[index][0] == None: #if index is "none" then puzzle is unsolvable
                    print(result[index][1], "unsolvable puzzles found.")
                    print("It took", result[index][2], "seconds to find all solutions.")
                    print("On average it took", avg_nodes, "nodes and", avg_time,
                          "seconds to find one solution, with a variance of", variance_nodes, "nodes and",
                          variance_time,
                          "seconds.")
                    print("\n") #all prints inform user with information
                elif result[index][0] == "unsolvable": #first value of index is unsolvable
                    print(str(index + 1), "unsolvable")
                    print()
                else: #go to next index if its solvable
                    print(str(index + 1), "Solution was found after", result[index][1], "nodes were looked at.")
                    print("Fastest solution took", result[index][0].steps, "moves.")
                    print()
            valid = False

            print("If you want more information on a specific solve, please enter its number.")
            print("If you want to exit, please enter \"exit\".")
            choice = input().replace(" ", "")
            if choice == "exit":
                valid = True
                heuristic.heuristic_options(results) #if user wants to exit call heuristic options
            while not valid:
                if choice == "exit":
                    heuristic.display_heuristic(heuristic_index, results)
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
                            heuristic.pretty_print(i)
                            c += 1

                        print("This solution took", result[choice - 1][2], "seconds and", result[choice - 1][1],
                              "nodes to compute.")

                print("If you want more information on a specific solve, please enter its number.")
                print("If you want to exit, please enter \"exit\".")
                choice = input().replace(" ", "")
                heuristic.display_heuristic(heuristic_index, results)
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
    """for i in range(100000):
        result = puzzleSolver.handle_start("HMaS", 100)
        path = "result_datt" + str(i) + ".json"
        with open(path, "wb") as file:
            pickle.dump(result, file, pickle.HIGHEST_PROTOCOL)"""
    loading = Loading()
    loading.start()
    # loading.loading_bar()
    # loading.heuristic_options(results)
