from .helpers import Coordinates


WHITE = 1
BLACK = 0

PAWN = 'pawn'
ROOK = 'rook'
KNIGHT = 'knight'
BISHOP = 'bishop'
KING = 'king'
QUEEN = 'queen'

WHITE_INITIAL_SQUARES = {
    Coordinates(x, y): WHITE for y in range(2) for x in range(8)
}

BLACK_INITIAL_SQUARES = {
    Coordinates(x, y): BLACK for y in range(6, 8) for x in range(8)
}
