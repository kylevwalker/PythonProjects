''' --------------------------------------------------------------------------
    File: twine.py
    Author: Kyle Walker
    Purpose: This program prompts the user with commands to explore a grid and
            display statistics such as current position, position history, map,
            crossover locations, and ranges. The user can give commands to move
            in one of the four cardinal directions, trace back a step, or do
            nothing. The user is also asked to give an obstacle file in the
            beginning, and if they do it will limit the positions they are
            able to reach. The map displays a printed graph of the path and
            current position from the origin, ranges show the max value in
            each direction, and crossings shows the amount of times an area was
            reached in history.
    Course: CSC 120, spring 2021
'''

def main():
    ''' This function asks for the obstacle file and opens it if possible.
        It then calls the prompter function, which carries out all other
        operations.
        Arguments: None
        Return Values: None
        Pre-conditions: None
    '''
    while True:
        try:
            print("Please give the name of the obstacles filename, or \
- for none:")
            file_name = input()
            obstacles = []
            if file_name == "-":
                break
            file = open(file_name, "r")
            for line in file:
                numbers = line.split()
                pair = (int(numbers[0]), int(numbers[1]))
                obstacles.append(pair)
            obstacles = sorted(obstacles)
            break
        except:
            print("ERROR: File not found. Check file or try a new file name.")

    current_position = (0, 0)
    history_array = [(0, 0)]
    prompter(current_position, history_array, obstacles)

def prompter(current_position, history_array, obstacles):
    ''' This function shows the user's position and history, then asks for a
        command every time. It will call the appropriate function for each
        command and use the returned values to adjust the on screen stats.
        Arguments: current_position tracks the current x and y coordinates.
        history_array records each previous position in a timeline array.
        obstacles is a sorted array that includes inaccessable coordinates.
        Return Values: None
        Pre-conditions: None
    '''
    x = 0
    y = 0
    while True:
        print("Current position: " + str(current_position))
        print("Your history:     " + str(history_array))
        print("What is your next command?")
        try:

            command = str(input())
            if command == "n" or command == "e" or command == "s" \
                or command == "w":
                current_position, history_array, x, y = movement(command,
                current_position, history_array, obstacles, x, y)
            elif command == "":
                print("You do nothing.")
            elif command == "back":
                current_position, x, y = back(current_position,
                history_array, x, y)
            elif command == "crossings":
                crossings(current_position, history_array)
            elif command == "map":
                mapper(current_position, history_array, obstacles)
            elif command == "ranges":
                ranges(current_position, history_array)
            else:
                print("ERROR: Incorrect command.")
            print()

        except:
            break

def movement(command, current_position, history_array, obstacles, x, y):
    ''' This function changes your coordinates based on the four cardinal
        directions and updates the history array. It will also prevent the
        user from crossing over obstacle locations.
        Arguments: command is the command input (n, e, s, w,) corresponding
        to up, right, down, and left respectively.
        current_position tracks the current x and y coordinates.
        history_array records each previous position in a timeline array.
        obstacles is a sorted array that includes inaccessable coordinates.
        x is the x position
        y is the y position
        Return Values: returns current_position, history_array, x, and y to
        update the position and history.
        Pre-conditions: Command must follow n, e, s, w format.
    '''
    if command == "n":
        y += 1
    elif command == "e":
        x += 1
    elif command == "s":
        y -= 1
    elif command == "w":
        x -= 1
    current_position = (x, y)
    if current_position in obstacles:
        print('''You could not move in that direction, because there \
is an obstacle in the way.''')
        print("You stay where you are.")
        current_position = history_array[-1]
        x, y = current_position[0], current_position[1]
    else:
        history_array.append(current_position)
    return current_position, history_array, x, y


def back(current_position, history_array, x, y):
    ''' This function reverts a step in the position history and resets the
        position to the last position the user was at.
        Arguments: current_position tracks the current x and y coordinates.
        history_array records each previous position in a timeline array.
        x is the x position
        y is the y position
        Return Values: returns current_position, x, y to update position.
        Pre-conditions: back command must be called
    '''
    if len(history_array) > 1:
        history_array.pop()
        current_position = history_array[-1]
        x, y = current_position[0], current_position[1]
        print("You retrace your steps by one space")
    else:
        print("Cannot move back, as you're at the start!")
    return current_position, x, y

def crossings(current_position, history_array):
    ''' This function shows how many time the current position has been
        recorded in the history.
        Arguments: current_position tracks the current x and y coordinates.
        history_array records each previous position in a timeline array.
        Return Values: None
        Pre-conditions: crossings command must be called.
    '''
    crossings = 0
    for element in history_array:
        if element == current_position:
            crossings += 1
    print("There have been " + str(crossings) + " times in the \
history when you were at this point.")


def mapper(current_position, history_array, obstacles):
    ''' This function displays a map with the origin, obstacles, and the path
        the user had taken. * for origin, + for current location, . for path,
        and X for obstacles.
        Arguments: current_position tracks the current x and y coordinates.
        history_array records each previous position in a timeline array.
        obstacles is a sorted array that includes inaccessable coordinates.
        Return Values: None
        Pre-conditions: map command must be called.
    '''
    print("+" + "-" * 11 + "+")
    row = 5
    while row >= -5:
        x_coord_array = []
        for element in history_array:
            if element[1] == row:
                x_coord_array.append(element[0])
            middle_section = ""
            for x_coord in range(-5, 6):
                if row == current_position[1] and len(middle_section) \
                - 5 == current_position[0]:
                    middle_section += "+"
                elif row == 0 and len(middle_section) == 5:
                    middle_section += "*"
                elif (x_coord, row) in obstacles:
                    middle_section += "X"
                elif x_coord in x_coord_array:
                    middle_section += "."
                else:
                    middle_section += " "
        print("|" + middle_section + "|")
        row -= 1
    print("+" + "-" * 11 + "+")

def ranges(current_position, history_array):
    ''' This function lists the max values for each direction in the history,
        not including backtraced values.
        Arguments: current_position tracks the current x and y coordinates.
        history_array records each previous position in a timeline array.
        Return Values: None
        Pre-conditions: ranges command must be called
    '''
    west_max = 0
    east_max = 0
    south_max = 0
    north_max = 0
    for element in history_array:
        if int(element[0]) < int(west_max):
            west_max = element[0]
        if int(element[0]) > int(east_max):
            east_max = element[0]
        if int(element[1]) < int(south_max):
            south_max = element[1]
        if int(element[1]) > int(north_max):
            north_max = element[1]
    print("The furthest West your twine goes is " + str(west_max))
    print("The furthest East your twine goes is " + str(east_max))
    print("The furthest South your twine goes is " + str(south_max))
    print("The furthest North your twine goes is " + str(north_max))

main()