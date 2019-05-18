# reponsible for all disk I/O. can add whatever code you think you need here.


class string_database:
    def _init_(self):
        print("this is my first constructor")

    def get_word(self, index):
        words = open("four_letters.txt", "r")
        contents = words.read().split()

        return contents[index]


def get_db():
    return string_database()
