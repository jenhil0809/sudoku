from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Puzzle(Base):
    __tablename__ = 'puzzles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    puzzle = Column(String, nullable=False)

    def __repr__(self):
        return f'Puzzle(puzzle={self.puzzle})'