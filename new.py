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
        if x not in "012345678" or y not in "012345678":
            return 2
        if val not in "0123456789":
            return 3
        if not self.squares[(int(x), int(y))].original:
            self.squares[(int(x), int(y))].set_value(val)
            return 0
        else:
            return 1


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
