class Puzzle:
    def __init__(self, start):
        self.squares = {(i, j): Square(i, j) for i in range(9) for j in range(9)}
        for i in range(len(self.squares)):
            if start[i] != " ":
                self.squares[(i // 9, i % 9)].set_original(start[i])
        self.sets = tuple([tuple([(i, j) for i in range(9)]) for j in range(9)]
                          + [tuple([(j, i) for i in range(9)]) for j in range(9)]
                          + [tuple([(i + k * 3, j + l * 3) for i in range(3) for j in range(3)])
                             for k in range(3) for l in range(3)])

    def do_move(self, val, x, y):
        self.squares[(x, y)].set_value(val)


class Square:
    def __init__(self, x, y):
        self.val = "0"
        self.x = x
        self.y = y
        self.original = False

    def set_value(self, val):
        self.val = val
        # add to list of moves done

    def set_original(self, val):
        self.original = True
        self.val = val
