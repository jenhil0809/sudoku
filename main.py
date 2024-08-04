class Square:
    def __init__(self, val):
        self.original = False
        self.original_val = "0"
        if val == "0":
            self.val = "0"
        else:
            self.set_original(val)

    # Change a cell's value
    def set_value(self, val):
        if not self.original:
            self.val = val

    # If one of the original cells, set the value and prevent any future changes
    def set_original(self, val):
        self.set_value(val)
        self.original_val = val
        self.original = True

    def reset(self):
        self.val = self.original_val


class Group:
    def __init__(self, squares):
        self.squares = squares

    @property
    def valid(self):
        vals = [square.val for square in self.squares]
        vals = list(filter(lambda x: x != "0", vals))
        return len(vals) == len(set(vals))


class Puzzle:
    def __init__(self, puzzle):
        self.squares = [Square(puzzle[i]) for i in range(81)]
        self.groups = ([Group([self.squares[i + j * 9] for i in range(9)]) for j in range(9)] +
                       [Group([self.squares[i * 9 + j] for i in range(9)]) for j in range(9)] +
                       [Group([self.squares[(i // 3) * 9 + i % 3 + (j % 3) * 3 + (j // 3) * 27] for i in range(9)]) for
                        j in range(9)])
        self.check_valid()

    # Change a cell in the grid using its coordinates
    def change_value(self, square, val):
        self.squares[square].set_value(val)

    # Return true if no repeated values in any group
    def check_valid(self):
        return not (False in [group.valid for group in self.groups])

    def reset(self):
        for cell in self.squares:
            cell.reset()

    # Check if there are no, one or several solutions
    def num_solutions(self):
        if not self.solve():
            return 0
        solution = [cell.val for cell in self.squares][:-1]
        self.reset()
        if not self.solve(excl=solution):
            return 1
        else:
            return 2

    def solve(self, i=0, excl=None):
        # Every square filled
        if self.squares[i] == self.squares[-1]:
            if not [cell.val for cell in self.squares][:-1] == excl:
                return True
            else:
                self.squares[i].set_value("0")
                return False
        # If already filled skip to next square
        if self.squares[i].val != "0":
            return self.solve(i + 1, excl)
        # Else go through other 9 values until a solution is found
        for n in range(1, 10):
            self.squares[i].set_value(str(n))
            if self.check_valid():
                if self.solve(i + 1, excl):
                    return True
            # Backtrack
            self.squares[i].set_value("0")
        return False

