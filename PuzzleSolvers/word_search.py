''' --------------------------------------------------------------------------
    File: word_search.py
    Author: Kyle Walker
    Purpose: This program aks the user for a text document in the format of a
            grid of scrambled words, and a set of words to search for. The
            program will run through every character in the grid and check the
            characters surrounding it in every direction, then iterate through
            the grid in each of the eight directions searching for the word.
            If the word is found, it's location will be recorded on the output
            grid.
    Course: CSC 120, spring 2021
    Format:
        Input txt file must match following format, where words are arranged in grid and word to find are listed below after a space:
                dgsomafh
                pabprswb
                qwrgfytm
                koyozrot
                urekvnif
                ldfhzdrg
                ispeegay
                etytmtlm
                qbyeivpg

                two
                words
'''
import os
import copy

def main():
    try:
        print("Please give the puzzle filename:")
        file_name = input()
        file = open(file_name, "r")
    except FileNotFoundError:
        print("Sorry, the file doesn't exist or cannot be opened.")
        os._exit(0)

    grid = []
    word_list = []
    grid_section = True


    for line in file:
        line = line.strip("\n")
        if line == '':
            grid_section = False
        elif grid_section is True:
            grid.append(list(line))
        elif grid_section is False:
            word_list.append(str(line))

    answer_key = []
    char_check(grid, word_list, answer_key)


def char_check(grid, word_list, answer_key):
    '''
        This function iterates through every character in the grid and
        calls the word search function every time the first character of
        the word matches the character in the grid.
        Arguments: grid = 2D array of all chars in the scrambled word grid.
        word_list = list of the words to be searched for.
        answer_key = list of coordinate tuples used in output graph.
        Return Values: None
        Pre-conditions: grid and word list must contain at least one row
        and string respectively.
    '''

    word_number = 0
    found_words = []
    while word_number < len(word_list):
        #found_ = False
        current_word = word_list[word_number]
        y = 0
        while y < len(grid):
            x = 0
            while x < len(grid[0]):
                if str(grid[y][x]) == str(current_word[0]):
                    word_search(x, y, grid, word_list, current_word, answer_key, found_words)

                x += 1
            y += 1
        word_number += 1
        if current_word not in found_words:
            print("Word " + "'" + current_word + "'" + " not found \n")
def word_search(x, y, grid, word_list, current_word, answer_key, found_words):
    '''
        Uses 8 directional combinations to iterate through the grid,
        storing the coordinates of the found words.
        Arguments: x = the column or x coordinate of the grid.
        y = the row or y coordinate of the grid.
        grid = 2D array of all chars in the scrambled word grid.
        word_list = list of the words to be searched for.
        current_word = current element of word_list, the word currently
        being searched for.
        answer_key = list of coordinate tuples used in output graph.
        found_words = list of words found in search.
        Return Values: None
        Pre-conditions: Only called if the coordinate in the grid
        matches the first character of the current word.
    '''
    steps = len(current_word)

    for j in range(8):
        temp_word = ""
        temp_coords = []
        answer_key = []
        i = 0
        while i < steps:
            try:
                # j is used as a counter for each direction in no
                # particular order. The while j loop helps condense
                # the 8 repeating loops into one as they all follow
                # the same structure but use different x and y offsets
                if j == 1:
                    temp_word += grid[y][x + i]
                    temp_coords.append((y, x + i))
                if j == 2:
                    temp_word += grid[y][x - i]
                    temp_coords.append((y, x - i))
                if j == 3:
                    temp_word += grid[y - i][x]
                    temp_coords.append((y - i, x))
                if j == 4:
                    temp_word += grid[y + i][x]
                    temp_coords.append((y + i, x))
                if j == 5:
                    temp_word += grid[y - i][x - i]
                    temp_coords.append((y - i, x - i))
                if j == 6:
                    temp_word += grid[y + i][x + i]
                    temp_coords.append((y + i, x + i))
                if j == 7:
                    temp_word += grid[y - i][x + i]
                    temp_coords.append((y - i, x + i))
                if j == 8:
                    temp_word += grid[y + i][x - i]
                    temp_coords.append((y + i, x - i))

                if temp_word == current_word:
                    #found = True
                    found_words.append(current_word)
                    answer_key = temp_coords
                    word_plotter(grid, word_list, answer_key, current_word)
            except IndexError:
                break
            i += 1


def word_plotter(grid, word_list, answer_key, current_word):
    '''
        Checks for which coordinates of the grid are not part of the
        found words and replaces them with a period symbol. Then
        displays the answer graph.
        Arguments: grid = 2D array of all chars in the scrambled word grid.
        word_list = list of the words to be searched for.
        answer_key = list of coordinate tuples used in output graph.
        current_word = current element of word_list, the word currently
        Return Values: None
        Pre-conditions: None
    '''
    solved_grid = copy.deepcopy(grid)

    row = 0
    while row < len(solved_grid):
        col = 0
        while col < len(solved_grid[row]):
            if (row, col) not in answer_key:
                solved_grid[row][col] = "."
            col += 1
        row += 1
    for line in solved_grid:
        line = ''.join(line)
        print(line)
        if line == "":
            print()
            break

main()