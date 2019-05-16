class string_database:
    def _init_(self):
        print("this is my first constructor")

    def void(self):
        print("an empty void test")


class integer_database:
    def _init_(self):
        print("this is the integer database")


class a2(integer_database, string_database):
    def _init_(self):
        super()._init_()
        print("this is my second constructor")


second = a2()
first = string_database()

second._init_()
