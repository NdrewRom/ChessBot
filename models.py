from sqlalchemy import Column, Integer, String, DateTime, Boolean
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

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    move_number = Column(Integer, nullable=False)
    is_my_move = Column(Boolean, nullable=False)
    uci_move = Column(String(5), nullable=False)
    game = relationship("GameRecord", back_populates="moves")
