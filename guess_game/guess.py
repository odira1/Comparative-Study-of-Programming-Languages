# represents the game (including the menu)

from importlib import reload
import sys
import random
import string_database
import game


class guess():
    """
    guess contains all data and object to ensure the that the game runs.
    It uses both the game module and string_database module to create objects 
    that are necessary for this game
    """
    games = []
    total_score = 0
    total_letter_guesses = 0
    total_bad_guesses = 0
    user_word = ["-", "-", "-", "-"]
    status = "Gave up"

    letter_freq = {'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70,
                   'f': 2.23, 'g': 2.02, 'h': 6.09, 'i': 6.97, 'j': 0.15,
                   'k': 0.77, 'l': 4.03, 'm': 2.41, 'n': 6.75, 'o': 7.51,
                   'p': 1.93, 'q': 0.10, 'r': 5.99, 's': 6.33, 't': 9.06,
                   'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15, 'y': 1.97,
                   'z': 0.07}

    def __init__(self):
        """
        Constructs a new 'guess' object.
        :param reset():                 Resets all global lists and parameters
                                        as needed for the new 'guess' instance.
        :param menu():                  Displays the game menu.
        :param select_random_string():  Retrieves a random word to be guessed
                                        by the user from a 'string_database' object
        :param choose_option():         Handles the game navigation with letters, 
                                        g = guess, t = tell me, l = letter and q = quit
        :param correct_word:            list to hold the result from select_random_string function.
        return:                         returns nothing
        """
        self.reset()
        self.menu()
        self.select_random_string()
        self.choose_option()
        self.correct_word = []

    def menu(self):
        """
        Game menu to print the letters guessesed by the user
        and game navigation options
        """
        print("\nCurrent Guess: " + "".join(self.user_word) + "\n")
        print("g = guess, t = tell me, l for a letter, and q to quit")

    def select_random_string(self):
        """
        Method to select a random word from a 'string_database' object 
        and stores the value in a global variable.
        """
        self.correct_word = list(string_database.get_db().get_word(
            random.randint(0, 4029)))
        self.correct_word = list("abed")
        # print(self.correct_word)
        # print(str(self.string_score()))

    def choose_option(self):
        """
        Method to handle game navigation.
        updates current game score global variable ('self.total_Score') when user gives updates
        """

        user_input = input()
        if user_input.lower() == 'g':
            # Handle string guess
            self.string_guess()
        elif user_input.lower() == 't':
            # Handle give up case
            self.total_score = 0 - self.uncovered_points()
            self.round_end_message(0)
        elif user_input.lower() == 'l':
            # Handle letter guesses
            self.char_guess()
        elif user_input.lower() == 'q':
            # Handle user quit but print game stats first
            self.print_game_stats()
            end_game()
        else:
            print("invalid option. let's try that again \n")
            self.menu()
            self.choose_option()

    def string_guess(self):
        user_guess = input("enter a four letter word: ")

        if len(user_guess) > 4 or len(user_guess) < 4:
            print("please choose a four letter word, lets try that again")
            self.string_guess()

        if list(user_guess) == self.correct_word:
            self.calc_score()
            # print(self.total_score)
            self.status = "success"
            self.round_end_message(1)
        else:
            self.total_bad_guesses += 1
            print("Incorrect guess. lets try that again")
            self.menu()
            self.choose_option()

    def char_guess(self):
        user_guess = input("enter a letter: \n")

        if len(user_guess) > 1 or len(user_guess) < 1:
            print("please choose a one letter word, lets try that again")
            self.char_guess()

        self.total_letter_guesses += 1

        if user_guess in self.correct_word:
            for x in range(len(self.correct_word)):
                if self.correct_word[x] == user_guess:
                    self.user_word[x] = user_guess

            if self.correct_word == self.user_word:
                self.calc_score()
                # print(self.calc_score())
                self.status = "success"
                self.round_end_message(1)
            else:
                print(
                    "you found " + str("".join(self.correct_word).count(user_guess)) + " letters")
                self.menu()
                self.choose_option()
        else:
            self.total_bad_guesses += 1
            print("this letter is not contained in the word!")
            self.menu()
            self.choose_option()

    def round_end_message(self, status):
        # create game object
        _game = game.game(len(self.games) + 1, "".join(self.correct_word), self.status,
                          self.total_bad_guesses, self.total_letter_guesses, self.total_score)
        self.games.append(_game)

        if status == 1:
            print("You guessed the right answer. it was truely " +
                  "".join(self.correct_word))

        else:
            print("Dont give up next time.the right answer was " +
                  "".join(self.correct_word))

    def uncovered_points(self):
        """
        Calculates the total frequency for the words that are yet to
        be uncovered.
        :param uncovered_indices:   Returns a list of indexes are that
                                    yet to be uncovered from the user_word.
        :count:                     Accumulator to store the sum of frequencies
                                    for uncovered letters.
        :return:                    returns the sum of the frequency of the
                                    uncovered word from local variable 'count'.
        """
        uncovered_indices = [i for i, x in enumerate(
            self.user_word) if x == "-"]
        count = 0

        for x in range(len(uncovered_indices)):
            count += self.letter_freq[self.correct_word[uncovered_indices[x]]]

        return count

    def calc_score(self):
        ""'
        
        '""
        count = self.uncovered_points()
        if count > 0:
            self.total_score = count / \
                self.total_letter_guesses if self.total_letter_guesses > 0 else count
        else:
            self.total_score = 0 - self.string_score()
            self.total_score /= self.total_letter_guesses

        # apply deduction for wrong guesses
        self.wrong_guess_penalty()

    def wrong_guess_penalty(self):
        #print("bad guesses: " + str(self.total_bad_guesses))
        divisor = 0.10 * self.total_bad_guesses
        self.total_score -= self.total_score * divisor if divisor > 0 else 0

    # function to reset global variables that may have changed
    def reset(self):
        self.user_word = ["-", "-", "-", "-"]
        self.total_score = 0
        self.total_letter_guesses = 0
        self.total_bad_guesses = 0
        self.status = "Gave up"

    def string_score(self):
        count = 0
        for x in range(len(self.correct_word)):
            count += self.letter_freq[self.correct_word[x]]
        return count

    def print_game_stats(self):
        game_total = 0
        print(
            "game    word    status      Bad Guesses     Missed letters      Score", end="")
        print(
            "\n----    ----    ------      -----------     --------------      -----", end="")
        for game_round in self.games:
            game_total += game_round.get_score()

            print("\n" + str(game_round.get_game_round()) +
                  "\t" + str(game_round.get_word()) +
                  "\t" + str(game_round.get_status()) +
                  "\t\t" + str(game_round.get_bad_guesses()) +
                  "\t\t" + str(game_round.get_missed_letters()) +
                  "\t\t" + str("%0.2f" % game_round.get_score()))
        print("\n\n" + "Final Score: " + str("%0.2f" % game_total))


def main():

    print("** The great guessing game ** ")

    for x in range(100):
        guess()

    print("you are a legend, you have finished the 100th round...")
    # game_stats()


def end_game():
    sys.exit()


main()


# NOTES:

# "".join(self.user_word)
# list(string)
# dir(guess) //view object contents
