# maintains information about a specific game


class game:
    def _init_(self):
        print("game class")

    def play(self):
        print("Let us play!")


def main():
    _game = game()
    _game._init_()


if __name__ == "__main__":
    main()
