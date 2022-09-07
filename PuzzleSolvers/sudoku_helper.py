''' --------------------------------------------------------------------------
    File: sudoku_helper.py
    Author: Kyle Walker
    Purpose: This program takes a sudoku grid file from the user and prompts
            for a command. The commands are set, search, conflicts, and back.
            This allows the user to set a value in the sudoku grid, search
            for areas with only one possible solution, check for conflicting
            values in the grid, and go back to a previous iteration of the
            grid. The history is stored in a linked list as a stack, where
            each time the grid is edited a new Node is pushed to the head of
            the linked list. Using the search and set commands, the user is
            able to fully solve any sudoku puzzle.


            Soduku input txt file must follow format where '.' = blank, and numbers are grouped in 3x3 boxes with gaps between:
                    53. .7. ...
                    6.. 195 ...
                    .98 ... .6.

                    8.. .6. ..3
                    4.. 8.3 ..1
                    7.. .2. ..6

                    .6. ... 28.
                    ... 419 ..5
                    ... .8. .79
    
'''

# ListNode and Stack Classes are created, and the pop and push methods are
# defined under the Stack
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def push(self, val):
        if self.head is None:
            self.head = ListNode(val)
        else:
            new_node = ListNode(val)
            new_node.next = self.head
            self.head = new_node

    def pop(self):
        old_node = self.head
        self.head = self.head.next
        old_node.next = None
        return old_node.val

def main():
    grid = []
    file_found = False
    HistoryStack = Stack()
    try:
        print("Please give the name of the file that contains the board:")
        file_name = input()
        file = open(file_name, "r")
        grid = grid_from_file(file)
        file_found = True
    except (FileNotFoundError, IOError):
        print("ERROR: The file could not be opened.")
        file_found = False

    # Current grid is created and added as the first node in the history stack
    cur_grid = grid
    HistoryStack.push(cur_grid)
    # blank line check for the input testcases
    blank_line = False
    while file_found is True:
        try:
            if blank_line is False:
                print("Your command:")
            command = input()
            if blank_line is False:
                print()
            blank_line = False
            # Checks commands
            if "set" in command:
                new_grid = set_point(command, cur_grid)
                HistoryStack.push(new_grid)
            elif command == "back":
                HistoryStack = go_back(HistoryStack)
            elif command == "conflicts":
                conflicting = False
                conflicts(HistoryStack, conflicting)
            elif command == "search":
                conflicting = False
                search(HistoryStack, conflicting)
            elif command == "":
                blank_line = True
            else:
                print("ERROR: Invalid command \n")
            # Prints the current grid every time a command is completed
            if blank_line is False:
                cur_grid = HistoryStack.head.val
                for row in cur_grid:
                    row_str = ""
                    for char in row:
                        row_str += str(char)
                    print(row_str)
                print()
        except EOFError:
            break

def grid_from_file(file):
    '''
        Creates a 2D array of the sudoku grid from the file.
        Arguments: file = the opened input file entered by the user
        Return Values: grid = the 2D array used as the first head of
        the stack
        Pre-conditions: file must be readable and opened in main
    '''
    grid = []
    temp_rows = []
    for line in file:
        line = line.strip("\n")
        print(line)
        for char in line:
            temp_rows.append(char)
        grid.append(temp_rows)
        temp_rows = []
    print()
    return grid

def set_point(command, cur_grid):
    '''
        Changes specific values in the grid as per user request, but
        also tells user if the value is already filled. Returns a new
        grid to be printed and pushed to the front of the stack.
        Arguments: command = the input containing the x, y, and num
        that the user wants to set.
        cur_grid = the head of the stack, the current grid.
        Return Values: new_grid = new head of list, containing edited
        values.
        Pre-conditions: set command must be entered with proper x, y, and
        number info.
    '''
    command = command.split(" ")
    y_in = int(command[2])
    x_in = int(command[1])
    y = y_in
    x = x_in
    if y_in < 4:
        y -= 1
    if x_in < 4:
        x -= 1
    if y_in > 6:
        y += 1
    if x_in > 6:
        x += 1
    num = int(command[3])

    new_grid = dup_grid(cur_grid)
    if new_grid[y][x] == ".":
        print("Square " + str(x_in) + "," + str(y_in) +\
        " set to " + str(num) + ".")
        print()
        new_grid[y][x] = num
    else:
        print("ERROR: The 'set' command cannot run, "
        "because the space already holds a value. \n")
    return new_grid

