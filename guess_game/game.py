# maintains information about a specific game


class game():
    def __init__(self, game_round, word, status, bad_guesses, missed_letters, score):
        self.game_round = game_round
        self.word = word
        self.status = status
        self.bad_guesses = bad_guesses
        self.missed_letters = missed_letters
        self.score = score

    def get_game_round(self):
        return self.game_round

    def get_word(self):
        return self.word

    def get_status(self):
        return self.status

    def get_bad_guesses(self):
        return self.bad_guesses

    def get_missed_letters(self):
        return self.missed_letters

    def get_score(self):
        return self.score


def main():
    #just testing for object creation
    gamer = game(1, "yule", "success", 0, 2, 2.02)
    # print(this_game().status)
    print(gamer.get_score())


if __name__ == "__main__":
    main()
