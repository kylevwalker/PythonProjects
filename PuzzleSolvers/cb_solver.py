""" ---------------------------------------------------------------------------
    File: cb_solver.py
    Author: Kyle Walker
    Purpose: This program takes a string that represents a "Cracker Barrel" peg
             game board and allows for various functions to be called. These
             functions will help to solve the game, show solutions, print a
             visualization of the board, and get all possible moves from the
             current board. There is a cb_one function that gives one possible
             solution of the many possible, and there is a cb_all function
             which gives every possible set of moves to solve the board with
             only one "peg" remaining.

"""

def print_board(board):
    '''
        This function prints the contents of the board as a more easily
            recognizable pyramid shaped board. The empty spots are shown as
            "0" and the pegs are shown as "1".
        Arguments:
            board: The string representing the pegs on the board. This is
                15 characters long, going from top to bottom and left to right
                on the board as an encoded string.
        Return Values:
            None
        Pre-conditions: board must be a string of 15 characters
    '''
    print("    " + board[0])
    print("   " + board[1] + " " + board[2])
    print("  " + board[3] + " " + board[4] + " " + board[5])
    print(" " + board[6] + " " + board[7] + " " + board[8] + " " + board[9])
    print(board[10] + " " + board[11] + " " +
          board[12] + " " + board[13] + " " + board[14])

def get_all_conceivable_moves():
    '''
        This function returns a hardcoded set of all concievable moves on the
        board.
            Because the shape of the board is not applicable to a linear
            string, these tuples show the possible moves that can be made
            from each peg.
        Arguments:
            None
        Return Values:
            all_moves: The set of all hardcoded tuples, representing all
            possible moves
                at all pegs.
        Pre-conditions: None
    '''
    all_moves = set([(0, 1, 3), (0, 2, 5),
                    (1, 3, 6), (1, 4, 8),
                    (2, 4, 7), (2, 5, 9),
                    (3, 1, 0), (3, 4, 5), (3, 6, 10), (3, 7, 12),
                    (4, 7, 11), (4, 8, 13),
                    (5, 2, 0), (5, 9, 14), (5, 8, 12), (5, 4, 3),
                    (6, 3, 1), (6, 7, 8),
                    (7, 4, 2), (7, 8, 9),
                    (8, 7, 6), (8, 4, 1),
                    (9, 8, 7), (9, 5, 2),
                    (10, 6, 3), (10, 11, 12),
                    (11, 7, 4), (11, 12, 13),
                    (12, 11, 10), (12, 7, 3), (12, 8, 5), (12, 13, 14),
                    (13, 12, 11), (13, 8, 4),
                    (14, 13, 12), (14, 9, 5)])
    return all_moves

def get_moves(board):
    '''
        This function returns all possible moves based on the current board.
        It refers to the all_moves set to check if the moves follow the
        rules of the game and shape of the board.
        Arguments:
            board: The string representing the pegs on the board. This is
                15 characters long, going from top to bottom and left to right
                on the board as an encoded string.
        Return Values:
            possible_moveset: a sorted set of all possible moves at the current
            board.
        Pre-conditions: board must be 15 char string containing only "1" and
        "0"
    '''
    all_moves = get_all_conceivable_moves()
    possible_moveset = set()
    for peg in range(0, 15):
        for move in all_moves:
            start = move[0]
            skip = move[1]
            end = move[2]
            if peg == start:
                if board[peg] == "1" and board[skip] == "1" and \
                   board[end] == "0":
                    possible_move = (start, skip, end)
                    possible_moveset.add(possible_move)
    return sorted(possible_moveset)

def cb_one(board):
    '''
        This function solves for one possible solution and returns the set of
            moves.
        Arguments:
            board: The string representing the pegs on the board. This is
                15 characters long, going from top to bottom and left to right
                on the board as an encoded string.
        Return Values:
            move: the array of moves used to solve the game
        Pre-conditions: board must be 15 char string containing only "1" and
        "0"
    '''
    possible_moves = get_moves(board)

    for move in possible_moves:
        new_board = list(board)
        new_board[move[0]] = '0'
        new_board[move[1]] = '0'
        new_board[move[2]] = '1'

        peg_count = 0
        for char in new_board:
            if char == '1':
                peg_count += 1
        if peg_count == 1:
            return [move]
        else:
            next_move = cb_one(new_board)
            if next_move is not None:
                return [move] + next_move

def cb_all(board):
    '''
        This is the outside function to solve for all solutions.
        Arguments:
            board: The string representing the pegs on the board. This is
                15 characters long, going from top to bottom and left to right
                on the board as an encoded string.
        Return Values:
            all_solutions: Set of all solutions found
        Pre-conditions: board must be 15 char string containing only "1" and
        "0"
    '''
    all_solutions = []
    cb_all_check(board, all_solutions)
    return all_solutions

def cb_all_check(board, solutions):
    '''
        This is the inside recursive function to solve for all solutions.
        Arguments:
            board: The string representing the pegs on the board. This is
                15 characters long, going from top to bottom and left to right
                on the board as an encoded string.
            solutions: an array of current moves to be added.
        Return Values:
            all_solutions: Set of all solutions found
        Pre-conditions: board must be 15 char string containing only "1" and
        "0"
    '''
    possible_moves = get_moves(board)

    for move in possible_moves:
        new_board = list(board)
        new_board[move[0]] = '0'
        new_board[move[1]] = '0'
        new_board[move[2]] = '1'

        peg_count = 0
        for char in new_board:
            if char == '1':
                peg_count += 1
        if peg_count == 1:
            solutions.append([move])
            return
        else:
            next_move = cb_all_check(new_board, solutions)
            if next_move is not None:
                return [move] + next_move

