""" ---------------------------------------------------------------------------
    File: rhymes.py
    Author: Kyle Walker
    Purpose: This program stores a pronunciation dictionary from an input file
            and uses the end pronunciation of words to find perfect rhymes. In
            a perfect rhyme, the entire ending pronunciation must be the same
            in both words and the preceding phoneme must not be the same. This
            program will accept words and display all perfect rhymes found in
            the given pronunciation dictionary. If a word has more than one
            way to pronounce it, rhymes for both pronunciations will be shown.
"""


def main():
    file_name = input()
    file = open(file_name, "r")
    pron_dict = dict()
    # Converts file into dictionary with words as keys and pronunciations as
    # a list in the value. If a word has another pronunciation, the duplicate
    # will be stored as a separate key with a "!" in its name.
    for line in file:
        line = line.split()
        if line[0] in pron_dict:
            pron_dict[line[0] + "!"] = line[1:]
        else:
            pron_dict[line[0]] = line[1:]
    # Loop for word prompt, and calling function to find rhymes
    while True:
        try:
            word = input()
            if word == "":
                print("No word given \n")
            elif len(word.split()) > 1:
                print("Multiple words entered, please enter "
                      "only one word at a time. \n")
            else:
                word = word.upper()
                rhyming_words = set()
                print("Rhymes for: " + word)
                # Calls function once for multiple pronunciation word
                if word + "!" in pron_dict:
                    rhyming_words = search(pron_dict, word.strip("!"))
                # Calls function if word is known in dictionary
                if word in pron_dict:
                    rhyming_words = search(pron_dict, word)
                # If word is unknown or no rhymes are returned, prints none
                if len(rhyming_words) == 0:
                    print("  -- none found --")
                else:
                    for words in sorted(rhyming_words):
                        print("  " + words)
        except EOFError:
            break

def search(pron_dict, word):
    '''
        This function finds the primary stress of the word, the phoneme
        found before the primary stress, and compares these to all values
        in the pronunciation dictionary. If a value follows the perfect
        rhyme rules, it will store the word in the rhyme set.
        Arguments: pron_dict: The total pronunciation dictionary created
        from the input file.
        word: The capitalized word used to base the rhyme pattern on.
        Returns: rhyming_words: The oset of all words that perfectly
        rhyme with the word parameter.
        PreCondtions: The word parameter or its alternate pronunciation
        must be in the pron_dict, so that the rhyme pattern can be found.
    '''
    word_pron = pron_dict[word]
    i = 0
    rhyming_words = set()
    # Checks for the primary stress, indicated by a "1". The index is saved to
    # remember the location of the primary stress in the word_pron array.
    while i < len(word_pron):
        if "1" in word_pron[i]:
            primary_stress = i
            break
        else:
            primary_stress = 0
            i += 1
    # The previous phoneme is found by indexing one space before the stress
    prev_phoneme = word_pron[primary_stress - 1]
    # This prevents words like "And", which do not have a previous phenome,
    # from passing through function.
    if primary_stress > 0:
        rhyme_pattern = word_pron[primary_stress:]
        pattern_length = len(rhyme_pattern)
        for key, value in pron_dict.items():
            # Compares the ending of the word with the rhyme pattern by slicing
            if value[len(value) - pattern_length:] == rhyme_pattern:
                # Checks if previous phoneme is not the same, and also that the
                # compared word is long enough to contain a previous phoneme
                if value[len(value) - pattern_length - 1] != prev_phoneme and \
                   len(value) != pattern_length:
                    # Removes the duplicate indication character
                    if "!" in key:
                        key = key[:-1]
                    rhyming_words.add(key)
    return rhyming_words


main()