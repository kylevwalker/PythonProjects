""" ---------------------------------------------------------------------------
    File: maze_solver.py
    Author: Kyle Walker
    Purpose: This program takes an input file of a maze that must include
             exactly one Start and one End point, as well as not having any
             looping paths. The maze paths are represented with hash symbols,
             and the program uses a custom tree class to recursively traverse
             each possible path until the correct solution is found. There are
             multiple commands whihc give different information on the maze.
             dumpCells shows all of the cells, or coordinates that represent
             path areas in sorted order. dumpTree prints the tree created in
             up, down, left, right order with indentations representing paths.
             dumpSolution gives the coordinates of the path that leads to the
             exit point. dumpSize gives the max width and height of the maze.
             Lastly, an empty line will print the maze with the correct path
             shown as period characters connecting the start and end points.

    Format:
        Input maze file must follow format, where S = start, E = end, and # = wall:
                ####S###########   ####
                #  #    #      #####  #
                #  ###  #####         #
                #    #  #   #         #
                #  ###  ### #         #
                #           #         #
                #         ####   ######
                #    E#####

"""

class MazeTreeNode:
    """ This class represents the Nodes used in the 4 - directional tree.
        These nodes each contain their coordinate position in the maze,
        and the 4 children adjacent to them (up, down, left, right).

        The constructor creates pointers to None, but allow for children to
        be assigned in each of the 4 directions. Each node can have a child
        up, down, left, or right of them with the possibility of None or
        a parent Node.

        The class does not contain any other methods.
    """
    def __init__(self, coords):
        self._coords = coords
        self._up = None
        self._down = None
        self._left = None
        self._right = None

def main():
    file = None
    try:
        file_name = input()
        file = open(file_name, "r")
    except FileNotFoundError:
        print("ERROR: Could not open file: " + file_name)

    if file is not None:
        try:
            cells, start_coord, end_coord, maze_data = cell_finder(file)
            if start_coord is None or end_coord is None:
                print("ERROR: Every map needs exactly one START and " \
                      "exactly one END position")
                return
            root = MazeTreeNode(start_coord)
            create_tree(root, cells, root)
            command = input()
            if command == "dumpCells":
                dump_cells(cells, start_coord, end_coord)
            elif command == "dumpTree":
                print("DUMPING OUT THE TREE THAT REPRESENTS THE MAZE:")
                print_tree(root, root, "")
            elif command == "dumpSolution":
                end_path = [root._coords]
                solve_maze(root, root, end_coord, end_path, maze_data, True)
            elif command == "dumpSize":
                dump_size(cells)
            elif command == "":
                end_path = [root._coords]
                solve_maze(root, root, end_coord, end_path, maze_data, False)
            else:
                print("ERROR: Unrecognized command " + str(command))
        except EOFError:
            return

def cell_finder(file):
    '''
        This function iterates through the maze file and creates an array
        of maze information, as well as a set of coords for the paths and
        a record of the start and end coordinates as tuples.
        Arguments:
            file: the input maze file
        Return Values:
            cells: A set of all path coordinates stored as tuples
            start_coord: A coord tuple of the start point
            end_coord: A coord tuple of the end point
            maze_data: 2D array of maze layout
        Pre-conditions: file must be found and following maze rules
    '''
    maze_data = []
    cells = set()
    for line in file:
        maze_data.append(line.strip("\n"))
    x = 0
    y = 0
    start_coord = None
    end_coord = None
    special_chars = ["#", "S", "E"]
    for row in maze_data:
        for x in range(len(row)):
            if maze_data[y][x] not in special_chars and maze_data[y][x] != " ":
                print("ERROR: Invalid character in the map")
            if maze_data[y][x] in special_chars:
                try:
                    if maze_data[y][x] == "S":
                        assert start_coord is None
                        start_coord = tuple([x, y])
                except AssertionError:
                    print("ERROR: The map has more than one START position")
                try:
                    if maze_data[y][x] == "E":
                        assert end_coord is None
                        end_coord = tuple([x, y])
                except AssertionError:
                    print("ERROR: The map has more than one END position")
                cell = tuple([x, y])
                cells.add(cell)
        y += 1
    return cells, start_coord, end_coord, maze_data

def dump_cells(cells, start_coord, end_coord):
    '''
        This function prints the sorted set of cells.
        Arguments:
            cells: The set of cells
            start_coord: the tuple for starting coords
            end_coord: the tuple for ending coords
        Return Values: none
        Pre-conditions: cells must not be empty, dumpCells called
    '''
    print("DUMPING OUT ALL CELLS FROM THE MAZE:")
    for pair in sorted(cells):
        if pair == start_coord:
            print("  " + str(pair) + "    START")
        elif pair == end_coord:
            print("  " + str(pair) + "    END")
        else:
            print("  " + str(pair))

def dump_size(cells):
    '''
        This function prints the max height and width of the maze
        based on the coordinate values rather than the file's lines
        Arguments:
            cells: The set of cells
        Return Values: none
        Pre-conditions: cells must not be empty, dumpSize must be called
    '''
    max_x = 0
    max_y = 0
    for pair in cells:
        if pair[0] > max_x:
            max_x = pair[0]
        if pair[1] > max_y:
            max_y = pair[1]
    print("MAP SIZE:")
    print("  wid: " + str(max_x + 1))
    print("  hei: " + str(max_y + 1))

