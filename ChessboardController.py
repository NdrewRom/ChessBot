import chess
import time
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

class ChessboardController:
    PIECE_SELECTOR = ".piece"

    def __init__(self, driver):
        self._driver = driver

    @staticmethod
    def square_to_coord(square: str) -> str:
        """'54' -> 'e4'"""
        col, row = square[0], square[1]
        return chr(int(col) + 96) + row

    @staticmethod
    def coord_to_square(coord: str) -> str:
        """'e4' -> '54'"""
        col, row = coord[0], coord[1]
        return str(ord(col) - 96) + row

    def get_pieces(self) -> dict[str, str]:
        while True:
            try:
                pieces_dict = {}
                elements = self._driver.find_elements(By.CSS_SELECTOR, "[class*='piece'][class*='square']")
                for el in elements:
                    class_name = el.get_attribute("class")

                    square_match = re.search(r'square-(\d+)', class_name)
                    piece_match = re.search(r'\b(w|b)(p|r|n|b|q|k)\b', class_name)

                    if not square_match or not piece_match:
                        continue

                    place = self.square_to_coord(square_match.group(1))
                    color, piece_type = piece_match.group(1), piece_match.group(2)
                    piece = piece_type.upper() if color == 'w' else piece_type
                    pieces_dict[place] = piece

                if not pieces_dict:
                    raise RuntimeError("Не удалось найти фигуры на доске")

                return pieces_dict
            except StaleElementReferenceException:
                time.sleep(0.1)
                continue

    def build_board(self, pieces_dict: dict, turn: bool = chess.WHITE) -> chess.Board:
        board = chess.Board()
        board.clear()
        for square, symbol in pieces_dict.items():
            square_index = chess.parse_square(square)
            piece = chess.Piece.from_symbol(symbol)
            board.set_piece_at(square_index, piece)
        board.turn = turn
        return board

    def make_move(self, move: chess.Move) -> None:
        from_move = self.coord_to_square(chess.square_name(move.from_square))
        to_move = self.coord_to_square(chess.square_name(move.to_square))

        from_element =  WebDriverWait(self._driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f".square-{from_move}"))
        )
        ActionChains(self._driver).move_to_element(from_element).click().perform()

        to_element = WebDriverWait(self._driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f".square-{to_move}"))
        )
        ActionChains(self._driver).move_to_element(to_element).click().perform()

    def is_game_over(self) -> bool:
        return len(
            self._driver.find_elements(
                By.CSS_SELECTOR,
                "[class*='game-over-modal']"
            )
        ) > 0

    def get_my_color(self) -> bool:
        board_element = self._driver.find_element(By.CSS_SELECTOR, "wc-chess-board")
        print(board_element.get_attribute("outerHTML")[:200])
        classes = board_element.get_attribute("class")
        return chess.BLACK if "flipped" in classes else chess.WHITE

    def wait_and_detect_enemy_move(self, board: chess.Board) -> chess.Move | None:
        try:
            current_pieces = self.get_pieces()
        except RuntimeError:
            return None

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
                return move

        return None

