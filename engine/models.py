import abc
import json
import os

from collections import namedtuple

from engine.constants import (PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING,
                              WHITE, BLACK)
from engine.helpers import Square

GameState = namedtuple('GameState',
                       ('turn', 'controlled_squares', 'check_pieces'))


class InvalidMoveError(Exception):
    pass


class Piece(metaclass=abc.ABCMeta):
    __slots__ = (
        'type', 'color', 'current_square', 'moves_count', 'prior_square',
        '_possible_movement_squares', 'is_on_board')

    movement_directions = []

    def __init__(self, type_, color, current_square):
        self.type = type_
        self.color = color
        self.current_square = current_square
        self.moves_count = 0
        self.prior_square = None
        self.is_on_board = True
        self._possible_movement_squares = []

    @property
    def possible_movement_squares(self):
        return self._possible_movement_squares

    def remove(self):
        self.is_on_board = False

    def move(self, to_square):
        self.moves_count += 1
        self.prior_square = self.current_square
        self.current_square = to_square


class SingleMovementMixin(metaclass=abc.ABCMeta):
    def calculate_possible_movement_squares(self):
        self._possible_movement_sqares = []
        for x, y in self.movement_directions:
            square = Square(self.current_square.x + x,
                            self.current_square.y + y)
            piece_on_square = PiecesManager.get_piece(square)
            if square.is_valid() and (piece_on_square is None or
                                      piece_on_square.color != self.color):
                self._possible_movement_squares.append(square)


class DirectionMovementMixin(metaclass=abc.ABCMeta):
    def calculate_possible_movement_squares(self):
        """
        Calculates all possible movement squares in different directions
        :return:
        """
        self._possible_movement_sqares = []
        for x, y in self.movement_directions:
            self._calculate_squares_for_direction(x, y)

    def _calculate_squares_for_direction(self, x, y):
        """
        Calculates all possible movement squares in certain direction
        :param x: direction x coordinate
        :param y: direction y coordinate
        :return:
        """
        iteration = 0
        while True:
            iteration += 1
            square = Square(self.current_square.x + x * iteration,
                            self.current_square.y + y * iteration)

            if not square.is_valid():
                break

            piece_on_square = PiecesManager.get_piece(square)

            if piece_on_square is not None:
                if piece_on_square.color != self.color:
                    self._possible_movement_squares.append(square)
                break

            self._possible_movement_squares.append(square)


class Pawn(Piece):
    def __init__(self, color, current_square):
        super().__init__(PAWN, color, current_square)

        # if we create piece not on initial row
        if self.current_square.y not in (1, 6):
            self.moves_count = 1

    @property
    def movement_direction(self, ):
        return 1 if self.color == WHITE else -1

    def calculate_possible_movement_squares(self):
        self._possible_movement_squares = []
        self._possible_forward_movement_squares()
        self._possible_attack_movement_squares()

    def _step_move(self, step):
        square = Square(self.current_square.x,
                        self.current_square.y + step)
        if square.is_valid() and PiecesManager.get_piece(square) is None:
            return square

    def _possible_forward_movement_squares(self):
        possible_movement_squares = []
        one_square_move = self._step_move(self.movement_direction)
        possible_movement_squares.append(one_square_move)

        if one_square_move and self.moves_count == 0:
            two_squares_move = self._step_move(self.movement_direction * 2)
            possible_movement_squares.append(two_squares_move)

        # filter not None values
        self._possible_movement_squares += list(
            filter(bool, possible_movement_squares))

    def _possible_attack_movement_squares(self):
        squares = [Square(self.current_square.x + self.movement_direction,
                          self.current_square.y + self.movement_direction),
                   Square(self.current_square.x - self.movement_direction,
                          self.current_square.y + self.movement_direction)]
        for square in squares:
            piece_on_square = PiecesManager.get_piece(square)
            if square.is_valid() and piece_on_square is not None \
                    and piece_on_square.color != self.color:
                self._possible_movement_squares.append(square)

    def __str__(self):
        return ("\u265F" if self.color == WHITE else '\u2659').center(5)


class Rook(Piece, DirectionMovementMixin):
    movement_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def __init__(self, color, current_square):
        super().__init__(ROOK, color, current_square)

    def __str__(self):
        return ("\u265C" if self.color == WHITE else '\u2656').center(5)


class Knight(Piece, SingleMovementMixin):
    movement_directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2),
                           (-1, 2), (-1, -2)]

    def __init__(self, color, current_square):
        super().__init__(KNIGHT, color, current_square)

    def __str__(self):
        return ("\u265E" if self.color == WHITE else '\u2658').center(5)


class Bishop(Piece, DirectionMovementMixin):
    movement_directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    def __init__(self, color, current_square):
        super().__init__(BISHOP, color, current_square)

    def __str__(self):
        return ("\u265D" if self.color == WHITE else '\u2657').center(5)


