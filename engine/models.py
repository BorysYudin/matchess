import abc
import json
import os

from engine.constants import (PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING,
                              WHITE_INITIAL_SQUARES, BLACK_INITIAL_SQUARES,
                              WHITE, BLACK)
from engine.helpers import Coordinates


class InvalidMoveError(Exception):
    pass


class Piece(metaclass=abc.ABCMeta):
    __slots__ = (
        'type', 'color', 'current_square', 'moves_count', 'prior_square',
        '_available_moves', 'is_on_board')

    def __init__(self, type_, color, current_square):
        self.type = type_
        self.color = color
        self.current_square = current_square
        self.moves_count = 0
        self.prior_square = None
        self._available_moves = []
        self.is_on_board = True

    @property
    def available_moves(self):
        return self._available_moves

    @abc.abstractmethod
    def calculate_available_moves(self, turn, board, controlled_squares=None,
                                  check_pieces=None):
        raise NotImplemented

    def remove(self):
        self.is_on_board = False

    def move(self, square):
        self.moves_count += 1
        self.prior_square = self.current_square
        self.current_square = square


class Pawn(Piece):
    def __init__(self, color, current_square):
        super().__init__(PAWN, color, current_square)

    @property
    def step(self):
        return 1 if self.color == WHITE else -1

    def calculate_available_moves(self, turn, board, controlled_squares=None,
                                  check_pieces=None):
        available_moves = []
        available_moves += self._available_forward_moves(turn, board,
                                                         controlled_squares,
                                                         check_pieces)
        available_moves += self._available_attack_moves(turn, board,
                                                        controlled_squares,
                                                        check_pieces)
        self._available_moves = available_moves
        return available_moves

    def _available_forward_moves(self, turn, board, controlled_squares,
                                 check_pieces):
        available_moves = []
        one_square_move = Coordinates(self.current_square.x,
                                      self.current_square.y + self.step)
        if board.is_square_on_board(one_square_move) and \
                board.get_piece(one_square_move) is None:
            available_moves.append(one_square_move)

        two_squares_move = Coordinates(self.current_square.x,
                                       self.current_square.y + self.step * 2)

        if self.moves_count == 0 and \
                board.is_square_on_board(two_squares_move) and \
                board.get_piece(two_squares_move) is None:
            available_moves.append(two_squares_move)

        return available_moves

    def _available_attack_moves(self, turn, board, controlled_squares,
                                check_pieces):
        available_moves = []
        squares = [Coordinates(self.current_square.x + self.step,
                               self.current_square.y + self.step),
                   Coordinates(self.current_square.x - self.step,
                               self.current_square.y + self.step)]
        for square in squares:
            board_piece = board.get_piece(square)
            if board.is_square_on_board(
                    square) and board_piece and board_piece != self.color:
                available_moves.append(square)

        return available_moves

    def __str__(self):
        return ("\u265F" if self.color == WHITE else '\u2659').center(5)


class Rook(Piece):
    def __init__(self, color, current_square):
        super().__init__(ROOK, color, current_square)

    def calculate_available_moves(self, turn, board, controlled_squares=None,
                                  check_pieces=None):
        available_moves = []

        for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            square = Coordinates(self.current_square.x + x,
                                 self.current_square.y + y)
            board_piece = board.get_piece(square)
            iteration = 1
            while board.is_square_on_board(square) and board_piece is None:
                iteration += 1
                available_moves.append(square)
                square = Coordinates(self.current_square.x + x * iteration,
                                     self.current_square.y + y * iteration)
                board_piece = board.get_piece(square)
        self._available_moves = available_moves
        return available_moves

    def __str__(self):
        return ("\u265C" if self.color == WHITE else '\u2656').center(5)


class Knight(Piece):
    def __init__(self, color, current_square):
        super().__init__(KNIGHT, color, current_square)

    def calculate_available_moves(self, turn, board, controlled_squares=None,
                                  check_pieces=None):
        available_squares = []

        for x, y in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2),
                     (-1, 2), (-1, -2)]:
            square = Coordinates(self.current_square.x + x,
                                 self.current_square.y + y)
            if board.is_square_on_board(square) and \
                    board.get_piece(square) != self.color:
                available_squares.append(square)
        self._available_moves = available_squares
        return available_squares

    def __str__(self):
        return ("\u265E" if self.color == WHITE else '\u2658').center(5)


class Bishop(Piece):
    def __init__(self, color, current_square):
        super().__init__(BISHOP, color, current_square)

    def calculate_available_moves(self, turn, board, controlled_squares=None,
                                  check_pieces=None):
        return []

    def __str__(self):
        return ("\u265D" if self.color == WHITE else '\u2657').center(5)


