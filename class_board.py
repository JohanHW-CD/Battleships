# Creates and handles the board in which the game takes place. All of the game takes place in one instance of Board.

from random import *


class Board:
    # Constructor. range of x and y are width and height of the board respectively. Any squares are allowed.
    def __init__(self, x=7, y=7):
        self.x = x
        self.y = y
        self.system = self.create_coordinate_system()

    def create_coordinate_system(self):
        # Creates an x*y array where each temp_row nestled inside a larger list. This array represents the playing board
        system = []
        for i in range(self.y + 1):
            temp_row = []
            for j in range(self.x + 1):
                temp_row.append(" ")
            system.append(temp_row)
        return system

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_system(self):
        return self.system

    def is_input_within_the_board(self, x, y):
        # Returns True if input values are within the coordinate system. Else, returns False.
        if x >= 0 and y >= 0:
            if x <= self.x and y <= self.y:
                return True
        else:
            return False

    def start_coordinate_ship(self):
        # Randomizes a starting coordinate for placing the ships
        x_coord = randint(0, self.x)
        y_coord = randint(0, self.y)
        return (x_coord, y_coord)

    def get_length(self, list_ship_sizes, ship_number):
        # Fetches length of one ship
        ship_length = int(list_ship_sizes[ship_number])
        return ship_length

    def check_if_possible_length(self, length):
        if length > self.x:
            print("The ship lengths are too long to be placed. Please configure in ships.txt and restart.")
            quit()

    def direction_of_ship(self, start_coordinate, length):
        # Takes starting coordinate & length, gives random direction, returns direction if ship does not end outside of board.
        while True:
            self.check_if_possible_length(length)
            direction = randint(0, 3)  # right: 0, left: 1, up: 2 (y index down), down: 3
            if direction == 0:
                end_coordinate = start_coordinate[0] + length - 1
                if end_coordinate <= self.x:
                    break
                else:
                    continue

            if direction == 1:
                end_coordinate = start_coordinate[0] - length + 1
                if end_coordinate >= 0:
                    break
                else:
                    continue

            if direction == 2:
                end_coordinate = int(start_coordinate[1]) - length + 1
                if end_coordinate >= 0:
                    break
                else:
                    continue

            if direction == 3:
                end_coordinate = int(start_coordinate[1]) + length - 1
                if end_coordinate <= self.y:
                    break
                else:
                    continue
        return direction

    def collision_check(self, start_coordinates, length, direction):
        # Given starting coordinates, length and direction. Returns True if the prospective coordinates collide with
        # other ship or lays right next to them. Returning True ==> new starting_coords and direction given.
        collision_right, collision_left, collision_up, collision_down = False, False, False, False
        if direction == 0:
            collision_right = self.collision_check_right(start_coordinates, length, direction)
        elif direction == 1:
            collision_left = self.collision_check_left(start_coordinates, length, direction)
        elif direction == 2:
            collision_up = self.collision_check_up(start_coordinates, length, direction)
        else:
            collision_down = self.collision_check_down(start_coordinates, length, direction)

        if collision_right or collision_left or collision_up or collision_down:
            return True
        else:
            return False

    def collision_check_right(self, start_coordinates, length, direction):
        # These functions iterate over a 3 coords wide area in the direction of a ships length, starting from behind the
        # ship and ending one step in front of it. If in any of these coordinates there is another ship then it returns
        # True, since this collides with the area of the other ship.

        for dy in range(3):
            y_coordinate_to_check = start_coordinates[1] - 1 + dy
            for dx in range(int(length) + 2):
                try:
                    x_coordinate_to_check = start_coordinates[0] - 1 + dx
                    if x_coordinate_to_check < 0 or y_coordinate_to_check < 0:
                        continue
                    if self.system[y_coordinate_to_check][x_coordinate_to_check] == "X":
                        return True
                    else:
                        continue
                except:
                    continue
        return False

    def collision_check_left(self, start_coordinates, length, direction):
        # 3 wide checking to the left
        for dy in range(3):
            y_coordinate_to_check = start_coordinates[1] - 1 + dy
            for dx in range(int(length) + 2):
                try:
                    x_coordinate_to_check = start_coordinates[0] + 1 - dx
                    if x_coordinate_to_check < 0 or y_coordinate_to_check < 0:
                        continue
                    if self.system[y_coordinate_to_check][x_coordinate_to_check] == "X":
                        return True
                    else:
                        continue
                except:
                    continue
        return False

    def collision_check_up(self, start_coordinates, length, direction):
        # 3 wide checking upwards, up == y index goes down
        for dx in range(3):
            x_coordinate_to_check = start_coordinates[0] - 1 + dx
            for dy in range(int(length) + 2):
                try:
                    y_coordinate_to_check = start_coordinates[1] + 1 - dy
                    if x_coordinate_to_check < 0 or y_coordinate_to_check < 0:
                        continue
                    if self.system[y_coordinate_to_check][x_coordinate_to_check] == "X":
                        return True
                    else:
                        continue
                except:
                    continue
        return False

    def collision_check_down(self, start_coordinates, length, direction):
        # 3 wide checking downwards
        for dx in range(3):
            x_coordinate_to_check = start_coordinates[0] - 1 + dx
            for dy in range(int(length) + 2):
                try:
                    y_coordinate_to_check = start_coordinates[1] - 1 + dy
                    if x_coordinate_to_check < 0 or y_coordinate_to_check < 0:
                        continue
                    if self.system[y_coordinate_to_check][x_coordinate_to_check] == "X":
                        return True
                    else:
                        continue
                except:
                    continue
        return False

    def place_ships(self, start_coordinates, length, direction):
        # The ships with approved starting_coordinates, lengths and directions are placed in the system. Returned in a list.
        # X == ship, # == shot ship, "o" == missed shot, " " = not shot.
        coordinates_of_ship = []
        if direction == 0:
            for i in range(int(length)):
                self.system[start_coordinates[1]][start_coordinates[0] + i] = 'X'
                coordinates_of_ship.append((start_coordinates[0] + i, start_coordinates[1]))

        if direction == 1:
            for i in range(int(length)):
                self.system[start_coordinates[1]][start_coordinates[0] - i] = 'X'
                coordinates_of_ship.append((start_coordinates[0] - i, start_coordinates[1]))

        if direction == 2:
            for i in range(int(length)):
                self.system[start_coordinates[1] - i][start_coordinates[0]] = 'X'
                coordinates_of_ship.append((start_coordinates[0], start_coordinates[1] - i))

        if direction == 3:
            for i in range(int(length)):
                self.system[start_coordinates[1] + i][start_coordinates[0]] = 'X'
                coordinates_of_ship.append((start_coordinates[0], start_coordinates[1] + i))
        return coordinates_of_ship

    def shoot(self, x, y):
        # Checks the value in the coordinate system where the player shoots and changes it accordingly.
        if self.is_input_within_the_board(x, y):
            if self.system[y][x] == " ":
                self.system[y][x] = "o"
                return "Miss!"
            elif self.system[y][x] == "o" or self.system[y][x] == "#":
                return None
            elif self.system[y][x] == "X":
                self.system[y][x] = "#"
                return "Hit!"
        else:
            return "Outside"

    def end_condition(self):
        # Checks if there are any ships left in game. If not it returns True meaning the end_condition is fulfilled.
        for i in range(len(self.system)):
            for j in range(len(self.system)):
                if self.system[i][j] == "X":
                    return False
                else:
                    pass
        return True

    def look_for_sunk_ship(self, list_of_hit_coordinates, coordinates_of_ships):
        # Checks if all coordinates for a ship are matched in the list of hit coordinates. The coordinates_of_ships variable
        # contains nested lists, where each nestled list describes one ship. Returns the index for a completely sunk ship.
        for i in range(len(coordinates_of_ships)):
            sunk_ship = all(coordinates in list_of_hit_coordinates for coordinates in coordinates_of_ships[i])
            if sunk_ship:
                return i
        return None

    def mark_around_sunk_ship(self, coordinates_of_ships, i):
        # Marks "o" in a 3 wide area around a sunk ship. Does not alter "#" symbols.
        if i is None:
            return None
        specific_sunk_ship_coordinates = coordinates_of_ships[i]
        for coordinate in specific_sunk_ship_coordinates:
            x_cor = coordinate[0]
            y_cor = coordinate[1]
            for y in range(3):
                for x in range(3):
                    try:
                        if y_cor - 1 + y < 0 or x_cor - 1 + x < 0:
                            continue
                        elif self.system[y_cor - 1 + y][x_cor - 1 + x] == "#":
                            continue
                        else:
                            self.system[y_cor - 1 + y][x_cor - 1 + x] = "o"
                    except:
                        pass
        # To ensure this ship cannot be found as sunk again it is deleted from the list of ship coordinates.
        removed_coords = coordinates_of_ships[i]
        del coordinates_of_ships[i]
        return removed_coords  # Removed coordinates are returned.
