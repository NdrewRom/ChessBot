import chess

class Game:
    def __init__(self):
        self._board = chess.Board()

    @property
    def board(self) -> chess.Board:
        return self._board

    @property
    def current_turn(self) -> bool:
        return self._board.turn

    def is_game_over(self) -> bool:
        return self._board.is_game_over()

    def make_move(self, move: chess.Move | str) -> None:
        try:
            if isinstance(move, str):
                move = chess.Move.from_uci(move)

            if move not in self._board.legal_moves:
                raise ValueError

            self._board.push(move)

        except (chess.InvalidMoveError, ValueError):
            raise ValueError("Некорректный ход")

    @property
    def outcome(self) -> chess.Outcome:
        return self._board.outcome()