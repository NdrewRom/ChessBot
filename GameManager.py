import time
import chess


class GameManager:
    def __init__(self, controller, engine, repo):
        self.controller = controller
        self.engine = engine
        self.repo = repo

    def play_game(self):
        time.sleep(1)

        my_color = self.controller.get_my_color()
        color_str = "БЕЛЫЕ" if my_color == chess.WHITE else "ЧЕРНЫЕ"

        print(f" Новая партия! Мой цвет: {color_str}")

        game_record = self.repo.create_game(my_color=color_str)
        print(f"Партия сохранена в БД с ID: {game_record.id}")

        board = chess.Board()

        try:
            while not self.controller.is_game_over():
                if board.turn == my_color:
                    self._handle_our_turn(board, game_record.id)
                else:
                    self._handle_enemy_turn(board, game_record.id)

        except Exception as e:
            print(f"Игра была прервана: {e}")

        finally:
            time.sleep(1)
            result_title = self.controller.get_game_result_reason()
            print(f" Сохраняю результат в БД: '{result_title}'")
            self.repo.finish_game(game_id=game_record.id, result=result_title)

    def _handle_our_turn(self, board: chess.Board, game_id: int):
        move = self.engine.get_best_move(board)
        print(f"Выполняю ход: {move}")
        self.repo.add_move(
            game_id=game_id,
            move_number=board.fullmove_number,
            is_my_move=True,
            uci_move=move.uci()
        )

        self.controller.make_move(move)
        board.push(move)

    def _handle_enemy_turn(self, board: chess.Board, game_id: int):
        enemy_move = self.controller.wait_and_detect_enemy_move(board)

        if enemy_move:
            self.repo.add_move(
                game_id=game_id,
                move_number=board.fullmove_number,
                is_my_move=False,
                uci_move=enemy_move.uci()
            )

            board.push(enemy_move)
            print(board)