class string_database:
    """
    Encapsulates  a method required to create list from text File.
    """

    def _init_(self):
        """
        constructs a new string_database object.
        """

    def get_word(self, index):
        """
        returns an item using a supplied index (random index) 
        from a list curated from a provided textfile
        """
        words = open("four_letters.txt", "r")
        contents = words.read().split()

        return contents[index]


def get_db():
    """
    returns an instance of string_database
    """
    return string_database()
