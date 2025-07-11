"""
Guess a 5 letter word within six guesses

Word list found at: https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93#file-valid-wordle-words-txt
"""

from typing import List

# Module used by recommendation of https://stackoverflow.com/a/306417
import random

# Module found at https://stackoverflow.com/a/293633
from termcolor import colored

guess_counter = 0
WORD_LENGTH = 5

guesses = ["     ", 
           "     ",
           "     ", 
           "     ", 
           "     ", 
           "     "]
letter_to_box_map = {
    'A': '🄰',
    'B': '🄱',
    'C': '🄲',
    'D': '🄳',
    'E': '🄴',
    'F': '🄵',
    'G': '🄶',
    'H': '🄷',
    'I': '🄸',
    'J': '🄹',
    'K': '🄺',
    'L': '🄻',
    'M': '🄼',
    'N': '🄽',
    'O': '🄾',
    'P': '🄿',
    'Q': '🅀',
    'R': '🅁',
    'S': '🅂',
    'T': '🅃',
    'U': '🅄',
    'V': '🅅',
    'W': '🅆',
    'X': '🅇',
    'Y': '🅈',
    'Z': '🅉',
    ' ': '☐'
}

def display_guesses(guesses: List[str]) -> None:
    """
    Display the guesses in the following format:

    [] [] [] [] []
    [] [] [] [] []
    [] [] [] [] []
    [] [] [] [] []
    [] [] [] [] []

    Args:
    - guesses (List[str]): The list of player guesses so far

    Return:
    - None
    """
    # Clear terminal first (solution found at: https://stackoverflow.com/a/70387199)
    print("\033c\033[3J")

    # Convert each guess to colored box version
    for guess in guesses:
        print(color_text(key_word, guess))


def color_text(key_word: str, guess: str) -> str:
    """
    Add color (if necessary) to each letter based on three conditions:
    - No color: for placeholders (spaces)
    - Light Red: letter does not exist in word
    - Yellow: letter is in word but not in current position
    - Green: letter is in word and in current position

    Args:
    - key_word (str): the correct word to guess
    - guess (str): the word being guessed and to be colored; not in box letters

    Return:
    - colored_text (str): The potentially colored box version of guess
    """

    # Edge case: the guess is actually just a placeholder
    if guess == "     ":
        sub_string = letter_to_box_map[" "] + " "
        return sub_string * 5

    # Hold the potentially colored text
    colored_text = ""

    # Go through each letter
    for index in range(WORD_LENGTH):
        # Extract the letter at the index for the key_word
        key_letter = key_word[index]

        # Extract and convert the letter at the index for the guess
        guess_letter = guess[index]
        box_letter = letter_to_box_map[guess_letter]

        # Check if guess_letter is even in the word
        if guess_letter not in key_word:
            colored_text += colored(box_letter, "light_red")

        else:
            # Yellow if not in right position
            if guess_letter != key_letter:
                colored_text += colored(box_letter, "yellow")
            # Green otherwise
            else:
                colored_text += colored(box_letter, "green")

        
        # If there are too many spaces, comment the line below
        colored_text += " "

    return colored_text


def guess_is_valid(guess: str) -> bool:
    """
    Checks if the guess meets both conditions:
    - has exactly 5 letters
    - has only letters

    Args:
    - guess (str): the user guess to validate

    Return:
    - a boolean based on validity (valid -> True, invalid -> False)
    """

    # Check if has 5 characters
    if len(guess) != 5:
        return False
    
    # Check if the letters are valid
    possible_letters = list(letter_to_box_map.keys())[:-1]
    for letter in guess:
        if letter not in possible_letters:
            return False
        
    # Passed both checks, good to go
    return True


def select_valid_word() -> str:
    """
    Selects a random word from words.txt

    Args:
    - None

    Return:
    - a word to be used as the key_word (str)
    """

    with open("words.txt", "r") as input_file:
        words = input_file.readlines()

    return random.choice(words).upper()


# Store the key word
key_word = select_valid_word()

# Play until guess_counter hits 6
while guess_counter < 6:
    # Display the guesses so far
    display_guesses(guesses)

    # Take the user guess, force 5 letter words
    user_guess = input("Enter your guess: ").upper()

    # Validate the input
    while not guess_is_valid(user_guess):
        print(colored("Your guess must only contain letters and be exactly five letters long", "red"))
        user_guess = input("Enter your guess: ").upper()

    # Replacing the placeholder with the guess
    guesses[guess_counter] = user_guess

    # Check the guess
    if user_guess == key_word:
        break
    else:
        guess_counter += 1


# Display the final board
display_guesses(guesses)

# Display the final word
print(f"The word was: {key_word}")