class Queen(Piece, DirectionMovementMixin):
    movement_directions = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]

    def __init__(self, color, current_square):
        super().__init__(QUEEN, color, current_square)

    def __str__(self):
        return ("\u265B" if self.color == WHITE else '\u2655').center(5)


class King(Piece, SingleMovementMixin):
    movement_directions = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]

    def __init__(self, color, current_square):
        super().__init__(KING, color, current_square)

    def __str__(self):
        return ("\u265A" if self.color == WHITE else '\u2654').center(5)


class PiecesManager:
    opponent_possible_movement_squares = []
    opponent_check_pieces = []
    pieces = {}

    def __init__(self, pieces_configuration):
        __class__.pieces = {
            WHITE: self._initiate_pieces(WHITE, pieces_configuration["WHITE"]),
            BLACK: self._initiate_pieces(BLACK, pieces_configuration["BLACK"])
        }

    def move_piece(self, from_square, to_square):
        """
        Change piece location square
        :param turn:
        :param from_square:
        :param to_square:
        :return:
        """
        piece = self.pieces[Game.turn].get(from_square)
        if piece:
            piece.move(to_square)
            del self.pieces[Game.turn][from_square]
            self.pieces[Game.turn][to_square] = piece

    @classmethod
    def get_piece(cls, square):
        """
        Get piece color on square
        :param square: Square(x, y)
        :return: None if no piece on square
        :return: 1 if WHITE piece on square
        :return: 0 if BLACK piece on square
        """
        all_pieces = {**cls.pieces[WHITE], **cls.pieces[BLACK]}
        return all_pieces.get(square)

    def calculate_opponent_possible_movement_squares(self):
        self.opponent_possible_movement_squares = []
        opponent_color = Game.get_opponent_color()
        for square, piece in self.pieces[opponent_color].items():
            piece.calculate_possible_movement_squares(Game.turn)
            self.opponent_possible_movement_squares += \
                piece.possible_movement_squares

    def get_possible_movement_squares(self):
        """
        Get available moves for current turn pieces
        :return:
        """
        possible_movement_squares = {}
        for square, piece in self.pieces[Game.turn].items():
            piece.calculate_possible_movement_squares()
            possible_movement_squares.update(
                {square: piece.possible_movement_squares})
        return possible_movement_squares

    def _initiate_pieces(self, color, configuration):
        pieces = {}
        for piece, squares in configuration.items():
            _class = globals()[piece.capitalize()]
            for square in squares:
                _square = Square.from_an(square)
                pieces.update({
                    _square: _class(color, _square)
                })
        return pieces

    def _validate_move(self, from_square, to_square):
        """
        Validates if piece on from_square exists, to_square is a valid move,
        and piece can make a move.
        :param from_square:
        :param to_square:
        :return:
        """
        piece = self.get_piece(from_square)

        if not piece or piece.color != Game.turn or \
                to_square not in piece.available_moves:
            raise InvalidMoveError(f"Invalid move for {from_square}")


class Game:
    turn = WHITE
    total_moves = 0
    is_check = False

    def __init__(self, configuration=None):
        if not configuration:
            filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'default_pieces_configuration.json')
            with open(filename) as f:
                configuration = json.load(f)
        self.pieces_manager = PiecesManager(configuration)

    @classmethod
    def get_opponent_color(cls):
        return WHITE if cls.turn == BLACK else BLACK

    def change_turn(self):
        self.turn = Game.get_opponent_color()

    def make_move(self, square1, square2):
        from_square = Square.from_an(square1)
        to_square = Square.from_an(square2)
        self.pieces_manager.move_piece(from_square, to_square)

    def get_board(self):
        for y in range(7, -1, -1):
            print('  ', end='')
            print('-' * 48)
            print(y + 1, end='')
            for x in range(8):
                print('|', end='')
                piece = self.pieces_manager.get_piece(Square(x, y))
                print(piece if piece else ' ' * 5, end='')
            print('|')
        print(' ', end='')
        print('-' * 48)
        print(' ', end='')
        for l in 'abcdefgh':
            print(l.center(6), end='')
        print()

    def start(self):
        while True:
            try:
                self.get_board()
                available_moves = \
                    self.pieces_manager.get_possible_movement_squares()

                for square, moves in available_moves.items():
                    print(f"{square}: {[str(m) for m in moves]}")

                from_, to = input(
                    f"{'White' if self.turn == WHITE else 'Black'} move: ").split()
                self.make_move(from_, to)
                self.change_turn()
            except InvalidMoveError as e:
                print(e)


if __name__ == '__main__':
    # filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #                     'default_pieces_configuration.json')
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'temp.json')
    with open(filename) as f:
        configuration = json.load(f)

    game = Game(configuration)
    game.start()