def create_tree(root, cells, prev):
    '''
        This function creates the tree using the MazeTreeNode class.
        It uses recursion and avoids looping to create a tree with all
        possible paths stored through connecting nodes.
        Arguments:
            root: the root node of the tree, created before calling
            cells: The set of cells
            prev: the parent node, orignally passed as the root but
            passes as each current parent during recursion
        Return Values: returns None if empty.
        Pre-conditions: cells must not be empty
    '''
    if root is not None:
        parent_coords = root._coords
        up = tuple([parent_coords[0], parent_coords[1] - 1])
        if up in cells:
            root._up = MazeTreeNode(up)
            if root._up._coords != prev._coords:
                create_tree(root._up, cells, root)

        down = tuple([parent_coords[0], parent_coords[1] + 1])
        if down in cells:
            root._down = MazeTreeNode(down)
            if root._down._coords != prev._coords:
                create_tree(root._down, cells, root)

        left = tuple([parent_coords[0] - 1, parent_coords[1]])
        if left in cells and root._left != prev:
            root._left = MazeTreeNode(left)
            if root._left._coords != prev._coords:
                create_tree(root._left, cells, root)

        right = tuple([parent_coords[0] + 1, parent_coords[1]])
        if right in cells and root._right != prev:
            root._right = MazeTreeNode(right)
            if root._right._coords != prev._coords:
                create_tree(root._right, cells, root)
    else:
        return None

def print_tree(root, prev, indent):
    '''
        This function prints the paths of the tree in proper
        preorder traversal order and to the pattern of up, down,
        left, right. There are indentation lines added to represent
        the paths of traversal.
        Arguments:
            root: the root node of the tree, created before calling
            prev: the parent node, orignally passed as the root but
            passes as each current parent during recursion
            indent: the number of lines added before each pair ("| ")
            this starts as an empty string, but duplicates for each
            recursive call.
        Return Values: none
        Pre-conditions: dumpTree Called
    '''
    if root is not None:
        print("  " + indent + str(root._coords))
        if root._up is not None and root._up._coords != prev._coords:
            indent += "| "
            print_tree(root._up, root, indent)
            indent = indent[:-2]
        if root._down is not None and root._down._coords != prev._coords:
            indent += "| "
            print_tree(root._down, root, indent)
            indent = indent[:-2]
        if root._left is not None and root._left._coords != prev._coords:
            indent += "| "
            print_tree(root._left, root, indent)
            indent = indent[:-2]
        if root._right is not None and root._right._coords != prev._coords:
            indent += "| "
            print_tree(root._right, root, indent)
            indent = indent[:-2]
    else:
        return None

def solve_maze(root, prev, end_coord, end_path, maze_data, is_print):
    '''
        This function finds the path from the start to end of the maze
        and either prints the path when specified, or calls the
        solution_maze function to print a solved diagram of the maze.
        Arguments:
            root: the root node of the tree, created before calling
            prev: the parent node, orignally passed as the root but
            end_coord: the tuple of the end point coordinate
            end_path: an array that records each path, so that when the end
            is found it will be stored here.
            maze_data: 2D array of maze layout
            is_print: Boolean used only to determine if the solution will be
            printed as a list of coordinates or a graph of the solved maze.
        Return Values: returns None if empty.
        Pre-conditions: dumpSolution called
    '''
    if root is not None:
        if root._coords == end_coord:
            if is_print is True:
                print("PATH OF THE SOLUTION:")
                for pair in end_path:
                    print("  " + str(pair))
            else:
                solution_maze(maze_data, end_path)

            return end_path
        if root._up is not None and root._up._coords != prev._coords:
            solve_maze(root._up, root, end_coord, end_path +
                       [root._up._coords], maze_data, is_print)
        if root._down is not None and root._down._coords != prev._coords:
            solve_maze(root._down, root, end_coord, end_path +
                       [root._down._coords], maze_data, is_print)
        if root._left is not None and root._left._coords != prev._coords:
            solve_maze(root._left, root, end_coord, end_path +
                       [root._left._coords], maze_data, is_print)
        if root._right is not None and root._right._coords != prev._coords:
            solve_maze(root._right, root, end_coord, end_path +
                       [root._right._coords], maze_data, is_print)
    else:
        return

def solution_maze(maze_data, end_path):
    '''
        This function prints the new maze with the solution path
        represented as periods.
        Arguments:
            end_path: an array that records each path, so that when the end
            is found it will be stored here.
            maze_data: 2D array of maze layout
        Return Values: None
        Pre-conditions: empty line called as command.
    '''
    y = 0
    new_maze = []
    for row in maze_data:
        temp_row = []
        for x in range(len(row)):
            cur_coords = tuple([x, y])
            cur_char = maze_data[y][x]
            if cur_coords in end_path and cur_char != "S" \
               and cur_char != "E":
                temp_row.append(".")
            else:
                temp_row.append(cur_char)
        new_maze.append(temp_row)
        y += 1
    print("SOLUTION:")
    for line in new_maze:
        row_contents = ""
        for char in line:
            row_contents += char
        print(str(row_contents))
main()