class Queen(Piece):
    def __init__(self, color, current_square):
        super().__init__(QUEEN, color, current_square)

    def calculate_available_moves(self, turn, board, controlled_squares=None,
                                  check_pieces=None):
        return []

    def __str__(self):
        return ("\u265B" if self.color == WHITE else '\u2655').center(5)


class King(Piece):
    def __init__(self, color, current_square):
        super().__init__(KING, color, current_square)

    def calculate_available_moves(self, turn, board, controlled_squares=None,
                                  check_pieces=None):
        return []

    def __str__(self):
        return ("\u265A" if self.color == WHITE else '\u2654').center(5)


class PiecesManager:
    controlled_squares = []
    check_pieces = []

    def __init__(self, configuration):
        self.pieces = {
            WHITE: self.__create_pieces(WHITE, configuration["WHITE"]),
            BLACK: self.__create_pieces(BLACK, configuration["BLACK"])
        }

    def move_piece(self, color, from_square, to_square):
        piece = self.pieces[color].get(from_square)
        if piece:
            piece.move(to_square)
            del self.pieces[color][from_square]
            self.pieces[color][to_square] = piece

    def get_black_piece(self, square, color=None):
        piece = self.pieces[BLACK].get(square)
        return piece if color and piece.color == color else None

    def get_piece(self, square):
        """
        Get piece color on square
        :param square: Coordinates(x, y)
        :return: None if no piece on square
        :return: 1 if WHITE piece on square
        :return: 0 if BLACK piece on square
        """
        all_pieces = {**self.pieces[WHITE], **self.pieces[BLACK]}
        return all_pieces.get(square)

    def calculate_opponent_available_moves(self, turn, board):
        self.controlled_squares = []
        opponent_color = WHITE if turn == BLACK else BLACK
        for square, piece in self.pieces[opponent_color].items():
            self.controlled_squares += piece.calculate_available_moves(turn,
                                                                       board)

    def get_available_moves(self, turn, board):
        """
        Get available moves for current turn pieces
        :return:
        """
        available_moves = {}
        for square, piece in self.pieces[turn].items():
            available_moves[square] = \
                piece.calculate_available_moves(turn, board,
                                                self.controlled_squares,
                                                self.check_pieces)
        return available_moves

    def __create_pieces(self, color, configuration):
        pieces = {}
        for piece, squares in configuration.items():
            _class = globals()[piece.capitalize()]
            for square in squares:
                _square = Coordinates.from_an(square)
                pieces.update({
                    _square: _class(color, _square)
                })
        return pieces


class Board:
    pieces = {
        **WHITE_INITIAL_SQUARES,
        **BLACK_INITIAL_SQUARES
    }

    def move_piece(self, from_square, to_square):
        piece = self.pieces.get(from_square)
        del self.pieces[from_square]
        self.pieces[to_square] = piece

    def get_piece(self, square):
        return self.pieces.get(square)

    def is_square_on_board(self, square):
        return 0 <= square.x <= 7 and 0 <= square.y <= 7


class Game:
    def __init__(self, configuration):
        self.turn = WHITE
        self.moves = 0
        self.is_check = False
        self.board = Board()
        self.pieces_manager = PiecesManager(configuration)

    def change_turn(self):
        self.turn = BLACK if self.turn == WHITE else WHITE

    def _validate_move(self, from_square, to_square):
        """
        Validates if piece on from_square exists, to_square is a valid move,
        and piece can make a move.
        :param from_square:
        :param to_square:
        :return:
        """
        piece = self.pieces_manager.get_piece(from_square)

        if not piece or piece.color != self.turn or \
                to_square not in piece.available_moves:
            raise InvalidMoveError(f"Invalid move for {from_square}")

    def make_move(self, coordinates1, coordinates2):
        from_square = Coordinates.from_an(coordinates1)
        to_square = Coordinates.from_an(coordinates2)
        self._validate_move(from_square, to_square)
        self.board.move_piece(from_square, to_square)
        self.pieces_manager.move_piece(self.turn, from_square, to_square)

    def get_available_moves(self):
        return self.pieces_manager.get_available_moves(self.turn, self.board)

    def get_board(self):
        for y in range(7, -1, -1):
            print('  ', end='')
            print('-' * 48)
            print(y + 1, end='')
            for x in range(8):
                print('|', end='')
                piece = self.pieces_manager.get_piece(Coordinates(x, y))
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
                available_moves = self.get_available_moves()

                for piece, moves in available_moves.items():
                    print(f"{piece}: {[str(m) for m in moves]}")

                from_, to = input(
                    f"{'White' if self.turn == WHITE else 'Black'} move: ").split()
                self.make_move(from_, to)
                self.change_turn()
            except InvalidMoveError as e:
                print(e)


if __name__ == '__main__':
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'default_pieces_configuration.json')
    with open(filename) as f:
        configuration = json.load(f)

    game = Game(configuration)
    game.start()
