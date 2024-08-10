from random import choice, randint


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
        vals = [square.val for square in self.squares]
        vals = list(filter(lambda x: x != "0", vals))
        return len(vals) == len(set(vals))


class Puzzle:
    def __init__(self, puzzle):
        self.squares = [Square(puzzle[i]) for i in range(81)]
        self.size = len(self.squares)
        self.groups = ([Group([self.squares[i + j * 9] for i in range(9)]) for j in range(9)] +
                       [Group([self.squares[i * 9 + j] for i in range(9)]) for j in range(9)] +
                       [Group([self.squares[(i // 3) * 9 + i % 3 + (j % 3) * 3 + (j // 3) * 27] for i in range(9)]) for
                        j in range(9)])
        self.check_valid()

    # Change a cell in the grid using its coordinates
    def change_value(self, square, val):
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
                for n in range(1, 10):
                    self.squares[i].set_value(str(n))
                    if self.check_valid():
                        return True
                    else:
                        return False
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

    @property
    def completed(self):
        if self.check_valid() and "0" not in [cell.val for cell in self.squares]:
            return True
        else:
            return False


class Game:
    def __init__(self, size: int = 81):
        self.puzzle: Puzzle | None = None
        self.size = size

    def load_game(self, mode, *args):
        if mode == "user":
            if len(args[0]) == self.size:
                self.puzzle = Puzzle(args[0])
                return True
            else:
                return False
        elif mode == "load":
            try:
                user_input = int(args[0])
                with open("puzzles.txt", "r") as file:
                    self.puzzle = Puzzle(file.readlines()[user_input])
                    return True
            except IndexError:
                return False
            pass

        elif mode == "generate":
            while not self.generate_puzzle(args[0]):
                self.generate_puzzle(args[0])
            return True

        else:
            return False

    def generate_puzzle(self, blanks):
        self.puzzle = Puzzle("0" * self.size)
        # Generate a full grid
        for cell in self.puzzle.squares:
            vals = [str(num) for num in range(1, 10)]
            val = choice(vals)
            cell.set_value(choice(val))
            vals.remove(val)
            while not self.puzzle.check_valid():
                try:
                    val = choice(vals)
                    cell.set_value(choice(val))
                    vals.remove(val)
                except IndexError:
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
        n = randint(0, 80)
        prev = self.puzzle.squares[n].val
        self.puzzle.squares[n].original = False
        self.puzzle.squares[n].original_val = "0"
        self.puzzle.squares[n].set_value("0")
        self.puzzle = Puzzle("".join([cell.val for cell in self.puzzle.squares]))
        return n, prev


if __name__ == "__main__":
    game = Game()
    game.load_game("generate", 40)
    print("".join([cell.val for cell in game.puzzle.squares]))
