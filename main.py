import time
from GameSetup import GameSetup
from repository import GameRepository
import chess
from ChessEngine import ChessEngine
from ChessboardController import ChessboardController
from Browser import Browser
from database import get_session, init_db, SessionLocal
from GameManager import GameManager




STOCKFISH_PATH = "stockfish/stockfish-windows-x86-64-avx2.exe"


def main():
    init_db()
    with get_session() as session:
        repo = GameRepository(session)

        with Browser() as browser:
            browser.open("https://www.chess.com/play/online")

            setup = GameSetup(browser.driver)
            setup.select_time_control()
            setup.start_as_guest()
            setup.enable_show_legal_moves()
            setup.start_game()

            controller = ChessboardController(browser.driver)

            with ChessEngine(STOCKFISH_PATH) as chess_engine:
                game_manager = GameManager(controller, chess_engine, repo)

                while True:
                    game_manager.play_game()

                    print("\nLooking for a new game")
                    setup.start_new_game()
                    setup.wait_for_new_game()


if __name__ == '__main__':
    main()