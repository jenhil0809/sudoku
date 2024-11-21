from random import choice, randint, seed


class Square:
    """Class for each cell in a sudoku"""

    def __init__(self, val: str):
        """
        Parameters
        ----------
        val: str
            string representing the value held by the cell
        Attributes
        ----------
        self.original: bool
            True if the cell is one of the cells given by the puzzle
        self.original_val: str
            the value of the cell before user inputs
        self.guesses: list of strs
            stores notes/guesses added by the user regarding this cell
        """
        self.original = False
        self.original_val = "0"
        self.guesses = []
        if val == "0":
            self.val = "0"
        else:
            self.set_original(val)

    def set_value(self, val):
        """
        Change the cell's value
        Parameters
        ----------
        val: str
            the value the cell should be set to
        """
        if not self.original:
            self.val = val

    def add_guess(self, val):
        """
        Add a guess to guesses
        Parameters
        ----------
        val: str
            the value that should be added to the list
        """
        if val not in self.guesses:
            self.guesses.append(val)
            self.guesses.sort()

    def set_original(self, val):
        """
        If one of the original cells, set the value and prevent any future changes
        Parameters
        ----------
        val: str
            the value the cell should contain
        """
        self.set_value(val)
        self.original_val = val
        self.original = True

    def reset(self, guesses: bool = False):
        """
        Set the cell's value to its original value and delete all guesses
        Parameters
        ----------
        guesses: bool
            True if guesses should also be deleted, otherwise False
        """
        self.val = self.original_val
        if guesses:
            self.guesses = []


class Group:
    """A group is a set of cells where no cell should contain the same value"""

    def __init__(self, squares):
        """
        Parameters
        ----------
        squares: list of Squares
            all the Square objects in the group
        """
        self.squares = squares

    @property
    def valid(self):
        """
        Check if any non-blank cells in the group contain the same value
        Returns
        -------
        bool
            True if no repeated values, False otherwise
        """
        vals = [square.val for square in self.squares if square.val != "0"]
        return len(vals) == len(set(vals))


class Puzzle:
    """A sudoku puzzle"""

    def __init__(self, puzzle: str, size: int = 9):
        """
        Parameters
        ----------
        puzzle: str
            A string with the values that should be in the sudoku cells
        size: int
            The size of the sudoku puzzle (can be 4, 9 or 16)
        Attributes
        ----------
        self.vals: list of strs
            The values that can be placed in a cell
        self.groups: list of Groups
            All the groups that are in the puzzle
        """
        self.size = size
        if self.size == 4:
            vals = [str(val + 1) for val in range(4)]
        elif self.size == 9:
            vals = [str(val + 1) for val in range(9)]
        else:
            vals = [str(val + 1) for val in range(9)] + [char for char in "ABCDEFG"]
        self.vals = vals
        self.squares = [Square(puzzle[i]) for i in range(self.size ** 2)]
        self.groups = ([Group([self.squares[i + j * self.size] for i in range(self.size)]) for j in range(self.size)] +
                       [Group([self.squares[i * self.size + j] for i in range(self.size)]) for j in range(self.size)] +
                       [Group([self.squares[int((i // (self.size ** 0.5)) * self.size + i % (self.size ** 0.5) + (
                               j % (self.size ** 0.5)) * (self.size ** 0.5) + (j // (self.size ** 0.5)) * (
                                                        self.size ** 1.5))] for i in range(self.size)]) for
                        j in range(self.size)])
        self.check_valid()

    def return_clashes(self):
        """
        Loops through all the groups to check if any of them contain clashing values
        Returns
        -------
        set
            Empty set if no clashes, otherwise the indexes of any cells that contain a clash
        """
        clash = []
        for group in self.groups:
            for i in group.squares:
                for j in group.squares:
                    if i.val == j.val and i.val != "0" and i != j:
                        clash.append(self.squares.index(i))
                        clash.append(self.squares.index(j))
        return set(clash)

    def change_value(self, square, val):
        """
        Change the value held by a cell in the grid using its coordinates
        Parameters
        ----------
        square: int
            the index of the cell to be altered
        val: str
            the value the cell should store
        """
        if not self.squares[square].original:
            self.squares[square].set_value(val)

    def add_guess(self, square, val):
        """
        Add a guess for a cell in the grid using its coordinates
        Parameters
        ----------
        square: int
            the index of the cell to be altered
        val: str
            the value that has been guessed
        """
        self.squares[square].add_guess(val)

    def add_all_guesses(self):
        """For every non-original cell in the puzzle, add all values which would not cause a clash
         to the guesses list"""
        for cell in self.squares:
            if not cell.original:
                for val in self.vals:
                    cell.add_guess(val)
        for group in self.groups:
            for val in self.vals:
                if val in [cell.val for cell in group.squares]:
                    for cell in group.squares:
                        if not cell.original and val in cell.guesses:
                            cell.guesses.remove(val)

    def check_valid(self):
        """
        Check if there are repeated values in any group
        Returns
        -------
        bool
            True if there are no repeated values, otherwise False
        """
        return not (False in [group.valid for group in self.groups])

    def reset(self, guesses: bool = False):
        """
        Set the values of all cells in the group back to their original values
        Parameters
        -------
        guesses: bool
            True if guesses should also be deleted, False otherwise
        """
        for cell in self.squares:
            cell.reset(guesses)

    def num_solutions(self):
        """
        Check if there are no, one or several solutions
        Returns
        int
            0 if no solutions, 1 if exactly one solution, 2 if multiple solutions
        """
        if not self.solve():
            return 0
        solution = [cell.val for cell in self.squares][:-1]
        self.reset()
        if not self.solve(excl=solution):
            return 1
        else:
            return 2

    def solve(self, i=0, excl=None):
        """
        Attempt to solve the sudoku using backtracking
        Parameters
        ----------
        i: the index of a cell currently not filled
        excl: list
            A valid solution to the sudoku that should be ignored
        Returns
        -------
        Bool
            True if a solution (other than that given by excl) is found, otherwise False
        """
        # every square filled
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
        """
        Detect if the sudoku puzzle has been completed
        Returns
        -------
        bool
            True if completed, otherwise False
        """
        if self.check_valid() and "0" not in [cell.val for cell in self.squares]:
            return True
        else:
            return False

    def sandwich(self):
        """
        Finds the sum of values between 1 and 9 for every row and column
        Returns
        -------
        (list, list)
            First list for rows, second for columns
        """
        cols = []
        rows = []
        vals = [square.val for square in self.squares]
        for cell in self.squares:
            cell.reset()
        self.solve()
        for i in range(9):
            rows.append(self.sandwich_sums(i, True))
            cols.append(self.sandwich_sums(i, False))
        for i in range(len(self.squares)):
            self.squares[i].val = vals[i]
        return rows, cols

    def sandwich_sums(self, i, is_row=True):
        """Find the sum of values between 1 and 9 for a row/column
        Parameters
        -------
        i: int
            The row/column number
        is_row: bool
            Default True. True if a row, False if a column."""
        if is_row:
            line = [int(self.squares[9 * i + n].val) for n in range(9)]
        else:
            line = [int(self.squares[i + 9 * n].val) for n in range(9)]
        if line.index(9) > line.index(1):
            return sum(line[line.index(1) + 1:line.index(9)])
        else:
            return sum(line[line.index(9) + 1:line.index(1)])


