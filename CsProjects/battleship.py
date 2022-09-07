""" ---------------------------------------------------------------------------
    File: battleship.py
    Author: Kyle Walker
    Purpose: This program uses creates an the Board and Ship Classes to be used
             in the battleship program. Each of these classes contain methods
             and attributes that allow the game to be played on a single board.
             Ships can be created using any shape and position with a chosen
             rotation, and will be stored on the board for the game. The player
             can choose where to set the ships as well as which coordinates to
             attack. The board layout will be printed out after each turn to
             show which spots are hits, misses, ships, empty spots, or sunken
             ships. There are multiple assertions to make sure no actions go
             outside of the board's boundaries.

"""

class Board:
    """ This class represents the Board where the ships and hit data will be
        stored and printed. The board is created to fit any input size, and
        contains the methods used for "playing" battleship such as adding
        ships, taking shots, and displaying the board after each turn.

        The constructor creates the 2d array used to store ship and hit data,
        also useful for printing out the board. The size attribute defines
        the size of the board's axes, from 0 inclusive to size exclusive.
        There is also a ships attribute which serves as a dictionary of ship
        names, references, and coordinates.

        The class defines several helpful methods and fields:
            add_ship = Adds a ship to the grid at a given location, following
            its shape and rotation and storing the coordinates in the dict.
            print = prints the visual of the grid and all pieces for each turn.
            has_been_used = A check to see if a shot has already been taken
            at a given coordinate.
            attempt_move = Checks the grid and changes the value to a hit,
            miss, or sunken ship depending on criteria. It also returns
            the result of the action such as hit, miss, or sunk.

    """
    def __init__(self, size):
        self._grid = []
        self._size = size
        self._ships = dict()
        assert type(size) == int and size > 0
        for i in range(size):
            row_array = []
            for i in range(size):
                row_array.append(".")
            self._grid.append(row_array)

    def add_ship(self, ship, position):
        ship_location = []
        # Converts position into 2d array indexes
        for coord in ship._shape:
            location_coord = []
            location_coord.append(coord[0] + position[0])
            location_coord.append(coord[1] + position[1])
            ship_location.append(location_coord)
        self._ships[ship] = [ship._name, ship_location]

        for coord in ship_location:
            assert coord[0] <= self._size and coord[1] <= self._size
            y = self._size - coord[1] - 1
            x = coord[0]
            assert self._grid[y][x] == "."
            self._grid[y][x] = ship._name[0]

    def print(self):
        # Axis_space helps to fit grid when size has two digits.
        if self._size < 11:
            axis_space = 1
        else:
            axis_space = 2
        print(" " * (axis_space + 1) + "+" + "--" * self._size + "-+")
        row_ind = self._size
        for row in self._grid:
            row_ind -= 1
            contents = ""
            for element in row:
                contents += (" " + str(element))
            if axis_space == 2 and len(str(row_ind)) == 1:
                print(" " + str(row_ind) + " " + "|" + contents + " |")
            else:
                print(str(row_ind) + " " + "|" + contents + " |")
        print(" " * (axis_space + 1) + "+" + "--" * self._size + "-+")
        # Adds the extra row of digits when size is 2 digits
        if axis_space == 2:
            x_axis = " " * 23
            for i in range(10, self._size):
                x_axis += (str(i)[0] + " ")
            print(" " * axis_space + x_axis)
        extra_digits = ""
        for i in range(10, self._size):
            extra_digits += (str(i)[1] + " ")
        print(" " * axis_space + "   0 1 2 3 4 5 6 7 8 9 " + extra_digits)

    def has_been_used(self, position):
        assert position[0] <= self._size and position[1] <= self._size
        y = self._size - position[1] - 1
        x = position[0]
        was_used = False
        hitmarkers = ["o", "X", "*"]
        if self._grid[y][x] in hitmarkers:
            was_used = True
        return was_used

    def attempt_move(self, position):
        assert position[0] <= self._size and position[1] <= self._size
        y = self._size - position[1] - 1
        x = position[0]
        result = "Miss"
        assert self.has_been_used(position) is False
        if self._grid[y][x].isalpha():
            self._grid[y][x] = "*"
            result = "Hit"
        if self._grid[y][x] == ".":
            self._grid[y][x] = "o"

        for key, value in self._ships.items():
            i = 0
            while i < len(value[1]):
                if list(position) == value[1][i]:
                    key._status[i] = "*"
                i += 1
            # Checks if the ship's status contains all hits, and checks that
            # This specific ship has not already been sunk.
            # When sunk, the dictionary value will clear and only contain
            # the "Sunk" keyword to prevent returning multiple sunk results.
            if set(key._status) == {"*"} and self._ships[key][1] != ["Sunk"]:
                for coord in self._ships[key][1]:
                    coord_y = self._size - coord[1] - 1
                    coord_x = coord[0]
                    self._grid[coord_y][coord_x] = "X"
                result = ("Sunk (" + str(key._name) + ")")
                self._ships[key][1] = ["Sunk"]
        return result

class Ship:
    """ This class represents each Ship that is used to set up the Board
        for the game of battleship. Multiple ships can be made and given
        any shape and rotation, so that they can be placed anywhere
        available on the Board.

        The constructor creates a Ship object that contains a name string,
        and a shape which is a list of connected coordinates. The name is
        the string corresponding to the ship, the shape is the list of
        base coordinates, and the status is a list containing whether
        each part of the ship is alive or has been hit.

        The class defines several helpful methods and fields:
            print = Prints the status of the ship as a string of the
            letter corresponding to the name, with asterisks at hit spots.
            It then shows the full name next to the status.
            is_sunk = Checks the status of the ship to determine if it
            is still standing or has been sunk.
            rotate = calculates the new base coordinates of the ship's
            shape based on the number of 90 degree rotations.

    """
    def __init__(self, name, shape):
        self._name = name
        self._shape = shape
        self._status = []
        for i in range(len(self._shape)):
            self._status.append(str(self._name)[0])

    def print(self):
        length = 0
        ship_data = ""
        for element in self._status:
            ship_data += str(element)
            length += 1
        print(ship_data + " " * (10 - length) + str(self._name))

    def is_sunk(self):
        is_sunk = False
        if set(self._status) == {"*"}:
            is_sunk = True
        return is_sunk

    def rotate(self, amount):
        assert 0 <= amount <= 3
        new_position = []
        for coords in self._shape:
            if amount == 0:
                new_x = coords[0]
                new_y = coords[1]
            elif amount == 1:
                new_x = coords[1]
                new_y = coords[0] * -1
            elif amount == 2:
                new_x = coords[0] * -1
                new_y = coords[1] * -1
            elif amount == 3:
                new_x = coords[1] * -1
                new_y = coords[0]
            new_coords = (new_x, new_y)
            new_position.append(new_coords)
        self._shape = new_position





