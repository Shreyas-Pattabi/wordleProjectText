# Name: Shreyas Pattabi
# UTEID: sp54486
#
# On my honor, Shreyas Pattabi, this programming assignment is my own work
# and I have not provided this code to any other student.

import random


def main():
    """ Plays a text based version of Wordle.
        1. Read in the words that can be choices for the secret word
        and all the valid words. The secret words are a subset of
        the valid words.
        2. Explain the rules to the player.
        3. Get the random seed from the player if they want one.
        4. Play rounds until the player wants to quit.
    """
    secret_words, all_words = get_words()
    welcome_and_instructions()
    play_game(secret_words, all_words)


def welcome_and_instructions():
    """
    Print the instructions and set the initial seed for the random
    number generator based on user input.
    """
    print('Welcome to Wordle.')
    instructions = input('\nEnter y for instructions, anything else to skip: ')
    if instructions == 'y':
        print('\nYou have 6 chances to guess the secret 5 letter word.')
        print('Enter a valid 5 letter word.')
        print('Feedback is given for each letter.')
        print('G indicates the letter is in the word and in the correct spot.')
        print('O indicates the letter is in the word but not that spot.')
        print('- indicates the letter is not in the word.')
    set_seed = input(
        '\nEnter y to set the random seed, anything else to skip: ')
    if set_seed == 'y':
        random.seed(int(input('\nEnter number for initial seed: ')))


def get_words():
    """ Read the words from the dictionary files.
        We assume the two required files are in the current working directory.
        The file with the words that may be picked as the secret words is
        assumed to be names secret_words.txt. The file with the rest of the
        words that are valid user input but will not be picked as the secret
        word are assumed to be in a file named other_valid_words.txt.
        Returns a sorted tuple with the words that can be
        chosen as the secret word and a set with ALL the words,
        including both the ones that can be chosen as the secret word
        combined with other words that are valid user guesses.
    """
    temp_secret_words = []
    with open('secret_words.txt', 'r') as data_file:
        all_lines = data_file.readlines()
        for line in all_lines:
            temp_secret_words.append(line.strip().upper())
    temp_secret_words.sort()
    secret_words = tuple(temp_secret_words)
    all_words = set(secret_words)
    with open('other_valid_words.txt', 'r') as data_file:
        all_lines = data_file.readlines()
        for line in all_lines:
            all_words.add(line.strip().upper())
    return secret_words, all_words


def play_game(secret_words, all_words):
    """
    Selects a random word in secret_words as the target. Starts the game
    by allowing users to guess valid words. A valid word is any word
    that exists in all_words. It outputs the status of the guess against
    the target after each guess and maintains a record of the previous
    guesses. It allows up to 6 guesses to get the target word.
    :param secret_words: list of secret words. Subset of all_words
    :param all_words: list of all valid guesses
    :return: void
    """
    word = random.choice(secret_words)
    unused_chars = []
    game_rounds = 0
    response = [" Genius!", " Magnificent!", " Impressive!",
                " Splendid!", " Great!", " Phew!"]
    game_word = ""
    for i in range(65, 91):
        unused_chars.append(chr(i))
    while game_rounds < 6:
        guess = input("\nEnter your guess. A 5 letter word: ").upper()
        current_choice = ["-", "-", "-", "-", "-"]
        visited = [False, False, False, False, False]
        if guess not in all_words:
            print("\n" + guess + " is not a valid word."
                                 " Please try again.")
            continue
        game_word = make_guess(guess, word, unused_chars, visited,
                               current_choice, game_word)
        if guess == word:
            print("\nYou win." + response[game_rounds])
            break
        game_rounds += 1
    if game_rounds == 6:
        print("\nNot quite. The secret word was " + word + ".")
    again = input("\nDo you want to play again? Type Y for yes: ")
    again = again.upper()
    if again == "Y":
        play_game(secret_words, all_words)


def make_guess(guess, word, unused_chars, visited, current_choice, game_word):
    """
    Method for making the guess. Uses and updates all the relevant
    parameters and returns the most updated version of game_word.
    :param guess: The user's guess word
    :param word: The target word
    :param unused_chars: List of characters that have not been used
    :param visited: List that marks when a letter in the target has
    been compared against a character in the guess
    :param current_choice: List that maintains the status of the guess.
    G for letter match, O for letter exists in target but not a match,
    dash for letter is not in target
    :param game_word: is the string that keeps a record of all the
    guesses
    :return: game_word updated with the newest guess
    """
    for i in range(5):
        if guess[i] in unused_chars:
            unused_chars.remove(guess[i])
        if guess[i] == word[i]:
            visited[i] = True
            current_choice[i] = "G"
    for i in range(5):
        if guess[i] in word and current_choice[i] == "-":
            for j in range(5):
                if word[j] == guess[i] and not visited[j]:
                    visited[j] = True
                    current_choice[i] = "O"
                    break
    game_word += "\n"
    for i in range(5):
        game_word += current_choice[i]
    game_word += "\n" + guess
    unused_word = "Unused letters:"
    for letter in unused_chars:
        unused_word += " " + letter
    print(game_word)
    print("\n" + unused_word)
    return game_word


if __name__ == '__main__':
    main()
