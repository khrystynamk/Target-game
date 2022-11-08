"""English target game"""
import string
import random
import sys
from typing import List

def generate_grid() -> List[List[str]]:
    """
    Generates list of lists of letters - i.e. grid for the game.
    e.g. [['D', 'G', 'E'], ['W', 'F', 'S'], ['J', 'M', 'G']]
    """
    grid = []
    letters = string.ascii_uppercase
    for line in range(3):
        grid.append([])
        string_of_letters = ''.join(random.choice(letters) for i in range(3))
        grid[line] = [x for x in string_of_letters]
    return grid

def check_word_suitable(word: str, central_letter: str, letters: List[str]) -> bool:
    """
    Checks the word according to the rules.
    """
    is_word_suitable = True
    if len(word) in range(4, 10) and central_letter in word:
        letters_map = []
        for letter in letters:
            letter_in_map = list(filter(lambda item: item[0] == letter, letters_map))
            if len(letter_in_map) < 1:
                letters_map.append((letter, letters.count(letter)))

        for letter in word:
            letter_occurances_in_word = word.count(letter)
            letter_in_map = list(filter(lambda item: item[0] == letter \
                     and item[1] >= letter_occurances_in_word, letters_map))
            if len(letter_in_map) < 1:
                is_word_suitable = False
    else:
        is_word_suitable = False

    return is_word_suitable

def get_words(f_dict: str, letters: List[str]) -> List[str]:
    """
    Reads the file f. Checks the words with rules and returns a list of words.
    """
    list_of_words = []
    central_letter = letters[len(letters) // 2]
    with open(f_dict, 'r', encoding='utf-8') as file:
        next(file)
        next(file)
        next(file)
        for word in file:
            word = word.strip().lower()
            if check_word_suitable(word, central_letter, letters):
                list_of_words.append(word)
    return list_of_words

def get_user_words() -> List[str]:
    """
    Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish for *nix or Ctrl-Z+Enter
    for Windows.
    Note: the user presses the enter key after entering each word.
    """
    user_words = []
    print('Press CTRL + D (Unix) or CTRL + Z (Windows) to exit')
    user_words = sys.stdin.read().splitlines()

    return user_words

def get_pure_user_words(
    user_words: List[str],
    letters: List[str],
    words_from_dict: List[str]
    ) -> List[str]:
    """
    (list, list, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.
    """
    words_not_in_dictionary = []
    central_letter = letters[len(letters) // 2]
    for user_word in user_words:
        if user_word not in words_from_dict and\
                check_word_suitable(user_word, central_letter, letters):
            words_not_in_dictionary.append(user_word)
    return words_not_in_dictionary

def get_correct_user_words(
        user_words: List[str],
        letters: List[str],
        words_from_dict: List[str]
    ) -> List[str]:
    """
    (list, list, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.
    """
    correct_user_words = []
    central_letter = letters[len(letters) // 2]
    for user_word in user_words:
        if user_word in words_from_dict and check_word_suitable(user_word, central_letter, letters):
            correct_user_words.append(user_word)
    return correct_user_words

def write_results_to_file(list_of_words, correct_user_words, words_not_in_dictionary):
    """
    Write results into a file.
    """
    with open('result.txt', 'w', encoding = 'utf-8') as file:
        file.write(f'Number of correct words: {len(correct_user_words)}')
        file.write(f'All words: {", ".join(list_of_words)}')
        file.write(f'Words that the player 'f'missed:\
         {", ".join(set(list_of_words) - set(correct_user_words))}')
        file.write(f'Words the player entered and that are not 'f'present in the dictionary:\
         {", ".join(words_not_in_dictionary)}')

def results():
    """
    Output the results of the game.
    """
    grid = generate_grid()
    print(grid)
    print('Please enter your words.')
    user_words = get_user_words()
    letters_list = []
    list(map(letters_list.extend, grid))
    letters = [y.lower() for y in letters_list]
    list_of_words = get_words('en.txt', letters)
    correct_user_words = get_correct_user_words(user_words, letters, list_of_words)
    words_not_in_dictionary = get_pure_user_words(user_words, letters, list_of_words)
    print(f'Number of correct words: {len(correct_user_words)}')
    print(f'All words: {", ".join(list_of_words)}')
    print(f'Words that the player 'f'missed:\
     {", ".join(set(list_of_words) - set(correct_user_words))}')
    print(f'Words the player entered and that are not 'f'present in the dictionary:\
     {", ".join(words_not_in_dictionary)}')
