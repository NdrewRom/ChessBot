from sqlalchemy.orm import Session
from models import GameRecord, MoveRecord
class GameRepository:

    def __init__(self, session: Session):
        self.session = session

    def create_game(self, my_color: str) -> GameRecord:
        game = GameRecord(my_color=my_color)
        self.session.add(game)
        self.session.commit()
        self.session.refresh(game)
        return game

    def add_move(self, game_id: int, move_number: int, move_uci: str) -> None:
        move = MoveRecord(
            game_id=game_id, move_number=move_number, move_uci=move_uci
        )
        self.session.add(move)
        self.session.commit()

    def finish_game(self, game_id: int, result: str) -> None:
        game = (
            self.session.query(GameRecord)
            .filter(GameRecord.id == game_id)
            .first()
        )
        if not game:
            raise ValueError(f"Партия с ID {game_id} не найдена")

        game.result = result
        self.session.commit()