
class game():
    """
    Maintains all necessary information about a specific game.
    """

    def __init__(self, game_round, word, status, bad_guesses, missed_letters,
                 score):
        """
        Constructs a new 'game' object.
        :param game_round:      Contains the round for the current game object.
        :param word:            Contains the word to be guessed in this game.
        :param status:          Holds the status of the current game
        :param bad_guesses:     Holds the number of wrong guesses.
        :param missed_letters:  Holds the number of letter the user missed.
        :param score:           Holds the total game score.
        """

        self.game_round = game_round
        self.word = word
        self.status = status
        self.bad_guesses = bad_guesses
        self.missed_letters = missed_letters
        self.score = score

    def get_game_round(self):
        """
        Returns the round where this game object was created.
        """

        return self.game_round

    def get_word(self):
        """
        Returns the word to be guessed in this game round.
        """
        return self.word

    def get_status(self):
        """
        Returns the status of the current game,value may be gave up or success.
        """

        return self.status

    def get_bad_guesses(self):
        """
        Returns the number of wrong guesses.
        """

        return self.bad_guesses

    def get_missed_letters(self):
        """
        Returns the number letters that were not guessed by the user
        """

        return self.missed_letters

    def get_score(self):
        """
        Return the total game score.
        """

        return self.score


def main():
    """
    Main method to test creation of objects of the 'game' class.
    Will only run if this module is the the point of entry.
    """
    gamer = game(1, "yule", "success", 0, 2, 2.02)
    print(gamer.get_score())


if __name__ == "__main__":
    main()
