# Functions that deal with importing modules and high scores.


def import_sizes():
    # Reads a text file containing the predetermined ships' sizes, returns these as list
    file = open("sizes.txt", "r+")
    ship_sizes_string = file.read()
    list_ship_sizes = ship_sizes_string.split(" ")
    return list_ship_sizes


def import_high_scores() -> list:
    # reads saved high scores in a text file and returns all in one list
    file = open("high_scores_stored.txt", "r+")
    high_scores_string = file.read()
    list_high_scores = high_scores_string.split(",")
    file.close()
    return list_high_scores


def display_highscores_text():
    # Displays imported saved high scores
    high_scores = import_high_scores()
    print("LEADER BOARD")
    for i in range(len(high_scores)):
        print(str(i + 1) + ": " + high_scores[i] + "%")
    print("")


def request_new_highscore_text(i, player_score):
    # Asks for the username of the player then formats it for the high_score_stored file text file.
    username = input("""Congratulations! You made it onto the leaderboard!
Write your name (max 12 characters) to save your achievement! 
you placed: """ + str(i + 1) + "st/th")
    while True:
        if len(username) > 12:
            username = input("Make sure your username is less than 13 characters")
        elif len(username) <= 12:
            break
    high_score_to_save = format_new_highscore_string(username, player_score)
    return high_score_to_save


def format_new_highscore_string(username, player_score):
    # Takes inputted username and score and formats for saving.
    high_score_to_save = username + " -  " + str(player_score)
    return high_score_to_save


def format_high_scores_for_GUI(list_high_scores) -> str:
    # Format highscores that should be displayed for the GUI
    GUI_scores = "LEADER BOARD\n\n"
    for i in range(len(list_high_scores)):
        GUI_scores = GUI_scores + (str(i + 1) + ": " + list_high_scores[i] + "%\n")  # Creates "number:  name \n"
    return GUI_scores


def player_score_calculator(total_hits: int, shots_fired: int) -> float:
    # Calculates player's hit rate in percentage. Returns 0 if shots_fired is 0.
    if shots_fired != 0:
        percentage = round((total_hits / shots_fired) * 100, 1)
        return percentage
    else:
        return 0


def add_one_to_score(total_hits):
    total_hits += 1
    return total_hits


def add_one_to_total_shots(shots_fired):
    shots_fired += 1
    return shots_fired


def check_if_new_highscore(player_score: float):
    # Returns True if the player's score when game is completed is higher than any of the old high scores.
    high_scores = import_high_scores()  # list of old high_scores
    last_index = len(
        high_scores) - 1  # The index of the last element in the list high_scores. AKA the worst high score.
    lowest_score = float(
        high_scores[last_index - 1][-5:])  # The [-5:] is to reach the digits part in the stored strings.
    if player_score > lowest_score:
        return True
    else:
        return False


def save_highscore(player_score, username=None, GUI=None):
    # This function saves a player's score at the correct ordinal number in the high score storage file.
    high_scores = import_high_scores()  # list of old high_scores
    for i in range(0, len(high_scores)):
        if float(high_scores[i][-5:]) < float(player_score):
            # Compares from highest to lowest old highscore. True at first value where player_score is higher
            if not GUI:
                new_high_score_string = request_new_highscore_text(i, player_score)  # Returns formatted
            else:  # Username is not None if using GUI, so can format immediately:
                new_high_score_string = format_new_highscore_string(username, player_score)
            high_scores.insert(i, new_high_score_string)
            if len(high_scores) > 10:
                del high_scores[-1]  # Removes the last (thus lowest) high_score saved if there are too many.
            high_scores = ",".join(high_scores)
            file = open("high_scores_stored.txt", "w+")
            file.write(high_scores)
            file.close()
            break
        else:
            continue


def iteration_limit_ship_placement(iterations_attempting_to_place_ships):
    # Prevents an infinite loop when placing the ships
    iterations_attempting_to_place_ships += 1
    if iterations_attempting_to_place_ships > 64:
        print("There are too many ships to be placed. Please configure ships.txt and restart the program")
        quit()
    return iterations_attempting_to_place_ships