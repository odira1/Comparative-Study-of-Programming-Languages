# randomly select a string from string
# ask user to guess


def main():
    print("** The great guessing game ** \n")
    print("Current Guess: ---- \n")
    print("g = guess, t = tell me, l for a letter, and q to quit")
    user_input = input()

    if user_input.lower() == 'g':
        # we take a guess
        print("we take a guess")
    elif user_input.lower() == 't':
        # we tell the answer
        print("we tell the answer")
    elif user_input.lower() == 'l':
        # we give a letter
        guess_character = input("enter a letter: \n")
    elif user_input.lower == 'q':
        exit(0)
    else:
        print("invalid option")

    # print(file_reader())
    # print(user_input)


def game():
    # hold specific game info
    print("game information")


def stringDatabase():
    words = open("four_letters.txt", "r")
    contents = words.read().split()

    return contents[0]


main()
