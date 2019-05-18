# represents the game (including the menu)

import sys
import game
import random
import string_database


class guess:
    user_word = ['-', '-', '-', '-']
    correct_word = []

    def __init__(self, round_no):
        self.menu()
        self.select_random_string()
        self.choose_option()
        self.round = round_no + 1

    def menu(self):
        print("Current Guess: ---- \n")
        print("g = guess, t = tell me, l for a letter, and q to quit")

    # function to select random string
    def select_random_string(self):
        guess.correct_word = list(string_database.get_db().get_word(
            random.randint(0, 4029)))
        print(guess.correct_word)

    # function to handle choosen option
    def choose_option(self):
        user_input = input()
        if user_input.lower() == 'g':
            # we take a guess
            # print("we guess the full word"+"".join(guess.user_word))
            self.string_guess()
        elif user_input.lower() == 't':
            # we tell the answer
            self.round_end_message(0)
        elif user_input.lower() == 'l':
            # we give a letter
            print("we guess one character")
            self.char_guess()
        elif user_input.lower() == 'q':
            end_game()

    def string_guess(self):
        user_guess = input("enter a four letter word: ")

        if len(user_guess) > 4 or len(user_guess) < 4:
            print("please choose a four letter word, lets try that again")
            self.string_guess()

        if list(user_guess) == guess.correct_word:
            self.round_end_message(1)
        else:
            # deduct 10% from total score
            print("Incorrect guess. lets try that again")
            self.string_guess()

    def char_guess(self):
        user_guess = input("enter a letter: ")

        if len(user_guess) > 1 or len(user_guess) < 1:
            print("please choose a one letter word, lets try that again")
            self.char_guess()

        if user_guess in guess.correct_word:
            print("we just flipped one ")
            for x in range(len(guess.correct_word)):
                if guess.correct_word[x] == user_guess:
                    guess.user_word[x] = user_guess
                    print(guess.user_word)

            if guess.correct_word == guess.user_word:
                self.round_end_message(1)
            else:
                self.menu()
                self.choose_option()
        else:
            # deduct score accordingly
            print("this letter is not contained in the word")
            print("wrong guess, please try again")
            self.char_guess()

    def round_end_message(self, status):
        if status == 1:
            print("You guessed the right answer. it was truely " +
                  "".join(guess.correct_word))
        else:
            print("Dont give up next time.the right answer was " +
                  "".join(guess.correct_word))

    def score_keeper(self):
        # find_total()
        pass


def main():
    print("** The great guessing game ** \n")

    for x in range(100):
        guess(x)

    print("you are a legend, you have finished the 100th round...")
    # game_stats()


def end_game():
    sys.exit()


main()
