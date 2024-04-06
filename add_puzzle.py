from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model import Puzzle

engine = create_engine('sqlite:///sudoku.sqlite', echo=True)
puzzle_text = input("Sudoku: ")
puzzle = Puzzle(puzzle=puzzle_text)

with Session(engine) as sess:
    sess.add(puzzle)
    sess.commit()