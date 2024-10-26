from random import choice, randint, seed


class Square:
    def __init__(self, val):
        self.original = False
        self.original_val = "0"
        self.guesses = []
        if val == "0":
            self.val = "0"
        else:
            self.set_original(val)

    # Change a cell's value
    def set_value(self, val):
        if not self.original:
            self.val = val

    def add_guess(self, val):
        if val not in self.guesses:
            self.guesses.append(val)
            self.guesses.sort()

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
        vals = [square.val for square in self.squares if square.val != "0"]
        return len(vals) == len(set(vals))


class Puzzle:
    def __init__(self, puzzle, size: int=9):
        self.size = size
        if self.size == 4:
            vals = [str(val + 1) for val in range(4)]
        elif self.size == 9:
            vals = [str(val + 1) for val in range(9)]
        else:
            vals = [str(val + 1) for val in range(9)]+[char for char in "ABCDEFG"]
        self.vals = vals
        self.squares = [Square(puzzle[i]) for i in range(self.size**2)]
        self.groups = ([Group([self.squares[i + j * self.size] for i in range(self.size)]) for j in range(self.size)] +
                       [Group([self.squares[i * self.size + j] for i in range(self.size)]) for j in range(self.size)] +
                       [Group([self.squares[int((i // (self.size**0.5)) * self.size + i % (self.size**0.5) + (j % (self.size**0.5)) * (self.size**0.5) + (j // (self.size**0.5)) * (self.size**1.5))] for i in range(self.size)]) for
                        j in range(self.size)])
        self.check_valid()

    def return_clashes(self):
        clash = []
        for group in self.groups:
            for i in group.squares:
                for j in group.squares:
                    if i.val == j.val and i.val != "0" and i != j:
                        clash.append(self.squares.index(i))
                        clash.append(self.squares.index(j))
        return set(clash)

    # Change a cell in the grid using its coordinates
    def change_value(self, square, val):
        if not self.squares[square].original:
            self.squares[square].set_value(val)

    def add_guess(self, square, val):
        self.squares[square].add_guess(val)

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
                for n in self.vals:
                    self.squares[i].set_value(str(n))
                    if self.check_valid():
                        return True
            else:
                self.squares[i].set_value("0")
                return False
        # If already filled skip to next square
        if self.squares[i].val != "0" and self.squares[i] != self.squares[-1]:
            return self.solve(i + 1, excl)
        # Else go through other 9 values until a solution is found
        for n in self.vals:
            self.squares[i].set_value(str(n))
            if self.check_valid() and self.squares[i] != self.squares[-1]:
                if self.solve(i + 1, excl):
                    return True
            # Backtrack
            self.squares[i].set_value("0")
        return False

    @property
    def completed(self):
        if self.check_valid() and "0" not in [cell.val for cell in self.squares]:
            return True
        else:
            return False


class Game:
    def __init__(self, size: int = 9):
        self.puzzle: Puzzle | None = None
        self.size = size
        if self.size==16:
            self.vals=[char for char in "123456789ABCDEFGH"]
        else:
            self.vals=[str(digit+1) for digit in range(self.size)]

    def load_game(self, mode, arg: str, size=9):
        self.size=size
        if mode == "user":
            if len(arg) == self.size**2:
                self.puzzle = Puzzle(arg, self.size)
                return self.puzzle.num_solutions() == 1
            else:
                return False
        elif mode == "load":
            try:
                user_input = int(arg)
                with open(f"puzzles{size}.txt", "r") as file:
                    self.puzzle = Puzzle(file.readlines()[user_input], self.size)
                    return True
            except IndexError:
                return False

        elif mode == "generate":
            while not self.generate_puzzle(int(arg)):
                self.generate_puzzle(int(arg))
            return True

        else:
            return False

    def generate_puzzle(self, blanks):
        self.puzzle = Puzzle("0" * self.size**2, self.size)
        # Generate a full grid
        for cell in self.puzzle.squares:
            vals = [val for val in self.vals]
            val = choice(vals)
            cell.set_value(choice(val))
            vals.remove(val)
            while not self.puzzle.check_valid():
                try:
                    val = choice(vals)
                    cell.set_value(choice(val))
                    vals.remove(val)
                except IndexError:  # All possible values tried and invalid
                    return False
        # Remove values
        for i in range(blanks):
            n, prev = self.create_blank()
            while prev == "0" or self.puzzle.num_solutions() != 1:
                self.puzzle.squares[n].set_value(prev)
                n, prev = self.create_blank()
        if [cell.val for cell in self.puzzle.squares].count("0") == blanks:
            return True
        else:
            return False

    def create_blank(self):
        n = randint(0, self.size**2-1)
        prev = self.puzzle.squares[n].val
        self.puzzle.squares[n].original = False
        self.puzzle.squares[n].original_val = "0"
        self.puzzle.squares[n].set_value("0")
        self.puzzle = Puzzle("".join([cell.val for cell in self.puzzle.squares]), self.size)
        return n, prev


if __name__ == "__main__":
    seed(0)
    game = Game(9)
    game.load_game("generate", "20", 9)
    print("".join([cell.val for cell in game.puzzle.squares]))
