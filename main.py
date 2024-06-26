from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import model

class Group:
    def __init__(self):
        self.vals = []

    def add_val(self, val):
        self.vals.append(val)

    def check_valid(self):
        vals_no_zeroes = [str(box.val) for box in self.vals if box.val != " "]
        if len(set(vals_no_zeroes)) == len(vals_no_zeroes):
            return True
        else:
            return False


class Square:
    def __init__(self, val, row, col, rows, cols, boxes):
        self.coords = [row, col]
        self.val = val
        self.row = rows[row]
        self.col = cols[col]
        self.row.add_val(self)
        self.col.add_val(self)
        self.box = boxes[self.find_box()]
        self.box.add_val(self)

    def find_box(self):
        if str(self.coords[0]) in "012" and str(self.coords[1]) in "012":
            return 0
        elif str(self.coords[0]) in "345" and str(self.coords[1]) in "012":
            return 1
        elif str(self.coords[0]) in "678" and str(self.coords[1]) in "012":
            return 2
        elif str(self.coords[0]) in "012" and str(self.coords[1]) in "345":
            return 3
        elif str(self.coords[0]) in "345" and str(self.coords[1]) in "345":
            return 4
        elif str(self.coords[0]) in "678" and str(self.coords[1]) in "345":
            return 5
        elif str(self.coords[0]) in "012" and str(self.coords[1]) in "678":
            return 6
        elif str(self.coords[0]) in "345" and str(self.coords[1]) in "678":
            return 7
        else:
            return 8


rows = [Group() for i in range(9)]
cols = [Group() for i in range(9)]
boxes = [Group() for i in range(9)]

puzzle = ""


def get_puzzle(id):
    engine = create_engine('sqlite:///sudoku.sqlite', echo=True)
    sess = Session(engine)
    puzzle = sess.query(model.Puzzle).get(id).puzzle
    sess.close()
    return puzzle


puzzle = get_puzzle(2)

for row in range(9):
    for col in range(9):
        Square(puzzle[col + row * 9], row, col, rows, cols, boxes)


def do_move(val, row, col):
    square = rows[row].vals[col]
    prev = square.val
    square.val = val
    if not (square.row.check_valid() and square.col.check_valid() and square.box.check_valid()):
        square.val = prev
        return "Invalid: number may only appear once a row, column or 3x3 box"
    elif puzzle[col + row * 9] != " ":
        square.val = prev
        return "Invalid: box is a clue"
    elif val not in "0123456789":
        square.val = prev
        return "Invalid: value must be a digit"
    else:
        return "Valid"
