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
    word = random.choice(secret_words)
    unused_chars = []
    game_rounds = 0
    response = [" Genius!", " Magnificent!", " Impressive!", " Splendid!", " Great!", " Phew!"]
    game_word = ""
    for i in range(65, 91):
        unused_chars.append(chr(i))
    while game_rounds < 6:
        guess = input("\nEnter your guess. A 5 letter word: ").upper()
        current_choice = ["-", "-", "-", "-", "-"]
        visited = [False, False, False, False, False]
        if len(guess) != 5 or guess not in all_words:
            print(guess + " is not a valid word. Please try again.")
            continue
        game_word = make_guess(guess, word, unused_chars, visited, current_choice, game_word)
        if guess == word:
            print("\nYou win." + response[game_rounds])
            break
        game_rounds += 1
    if game_rounds == 6:
        print("\nNot quite. The secret word was " + word + ".")
    if input("\nDo you want to play again? Type Y for yes: ").upper() == "Y":
        play_game(secret_words, all_words)


def make_guess(guess, word, unused_chars, visited, current_choice, game_word):
    for i in range(5):
        if guess[i] in unused_chars:
            unused_chars.remove(guess[i])
        if guess[i] == word[i]:
            visited[i] = True
            current_choice[i] = "G"
    for i in range(5):
        if (guess[i] in word and not visited[word.index(guess[i])]
                and current_choice[i] == "-"):
            visited[word.index(guess[i])] = True
            current_choice[i] = "O"
    game_word += ("\n" + current_choice[0] + current_choice[1] +
                  current_choice[2] + current_choice[3] + current_choice[4])
    game_word += "\n" + guess
    unused_word = "Unused letters: "
    for letter in unused_chars:
        unused_word += letter + " "
    print(game_word)
    print("\n" + unused_word)
    return game_word


if __name__ == '__main__':
    main()