class Game:
    def __init__(self, size: int = 9):
        """
        The Game class allows a puzzle to be created and then holds the puzzle
        Parameters
        ----------
        size: the size of the puzzle that is held
        Attributes
        ----------
        self.puzzle: Puzzle|None
            the puzzle that the Game is holding or None if no puzzle has been created
        """
        self.puzzle: Puzzle | None = None
        self.size = size
        self.vals = self.set_vals()

    def set_vals(self):
        """
        Return a list of the values that should be used in the sudoku based on the size of the sudoku
        Returns
        ----------
        list of strs
            A list containing all the values
        """
        if self.size == 16:
            vals = [char for char in "123456789ABCDEFGH"]
        else:
            vals = [str(digit + 1) for digit in range(self.size)]
        return vals

    def load_game(self, mode, arg: str, size=9):
        """
        Load a new sudoku puzzle
        Parameters
        ----------
        mode: str
            "user" if a user inputted puzzle should be loaded
            "load" if a specific puzzle should be loaded from a file
            "load_random" if a random puzzle should be loaded from a file
            "generate" if a new puzzle should be created
        arg: str
            if mode == "user", a string containing the values of the sudoku
            if mode == "load", the index of the puzzle in the list
            if mode == "load_random", the difficulty of the sudoku
            if mode == "generate", the number of blank cells
        size: int
            the size of the sudoku to be created
        Returns
        -------
        bool
            True if the puzzle was successfully loaded, otherwise False
        """
        if size != self.size:
            self.size = size
            self.vals = self.set_vals()
        if mode == "user":
            if len(arg) == self.size ** 2:
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

        elif mode == "load_random":
            if size == 9:
                with open("puzzles9.txt", "r") as file:
                    lines = [line.strip() for line in file]
                if arg.lower() == "easy":
                    self.puzzle = Puzzle(choice([puzzle for puzzle in lines if puzzle.count("0") < 30]), self.size)
                    return True
                elif arg.lower() == "medium":
                    self.puzzle = Puzzle(choice([puzzle for puzzle in lines if 30 <= puzzle.count("0") < 42]),
                                         self.size)
                    return True
                elif arg.lower() == "hard":
                    self.puzzle = Puzzle(choice([puzzle for puzzle in lines if 42 <= puzzle.count("0")]), self.size)
                    return True
                else:
                    return False
            else:
                with open(f"puzzles{size}.txt", "r") as file:
                    lines = [line.strip() for line in file]
                self.puzzle = Puzzle(choice(lines), self.size)
                return True

        elif mode == "generate":
            while not self.generate_puzzle(int(arg)):
                self.generate_puzzle(int(arg))
            return True

        else:
            return False

    def generate_puzzle(self, blanks):
        """
        Generate a new puzzle using backtracking
        Parameters
        ----------
        blanks: int
            Number of blank cells in the puzzle
        Returns
        -------
        bool
            True when the puzzle has been created
        """
        self.puzzle = Puzzle("0" * self.size ** 2, self.size)
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
        """
        Create a blank cell when generating a puzzle
        Returns
        -------
        int, str
            the index of the blank cell created and the value held by this cell before it was changed to a blank cell
        """
        n = randint(0, self.size ** 2 - 1)
        prev = self.puzzle.squares[n].val
        self.puzzle.squares[n].original = False
        self.puzzle.squares[n].original_val = "0"
        self.puzzle.squares[n].set_value("0")
        self.puzzle = Puzzle("".join([cell.val for cell in self.puzzle.squares]), self.size)
        return n, prev


if __name__ == "__main__":
    seed(0)
    game = Game(4)
    game.load_game("generate", "8", 16)
    print("".join([cell.val for cell in game.puzzle.squares]))