def go_back(HistoryStack):
    '''
        Pops the head of the stack and moves the head to the previous node.
        Arguments: HistoryStack = The linked list / stack of grid data nodes
        Return Values: HistoryStack = edited stack returned.
        Pre-conditions: HistoryStack must contain at least one node for the
        pop to take place.
    '''
    if HistoryStack.head.next is None:
        print("ERROR: You are already at the init state,"
        " you cannot go back. \n")
    else:
        HistoryStack.pop()
    return HistoryStack

def conflicts(HistoryStack, conflicting):
    '''
        Checks for conflicting rows, columns, and squares to warn
        the user. Runs 3 separate functions to check each.
        Arguments: HistoryStack = The linked list / stack of grid data nodes
        conflicting = Bool used to record if there is a conflict or not,
        important because each conflict function can be used to either
        iterate through sections but will only record conflicts if this
        bool is True.
        Return Values: None
        Pre-conditions: conflicts command must be entered.
    '''
    grid = temp_grid(HistoryStack)
    checking = True
    conflicting = row_conflict_check(grid, conflicting, checking)
    conflicting = col_conflict_check(grid, conflicting, checking)
    conflicting = square_conflict_check(grid, conflicting, checking)
    if conflicting is False:
        print("Hooray! No conflicts found.")


def row_conflict_check(grid, conflicting, checking):
    '''
        Checks for conflicting values in each of the rows to return to the
        main conflicting function. Also can be used to record all row data.
        Arguments: grid: the duplicated current grid
        conflicting = Bool used to record if there is a conflict or not,
        important because each conflict function can be used to either
        iterate through sections but will only record conflicts if this
        bool is True.
        checking = Bool to determine if this function is being used for
        returning row data or for checking for conflicts.
        Return Values: conflicting = returns if conflicts are found
        row_num_array = array of all row numbers used for search function.
        Pre-conditions: conflicts command must be entered.
    '''

    y = 0
    row_num_array = []
    while y < 9:
        row_contents = []
        row = grid[y]
        for element in row:
            if str(element).isnumeric():
                row_contents.append(str(element))
        row_num_array.append(row_contents)
        if len(row_contents) > len(set(row_contents)):
            conflicting = True
            if checking is True:
                print("ERROR: Row " + str(y + 1) + " has a conflict.")

        y += 1
    if checking is True:
        return conflicting
    else:
        return row_num_array

def col_conflict_check(grid, conflicting, checking):
    '''
        Checks for conflicting values in each of the columns to return to the
        main conflicting function. Also can be used to record all column data.
        Arguments: grid: the duplicated current grid
        conflicting = Bool used to record if there is a conflict or not,
        important because each conflict function can be used to either
        iterate through sections but will only record conflicts if this
        bool is True.
        checking = Bool to determine if this function is being used for
        returning column data or for checking for conflicts.
        Return Values: conflicting = returns if conflicts are found
        col_num_array = array of allcolumn numbers used for search function.
        Pre-conditions: conflicts command must be entered.
    '''
    x = 0
    col_num_array = []
    while x < 9:
        col_contents = []
        for row in grid:
            if str(row[x]).isnumeric():
                col_contents.append(str(row[x]))
        col_num_array.append(col_contents)
        if len(col_contents) > len(set(col_contents)):
            conflicting = True
            if checking is True:
                print("ERROR: Column " + str(x + 1) + " has a conflict.")
        x += 1
    if checking is True:
        return conflicting
    else:
        return col_num_array


