# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Bogdan Zadorozhny
# Collaborators : -
# Time spent    : ~4 hours

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
WILDCARD = '*'
GAME_OVER = '!!'

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

    The score for a word is the product of two components:

    The first component is the sum of the points for letters in the word.
    The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    letters_amount = len(word)
    first_score = 0
    second_score = HAND_SIZE * letters_amount - 3 * (n - letters_amount)

    if second_score < 1:
        second_score = 1

    for i in word.lower():
        first_score += SCRABBLE_LETTER_VALUES.get(i, 0)

    scores = first_score * second_score
    return scores


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    print("Current hand:", end=" ")

    for letter in hand.keys():
        for _ in range(hand[letter]):
            print(letter, end=' ')
    print()


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {WILDCARD: 1}
    num_vowels = int(math.ceil(n / 3) - 1)

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()

    for letter in word.lower():
        if letter in new_hand:
            new_hand[letter] -= 1

    for letter in hand:
        if new_hand[letter] <= 0:
            new_hand.pop(letter)

    return new_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = word.lower()

    for letter in word:
        if letter not in hand or word.count(letter) > hand[letter]:
            return False

    for vowel in VOWELS:
        normal_word = word.replace(WILDCARD, vowel)

        if normal_word in word_list:
            return True

    return False


def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """
    length = sum(hand.values())
    return length


def ask_user(text, warning_text, checker):
    """
    text: message for input
    warning_text: warning message
    checker: validation conditions
    returns: value of variable
    """
    while True:
        variable = input(text)

        if checker(variable):
            break

        print(warning_text)
    return variable


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """
    total_score = 0

    # As long as there are still letters left in the hand
    while calculate_handlen(hand) > 0:
        hand_length = calculate_handlen(hand)

        # Display the hand
        display_hand(hand)

        # Ask user for input
        word = input('Enter word, or "!!" to indicate that you are finished: ')

        # If the input is two exclamation points, the game is over
        if word == GAME_OVER:
            break
        # Otherwise (the input is not two exclamation points):
        else:

            # If the word is valid, program tells the user how many points the word earned, and the updated total score
            if is_valid_word(word, hand, word_list):
                score = get_word_score(word, hand_length)
                total_score += score
                print(f'"{word}" earned {score} points. Total: {total_score} points')
            # Otherwise (the word is not valid), program shows a message
            else:
                print("This is not a valid word. Please choose another word.")

            # Then program updates the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)
        print()

    # Game is over (user entered '!!' or ran out of letters), so program tells user the total score
    if word != GAME_OVER:
        print("Ran out of letters.")

    print("Total score for this hand:", total_score)
    print("-" * 8)

    return total_score


def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()

    if letter in hand:
        letters = string.ascii_lowercase

        for el in hand:
            letters = letters.replace(el, "")

        new_letter = random.choice(letters)
        new_hand[new_letter] = new_hand[letter]
        del new_hand[letter]

    return new_hand


def substitution_offer(substitution, replay_hand, hand):
    """
        substitution: string
        replay_hand: string
        hand: dictionary (string -> int)
        returns: dictionary (string -> int)
    """
    # If the substitution and replay hand aren't used, the program asks user to use substitution
    if substitution and replay_hand != 'use':
        substitution = ask_user("Would you like to substitute a letter? ", "You have to enter yes or no.",
                                lambda x: x in ('yes', 'no'))

        # If user uses substitution, the program asks which letter he would like to replace and launches
        # substitution_hand function
        if substitution == 'yes':
            letter = (ask_user("Which letter would you like to replace: ", "You have to enter a letter.",
                               lambda x: x in string.ascii_letters)).lower()
            hand = substitute_hand(hand, letter)
            substitution = False
        print()
    return hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    game_score = 0
    substitution = True
    replay_hand = ''
    replay_hand_used = False
    hand = deal_hand(HAND_SIZE)
    # Ask user for input
    hands_number = int(ask_user("Enter total number of hands: ", "You have to enter an integer.",
                                lambda x: x.isdecimal() and int(x) > 0))

    # This loop works, while amount of hands isn't over
    while hands_number != 0:

        # Display the hand
        display_hand(hand)
        print()

        # Then program asks user to substitute a letter
        hand = substitution_offer(substitution, replay_hand, hand)

        # Then program counts round score and total game score, and shows this information
        game_score += play_hand(hand, word_list)

        # If the "replay hand" isn't used, the program asks user to use "replay hand"
        if not replay_hand_used:
            replay_hand = ask_user("Would you like to replay the hand? ", "You have to enter yes or no.",
                                   lambda x: x in ('yes', 'no'))

        # If user uses "replay hand", the program starts the next round with the same hand
        if replay_hand != 'yes':
            hands_number -= 1
            hand = deal_hand(HAND_SIZE)
            replay_hand = 'used'

        # Otherwise, the program the program starts the next round with the new hand
        else:
            replay_hand = 'use'
            replay_hand_used = True

    print("Total score over all hands:", game_score)
    return


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
