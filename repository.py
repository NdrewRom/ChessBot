from sqlalchemy.orm import Session
from models import GameRecord, MoveRecord
class GameRepository:

    def __init__(self, session):
        self.session = session

    def create_game(self, my_color: str):
        game = GameRecord(my_color=my_color, result="in_progress")
        self.session.add(game)
        self.session.commit()
        return game

    def add_move(self, game_id: int, move_number: int, is_my_move: bool, uci_move: str):
        move = MoveRecord(
            game_id=game_id,
            move_number=move_number,
            is_my_move=is_my_move,
            uci_move=uci_move
        )
        self.session.add(move)
        self.session.commit()

    def finish_game(self, game_id: int, result: str = "finished"):
        game = self.session.query(GameRecord).filter_by(id=game_id).first()
        if game:
            game.status = result
            self.session.commit()