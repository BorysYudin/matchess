class Square:
    column_letters = 'abcdefgh'

    def __init__(self, x, y):
        self.x, self.y = x, y

    @classmethod
    def from_an(cls, an_square):
        """
        From Algebraic notation
        :return:
        """
        column, row = an_square[:1].lower(), an_square[1:]
        x = cls.column_letters.index(column.lower())
        return cls(x, int(row) - 1)

    def to_an(self):
        return f"{self.column_letters[self.x]}{self.y+1}"

    def is_valid(self):
        """
        Checks if square is within the board coordinates
        :return:
        """
        return 0 <= self.x <= 7 and 0 <= self.y <= 7

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return self.to_an()
