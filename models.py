from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import ForeignKey
from datetime import datetime


Base = declarative_base()


class GameRecord(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    play_date = Column(DateTime, default=datetime.utcnow)
    my_color = Column(String)
    result = Column(String)
    moves = relationship("MoveRecord", back_populates="game")


class MoveRecord(Base):
    __tablename__ = "moves"
    game = relationship("GameRecord", back_populates="moves")
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    move_number = Column(Integer)
    move_uci = Column(String)

