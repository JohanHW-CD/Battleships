# This file includes the Mains for the GUI and the UI. It also includes the class for the GUI and functions that bunch
# together functions imported from all other files that should run together.

from functions_battleship import *
from class_board import *
from text_UI import *
from tkinter import *
from tkinter import messagebox

""" --------------------------------------
  Written by: Johan Hedstrand Welander
  Last edited: 2020-12-25
  -------------------------------------- """

class GUI:

    # Constructor:
    def __init__(self, coordinates_of_ships, list_of_sizes):
        # Most variables the GUI needs are made selfs so they don't have to be inputted frequently
        self.root = Tk()  # Initates the GUI
        self.shots_fired = 0
        self.total_hits = 0
        self.player_score = " ..."
        self.coordinates_of_ships = coordinates_of_ships
        self.hit_coordinates = []
        self.lengths_of_alive_ships = list_of_sizes
        self.lengths_of_dead_ships = []  # These last two are used to update the checkbox of alive ships.
        self.username_has_been_inputted = False  # Changes to true when highscores are saved.

    def create_frames(self):
        # Frames are invisible borders in which you can place things. game_frame contains all, board_frame is inside
        # the game_frame containing the board. Ship_info contains checkboxes for the ships.
        self.root.title("Battleships")
        self.game_frame = LabelFrame(self.root, text="Battleships", padx=10, pady=10)
        self.board_frame = LabelFrame(self.game_frame, borderwidth=0, highlightthickness=0)
        self.ship_info_frame = LabelFrame(self.game_frame)
        self.game_frame.pack()
        self.board_frame.grid(row=1, column=1, rowspan=3, )
        self.ship_info_frame.grid(row=1, column=0, padx=10)

    def create_leaderboard(self):
        # imports old high_scores, formats them and places them in a label (a text widget).
        scores = import_high_scores()
        scores_string = format_high_scores_for_GUI(scores)
        highscore_label = Label(self.game_frame, text=scores_string)
        highscore_label.grid(row=1, column=3)

    def display_player_score(self):
        player_score_label = Label(self.game_frame, text="Your hit percentage: " + str(self.player_score) + "%")
        player_score_label.grid(row=4, column=1)

    def create_quit_and_cheat_button(self):
        quit_button = Button(self.game_frame, text="Quit", command=self.quit_gui)
        cheat_button = Button(self.game_frame, text="Cheat", command=self.cheat)
        quit_button.grid(row=6, column=0)
        cheat_button.grid(row=6, column=3)

    def quit_gui(self):
        # Checks if player really wants to quit
        response = messagebox.askyesno("Quit", "Are you sure you want to quit?")
        if response == 1:
            self.root.destroy()
            exit()
        else:
            pass

    def cheat(self):
        # Shows the "True" board (with ships)
        self.create_board(True)
        stop_cheat_button = Button(self.game_frame, text="Stop Cheating", command=self.destroy_and_refresh)
        stop_cheat_button.grid(row=6, column=3)

    def create_list_of_ships(self):
        # Creates inside the frame for info about ships. First creates a heading, then for each ship it creates an
        # non-clickable (DISABLED) checkbutton that is checked in if the ship is dead, else is clear.
        ship_list_heading = Label(self.ship_info_frame, text="Sizes of ships")
        ship_list_heading.pack()
        for length in self.lengths_of_alive_ships:
            c = Checkbutton(self.ship_info_frame, state=DISABLED, text=str(length) + "x1")
            c.pack()
        for length in self.lengths_of_dead_ships:
            c = Checkbutton(self.ship_info_frame, state=DISABLED, text=str(length) + "x1")
            c.pack()
            c.select()

    def system_outputs_and_inputs(self, message):
        # Reacts to inputted messages and places them on the GUI
        if self.username_has_been_inputted == True:  # This means the player has saved their username as a highscore, game is over.
            message = "Thank you for playing"
        elif message == "Only win":  # This structure is just to aid readability when long sentences needs to be messaged
            message = "Congratulations, you won!"
        elif message == "New HS":
            message = "Congratulations! \n You've won and placed on the leaderboard!\nPlease input your name! \n(12 characters max)"
            if self.username_has_been_inputted != True:
                self.request_username_input()
        elif message == "Username try again":
            message = "Make sure your username \n is no longer than 12 characters"
            self.request_username_input()
        system_outputs = Label(self.game_frame, text=message)  # Label displays the message.
        system_outputs.grid(row=2, column=3)

    def request_username_input(self):
        # For when username is needed for saving new highscore, creates a field where player can write and an enter button
        self.input_box = Entry(self.game_frame)
        self.input_box.grid(row=3, column=3)
        enter_box = Button(self.game_frame, text="Enter", command=self.click_enter)
        enter_box.grid(row=4, column=3)

    def click_enter(self):
        # When player presses enter_box. Checks length of username. Either saves or requests new username input.
        username = self.input_box.get()
        if len(username) > 12:
            self.destroy_and_refresh(message="Username try again") #MAKE MORE DESCRIPTIVE
        else:
            save_highscore(self.player_score, username, GUI=True)
            self.username_has_been_inputted = True
            self.destroy_and_refresh(message="Thank you for playing!")

    def create_axes(self):
        # Creates and places a label for each value in the axes.
        for number in range(len(board.get_system())):
            axis_coord = str(number + 1)  # + 1 because range begins on 0 while the game uses 1- coordinates.
            x_axis_label = Label(self.board_frame, text=axis_coord)
            x_axis_label.grid(row=0, column=number + 1)
            y_axis_label = Label(self.board_frame, text=axis_coord)
            y_axis_label.grid(row=number + 1, column=0)

    def create_board(self, real=False):
        # Creates the board, if real == True then it displays the board with all ships visible.
        self.create_axes()
        for i in range(len(board.get_system())):
            for j in range(len(board.get_system())):
                # coordinate = (j, i). It checks what the system has in each coord and creates a button with that symbol
                # fire_and_continue continues the game, destroy_and_refresh simply refreshes the page with the new text.
                if board.get_system()[i][j] == "X" and real == True:
                    ship_button = Button(self.board_frame, text="X", height=1, width=2,
                                         command=lambda y=i, x=j: self.fire_and_continue(x, y))
                    ship_button.grid(row=i + 1, column=j + 1)
                elif board.get_system()[i][j] == "X" and real == False:
                    ship_button = Button(self.board_frame, text=" ", height=1, width=2,
                                         command=lambda y=i, x=j: self.fire_and_continue(x, y))
                    ship_button.grid(row=i + 1, column=j + 1)
                elif board.get_system()[i][j] == "o":
                    shot_button = Button(self.board_frame, text="o", height=1, width=2, command=lambda
                        text="You've already shot there before!": self.destroy_and_refresh(text))
                    shot_button.grid(row=i + 1, column=j + 1)
                elif board.get_system()[i][j] == "#":
                    hit_ship_button = Button(self.board_frame, text="#", height=1, width=2, command=lambda
                        text="You've already shot there before!": self.destroy_and_refresh(text))
                    hit_ship_button.grid(row=i + 1, column=j + 1)
                elif board.get_system()[i][j] == " ":
                    empty_button = Button(self.board_frame, text="", height=1, width=2,
                                          command=lambda y=i, x=j: self.fire_and_continue(x, y))
                    empty_button.grid(row=i + 1, column=j + 1)

    def create_GUI(self, message=" "):
        self.create_frames()
        self.create_list_of_ships()
        self.create_leaderboard()
        self.system_outputs_and_inputs(message)
        self.create_board()
        self.display_player_score()
        self.create_quit_and_cheat_button()

    def update_alive_ships(self, removed_coords):
        # removed_coords are of current sunk ship removed from the list of ship coordinates. First occurrence of this
        # length of a ship is removed from alive ships and added to dead: causes change in list of checkboxes for ships.
        if str(len(removed_coords)) in self.lengths_of_alive_ships:
            self.lengths_of_dead_ships.append(str(len(removed_coords)))
            self.lengths_of_dead_ships.sort(reverse=True)
            self.lengths_of_alive_ships.remove(str(len(removed_coords)))

    def fire_and_continue(self, x, y):
        # Shoots bord with input coordinates, checks for sunk ships and recalculates player_score with consequences.
        hit = board.shoot(x, y)
        message = "Miss!"
        if hit == "Hit!" or hit == "Miss!":
            self.shots_fired += 1
        if hit == "Hit!":
            message = "Hit!"
            self.total_hits += 1
            self.hit_coordinates.append((x, y))
            sunk_ship_index = board.look_for_sunk_ship(self.hit_coordinates, self.coordinates_of_ships)  # Fetches index of ship in list of ship coords if a ship is sunk
            if sunk_ship_index != None:  # If no ship is sunk, look_for_sunk_ship returns None.
                message = "You sank a ship!"
                removed_coords = board.mark_around_sunk_ship(self.coordinates_of_ships, sunk_ship_index)  # Marks area around sunk ship as "shot"
                self.update_alive_ships(removed_coords)
        self.player_score = player_score_calculator(self.total_hits, self.shots_fired)
        if board.end_condition():
            if check_if_new_highscore(self.player_score):
                message = "New HS"
            else:
                message = "Only win"
        self.destroy_and_refresh(message)

    def destroy_and_refresh(self, message=""):
        # Recreates the GUI
        self.game_frame.destroy()
        self.create_GUI(message)


