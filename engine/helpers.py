class Coordinates:
    def __init__(self, x, y):
        self.x, self.y = x, y

    @classmethod
    def from_an(cls, coordinates):
        """
        from Algebraic notation
        :return:
        """
        column, row = coordinates[:1].lower(), coordinates[1:]
        x = 'abcdefgh'.index(column)
        return cls(x, int(row) - 1)

    def to_an(self):
        return f"{'abcdefgh'[self.x]}{self.y+1}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return self.to_an()
