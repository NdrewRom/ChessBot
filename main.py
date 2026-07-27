import time
from GameSetup import GameSetup
import chess
from ChessEngine import ChessEngine
from ChessboardController import ChessboardController
from Browser import Browser


def main():
    with Browser() as browser:
        browser.open("https://www.chess.com/play/online")

        setup = GameSetup(browser.driver)
        setup.select_time_control()
        setup.start_as_guest()
        setup.enable_show_legal_moves()
        controller = ChessboardController(browser.driver)
        setup.start_game()


        with ChessEngine("stockfish/stockfish-windows-x86-64-avx2.exe") as chess_engine:
            while True:
                my_color = controller.get_my_color()
                print(f"Ваш цвет: {'БЕЛЫЕ' if my_color == chess.WHITE else 'ЧЕРНЫЕ'}")
                board = chess.Board()

                print("Бот запущен. Начинаем отслеживание игры...")

                while True:
                    if controller.is_game_over():
                        print("Игра окончена!")
                        break

                    if board.turn == my_color:
                        print("\n--- Мой ход! Думаю... ---")

                        move = chess_engine.get_best_move(board)
                        print(f"Делаю легальный ход: {move}")
                        controller.make_move(move)
                        board.push(move)
                        time.sleep(0.6)

                    else:
                        time.sleep(0.15)

                        try:
                            current_pieces = controller.get_pieces()
                        except RuntimeError:
                            continue

                        detected_move = None

                        for move in board.legal_moves:
                            board.push(move)
                            match = True
                            for square_index in chess.SQUARES:
                                square_name = chess.square_name(square_index)
                                piece_on_board = board.piece_at(square_index)
                                piece_on_site = current_pieces.get(square_name)
                                symbol_on_board = piece_on_board.symbol() if piece_on_board else None

                                if symbol_on_board != piece_on_site:
                                    match = False
                                    break
                            board.pop()

                            if match:
                                detected_move = move
                                break

                        if detected_move:
                            print(f"\n--- Обнаружен ход оппонента: {detected_move} ---")
                            board.push(detected_move)
                            print(board)
                            time.sleep(0.2)

                setup.start_new_game()
                setup.wait_for_new_game()

if __name__ == '__main__':
    main()