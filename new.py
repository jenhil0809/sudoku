class Puzzle:
    def __init__(self, start):
        self.squares = {(i, j): Square(i, j) for i in range(9) for j in range(9)}
        for i in range(len(self.squares)):
            if start[i] != " ":
                self.squares[(i // 9, i % 9)].set_original(start[i])
        self.sets = tuple([tuple([(i, j) for i in range(9)]) for j in range(9)]
                          + [tuple([(j, i) for i in range(9)]) for j in range(9)]
                          + [tuple([(i + k * 3, j + l * 3) for i in range(3) for j in range(3)])
                             for k in range(3) for l in range(3)]) # each of the 9 rows, columns and boxes

    # carries out a move after validating it
    def do_move(self, val, x, y):
        if x not in "012345678" or y not in "012345678":
            return 2  # square does not exist
        if val not in "0123456789":
            return 3  # invalid value
        if not self.squares[(int(x), int(y))].original:
            self.squares[(int(x), int(y))].set_value(val)
            if self.check_completed():
                return -1  # puzzle completed
            return 0  # puzzle not completed, but move valid
        else:
            return 1  # square is one of the clue squares

    # checks whether the puzzle is completed
    def check_completed(self):
        for group in self.sets:
            values = [self.squares[group[i]].val for i in range(9)]
            # if a square is empty 0 will be in values and if a value is repeated the length of the set will be < 9
            if not ("0" not in values and len(set(values)) == 9):
                return False
        return True


class Square:
    def __init__(self, x, y):
        self.val = "0"
        self.x = x
        self.y = y
        self.original = False

    # changes the value of a squares
    def set_value(self, val):
        self.val = val
        # add to list of moves done

    # sets the original clue squares that will not later be altered by the user
    def set_original(self, val):
        self.original = True
        self.val = val