def square_conflict_check(grid, conflicting, checking):
    '''
        Checks for conflicting values in each of the squares to return to the
        main conflicting function. Also can be used to record all square data.
        Arguments: grid: the duplicated current grid
        conflicting = Bool used to record if there is a conflict or not,
        important because each conflict function can be used to either
        iterate through sections but will only record conflicts if this
        bool is True.
        checking = Bool to determine if this function is being used for
        returning square data or for checking for conflicts.
        Return Values: conflicting = returns if conflicts are found
        square_num_array = array of all square numbers used for search funct.
        Pre-conditions: conflicts command must be entered.
    '''
    sx = 0
    sy = 0
    square_num_array = []
    square_row = sy * 3
    square_col = sx * 3
    x = 0
    y = 0
    while sy < 3:
        square_row = sy * 3
        while sx < 3:
            square_col = sx * 3
            square_contents = []
            for y in range(3):
                for x in range(3):
                    if str(grid[square_row + y][square_col + x]).isnumeric():
                        square_contents.append\
                        (str(grid[square_row + y][square_col + x]))
            square_num_array.append(square_contents)
            if (len(square_contents) > len(set(square_contents))):
                conflicting = True
                if checking is True:
                    print("ERROR: Sub-region " + str(sy) + "," +
                    str(square_col) + " has a conflict.")
            sx += 1
        sx = 0
        sy += 1
    if checking is True:
        return conflicting
    else:
        return square_num_array

def search(HistoryStack, conflicting):
    '''
        Searches for all places that have only one solution, and suggests
        the value to the user.
        Arguments: HistoryStack = The linked list / stack of grid data nodes
        conflicting = Bool used to record if there is a conflict or not,
        important because each conflict function can be used to either
        iterate through sections but will only record conflicts if this
        bool is True.
        Return Values: None
        Pre-conditions: search command prompted
    '''
    checking = False
    grid = temp_grid(HistoryStack)
    row_num_array = row_conflict_check(grid, conflicting, checking)
    col_num_array = col_conflict_check(grid, conflicting, checking)
    square_num_array = square_conflict_check(grid, conflicting, checking)
    y = 0
    x = 0
    sq = 0
    solved = False
    # Iterates through the rows, each column in the row, and the square that
    # correlates to each x,y value. The numbers from each row, column, and
    # square are stored in 2D arrays, allowing for iteration through each.
    # The total number data of the row, col, and quare lists are put into a set
    # and checked if only one number is missing, giving a solution.
    while y < 9:
        if y // 3 > (y - 1) // 3 and y != 0:
            sq += 3
        x = 0
        while x < 9:
            num_set = set()
            if grid[y][x] == ".":
                for element in row_num_array[y]:
                    num_set.add(element)
                for element in col_num_array[x]:
                    num_set.add(element)
                for element in square_num_array[sq + x // 3]:
                    num_set.add(element)
                if len(num_set) == 8:
                    for num in range(1, 10):
                        if str(num) not in num_set:
                            print("Solution! The only value possible at"
                            " square " + str(x + 1) + "," + str(y + 1) +
                            " is " + str(num) + ".")
                            solved = True
                            x += 1
            x += 1
        y += 1
    if solved is False:
        print("Sorry, no solutions were found.")

def dup_grid(grid):
    '''
        Duplicates the grid so that each node is a new reference,
        preventing past grids from being changed.
        Arguments: grid = the current grid from the file
        Return Values: new_grid = new copy of the old grid
        Pre-conditions: None
    '''
    new_grid = []
    for line in grid:
        new_grid.append(line.copy())
    return new_grid

def temp_grid(HistoryStack):
    '''
        Creates a temporary grid to be used when iterating through
        grid data, used locally in other functions to prevent
        changing original reference. Aso deletes all spaces to make
        iteration easier.
        Arguments: HistoryStack = The linked list / stack of grid data nodes
        Return Values: grid = temporary grid to be iterated through.
        Pre-conditions: HistoryStack must contain Node data
    '''
    grid = dup_grid(HistoryStack.head.val)
    for line in grid:
        if line == []:
            grid.remove(line)
    for line in grid:
        for char in line:
            if char == " ":
                line.remove(char)
    return grid


main()