def display_text(score, system, x):
    # Creates the display for the text_based game
    clear_screen()
    present_sizes(import_sizes())
    display_highscores_text()
    present_board(system, x)
    print("Your hit percentage is " + str(score) + "%")


def end_game_text(player_score):
    # Puts together the ending text to make the following function main_text() easier to read
    display_text(player_score, board.get_system(), board.get_x())
    print("You've sunk all ships! Thank you for playing!")
    save_highscore(player_score)
    exit()


def main_text(coordinates_of_ships):
    shots_fired, total_hits, player_score, hit_coordinates = 0, 0, " ...", []
    while True:
        while True:
            display_text(player_score, board.get_system(), board.get_x())
            decision = menu_choice()
            if decision == "1":  # User wants to fire at ships
                user_wants_to_fire = True
                break
            elif decision == "2":  # User wants to see the board, high_score will not be saved after this
                present_board(board.get_system(), board.get_x(), True)
                if want_return_to_main_menu():
                    display_text(player_score, board.get_system(), board.get_x())
                    continue
        while user_wants_to_fire == True:
            display_text(player_score, board.get_system(), board.get_x())
            shot_coords = input_to_shoot()
            hit = board.shoot(shot_coords[0], shot_coords[1])  # Returns None, "outside", "Hit" or "Miss!" None if already shot coordinate is shot.
            if hit == "Hit!" or hit == "Miss!":
                shots_fired = add_one_to_total_shots(shots_fired)
            if hit == "Hit!":
                total_hits = add_one_to_score(total_hits)
                hit_coordinates.append((shot_coords[0], shot_coords[1]))
                sunk_ship_index = board.look_for_sunk_ship(hit_coordinates,
                                                           coordinates_of_ships)  # Fetches index of ship in list of ship coords if a ship is sunk
                board.mark_around_sunk_ship(coordinates_of_ships, sunk_ship_index)  # Marks the area around a sunk ship as "shot"
            player_score = player_score_calculator(total_hits, shots_fired)
            display_text(player_score, board.get_system(), board.get_x())
            announce_result_of_shot(hit, sunk_ship_index=None)
            if board.end_condition():  # Checks if the end condition (all ships have been sunk) is fulfilled
                end_game_text(player_score)
            if not fire_again():
                user_wants_to_fire = False


