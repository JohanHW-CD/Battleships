# Here will be all functions dealing with purely text-based user interface.
import os


def introduction():
    # Introduces the game and user decides on text-based or GUI game.
    print("""Welcome to Battleships! \n
on the other side of this screen there are enemy flagships wanting to hack your computer \n
the solution? To find their coordinates and attack them!!! \n
Below are three options, command is your cap' \n""")
    response = (input("Do you want to play text-based or with GUI? [T/G]")).upper()
    while True:
        if response != "T" and response != "G":
            response = (input("Please be sure to input 'T' or 'G'")).upper()
        else:
            break
    return response


def present_board(system, x, real=False):
    # If real = True: the real board is displayed, else a board without the ships are shown.
    # Below are iterations to make the chess-like pattern given the coordinate system of the board.
    print(" ", end="")
    for i in range(len(system)):
        print("   " + str(i + 1), end="  ")
    print("")
    print("  " + "------" * (x + 1))

    for i in range(len(system)):
        print(str(i + 1) + "|", end="")
        for j in range(len(system)):
            if system[i][j] == "X" and real == False:
                print("  " + " " + "  |", end="")
            else:
                print("  " + system[i][j] + "  |", end="")
        print("")
        print("  " + "------" * (x + 1))


def input_to_shoot():
    # Requests the coordinates of which to shoot. Error handles these simultaneously.
    while True:
        try:
            shoot_y = int(
                input("Fire at what y-coordinate?")) - 1  # -1 because lists are 0-7 but users like 1-8 coordinates.
            shoot_x = int(input("Fire at what x-coordinate?")) - 1
            return (shoot_x, shoot_y)
        except:
            print("You need to input integers")


def fire_again():
    # Gives the option to shoot more or return to the main menu
    while True:
        response = (input("Do you want to shoot more? (Y/N)")).upper()
        if response == "Y":
            return True
        elif response == "N":
            return False
        else:
            print("Make sure to answer with 'Y' or 'N'")


def announce_result_of_shot(shoot, sunk_ship_index):
    if sunk_ship_index != None:
        print("You sank a ship!")
    elif shoot == "Hit!":
        print("That's a hit!")
    elif shoot == "Miss!":
        print("Miss!")
    elif shoot == None:
        print("You've already shot there before!")
    elif shoot == "Outside":
        print("You shot outside of the border! Try again!")


def present_sizes(list_of_sizes):
    # Prints a string stating the sizes of all ships in the beginning of the game
    presentation = "The ships in beginning of the game are of the lengths: "
    for size in list_of_sizes:
        presentation += str(size) + "x1, "
    print(presentation)


def want_return_to_main_menu():
    while True:
        response = (input("Ready to return to the main menu? [Y]")).upper()
        if response == "Y":
            return True
        else:
            print("Make sure to answer with 'Y' when ready")


def clear_screen():
    print("\n" * 60)  # in case the user does not use the CMD this will make it look cleared
    os.system('cls')  # Clears the terminal


def print_menu() -> str:
    # Prints menu and allows selection
    decision = input("""1. Fire!
2. Cheat a little (Look at the opponents board))
3. Quit""")
    return decision


def menu_choice():
    # Displays the menu and responds to selections. Error handles inputs.
    decision = print_menu()
    while True:
        if decision == "3":  # User wants to quit
            if check_quitting():  # Double checks if player wants to quit
                exit()
            else:
                break
        elif decision == "2" or decision == "1":
            return decision  # "2" and "1" are treated in Main()
        else:
            print("Make sure you input 1, 2, or 3 to select your option", end="")
            decision = input(" ")


def check_quitting():
    # Double checks if player wants to quit. Returning True kills game. Returning False moves user to main menu.
    while True:
        user_input = (input("Are you sure you want to quit? [Y/N]")).upper()
        if user_input == "Y":
            return True
        elif user_input == "N":
            return False
        else:
            print("Y = yes and N = no")