def main_GUI(coordinates_of_ships, list_of_sizes):
    gui = GUI(coordinates_of_ships, list_of_sizes)
    gui.create_GUI()
    gui.root.mainloop()


def Main(coordinates_of_ships):
    interface = introduction()
    if interface == "G":
        main_GUI(coordinates_of_ships, list_of_sizes)
    elif interface == "T":
        main_text(coordinates_of_ships)


# Initalization
board = Board()
coordinates_of_ships = []
list_of_sizes = import_sizes()
iterations_attempting_to_place_ships = 0
for ship in range(len(list_of_sizes)):
    ship_collision = True  # Assumes ships collide in their placement until tested
    ship_length = board.get_length(list_of_sizes, ship)
    while ship_collision:
        iterations_attempting_to_place_ships = iteration_limit_ship_placement(iterations_attempting_to_place_ships)
        start_coordinates = board.start_coordinate_ship()  # Creates starting_coordinates to place the ship
        direction = board.direction_of_ship(start_coordinates, ship_length)  # Gives legal direction to the ship
        ship_collision = board.collision_check(start_coordinates, ship_length, direction)  # Checks for ship collisions
        if ship_collision == True:
            # If the ship collides, we randomize new starting_coordinates and a new direction and try again
            # Otherwise, the loop breaks and the ship is placed on the board
            continue
        else:
            break
    coordinates_of_ship = board.place_ships(start_coordinates, ship_length, direction)
    coordinates_of_ships.append(
        coordinates_of_ship)  # Appends the placed coordinates to a list containing all ship's coordinates.

Main(coordinates_of_ships)
