import main
import tkinter as tk
import keyboard
import time
from random import randint


class GameApp(tk.Tk):
    """Holds the frames to be displayed and settings"""

    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry(f"700x800")
        self.coord = tk.IntVar()
        self.game = main.Game()
        self.settings = {"hint_num": tk.IntVar(value=3),
                         "timer_on": tk.IntVar(),
                         "clashes": tk.IntVar(),
                         "dimensions": tk.IntVar(value=9),
                         "highlights": tk.IntVar(),
                         "sandwich": tk.IntVar(),
                         "display_moves": tk.IntVar(),
                         "difficulty": tk.StringVar(value="Medium"),
                         "time_limit": tk.DoubleVar(value=5),
                         "limit_on": tk.IntVar()}
        self.frame = LoadGameFrame(self)
        self.new_frame(LoadGameFrame(self))
        self.setting_frame = SettingsFrame(self)

    def new_frame(self, frame):
        """
        Deletes the old frame and loads the new one
        Parameters
        ----------
        frame = the frame to be loaded
        """
        self.frame.destroy()
        self.frame = frame
        frame.pack()
        try:
            self.setting_frame.pack_forget()
        except AttributeError:
            pass

    def open_settings(self):
        """Loads the settings frame over any other frame"""
        self.setting_frame.pack()
        self.frame.pack_forget()

    def close_settings(self):
        """Removes the setting frame and changes the screen depending on the new settings"""
        self.setting_frame.pack_forget()
        self.frame.setting_update()
        self.frame.pack()


class LoadGameFrame(tk.Frame):
    """Allows the user to load a game"""

    def __init__(self, master: GameApp):
        """
        Parameters
        ----------
        master: GameApp
            The object that holds this frame
        Attributes
        ----------
        self.user_game: tk.StringVar
            User input into the textbox for a user inputted game
        self.line_number: tk.Stringvar
            The line of the file the puzzle the user wants to load is on
        """
        super().__init__()
        self.master: GameApp = master
        self.user_game = tk.StringVar()
        self.line_number = tk.StringVar()
        self.generate = tk.Button(self, text="Generate", command=self.generate_game, width=80)
        self.user = tk.Button(self, text="User input", command=self.input_game, width=24)
        self.load = tk.Button(self, text="Load", command=self.load_game, width=36)
        self.load_any = tk.Button(self, text="Load random", command=self.load_random, width=80)
        self.settings = tk.Button(self, text="Settings", command=self.master.open_settings, width=80)
        self.user_game_input = tk.Entry(self, textvariable=self.user_game, width=64)
        self.line_input = tk.Entry(self, textvariable=self.line_number, width=50)
        self.setting_update()
        self.place_widgets()

    def generate_game(self):
        """Generates a new puzzle"""
        if self.master.settings["dimensions"].get() == 4:
            if self.master.game.load_game("generate", str(randint(2, 5)), 4):
                self.master.new_frame(SudokuGrid(self.master))
        elif self.master.settings["dimensions"].get() == 9:
            if self.master.settings["difficulty"].get() == "Easy":
                if self.master.game.load_game("generate", str(randint(15, 29)), 9):
                    self.master.new_frame(SudokuGrid(self.master))
            elif self.master.settings["difficulty"].get() == "Medium":
                if self.master.game.load_game("generate", str(randint(30, 40)), 9):
                    self.master.new_frame(SudokuGrid(self.master))
            elif self.master.settings["difficulty"].get() == "Hard":
                if self.master.game.load_game("generate", str(randint(41, 55)), 9):
                    self.master.new_frame(SudokuGrid(self.master))

    def input_game(self):
        """Loads a user inputted game"""
        if self.master.game.load_game("user", self.user_game.get(), self.master.settings["dimensions"].get()):
            self.master.new_frame(SudokuGrid(self.master))

    def load_game(self):
        """Load a game from memory"""
        if self.master.game.load_game("load", self.line_number.get(), self.master.settings["dimensions"].get()):
            self.master.new_frame(SudokuGrid(self.master))

    def load_random(self):
        """Load a random game from memory with a given difficulty level"""
        if self.master.game.load_game("load_random", self.master.settings["difficulty"].get(),
                                      self.master.settings["dimensions"].get()):
            self.master.new_frame(SudokuGrid(self.master))

    def place_widgets(self):
        """Places the required widgets on the screen"""
        self.generate.grid(row=0, column=0, columnspan=4)
        self.user.grid(row=1, column=0)
        self.user_game_input.grid(row=1, column=1, columnspan=3)
        self.load.grid(row=2, column=0, columnspan=2)
        self.line_input.grid(row=2, column=2, columnspan=2)
        self.load_any.grid(row=3, column=0, columnspan=4)
        self.settings.grid(row=4, column=0, columnspan=4)
        tk.Label(self, text="""\n\nGenerate: will create a new puzzle\n
        User input: write the sudoku in the textbox with blank squares represented by 0\n
        Load: input the puzzle number to load\n
        Load random: load a random puzzle from the database\n""").grid(row=5, column=0, columnspan=4)

    def setting_update(self):
        """If the dimensions of the puzzle are 16x16 or the difficulty level is hard, a puzzle cannot be generated,
        so this option should be disabled"""
        if self.master.settings["dimensions"].get() == 16:# or self.master.settings["difficulty"].get() == "Hard":
            self.generate.config(state="disabled")
        else:
            self.generate.config(state="normal")


class SudokuGrid(tk.Frame):
    """Displays the sudoku puzzle"""

    def __init__(self, master: GameApp):
        """
        Parameters
        ----------
        master: GameApp
            The object that holds this frame
        Attributes
        ----------
        self.solved: bool
            True if the puzzle has been completed, otherwise False
        self.hints_taken: int
            The number of hints the user has been given
        self.start_time: float
            Allows the time since the user began solving the puzzle to be calculated
        self.val: tk.StringVar
            The value a cell's value should be changed to
        """
        super().__init__()
        self.master: GameApp = master
        self.solved = False
        self.hints_taken = 0
        self.val = tk.StringVar(value="0")
        self.start_time = time.time()
        self.timer = tk.Label(self, text=f"{int(time.time() - self.start_time)}")
        self.arrow = False
        self.sandwich_vals = None
        keyboard.on_press_key("w", lambda _: self.move_square(False, -self.master.settings["dimensions"].get()))
        keyboard.on_press_key("up", lambda _: self.move_square(True, -self.master.settings["dimensions"].get()))
        keyboard.on_press_key("s", lambda _: self.move_square(False, self.master.settings["dimensions"].get()))
        keyboard.on_press_key("down", lambda _: self.move_square(True, self.master.settings["dimensions"].get()))
        keyboard.on_press_key("a", lambda _: self.move_square(False, -1))
        keyboard.on_press_key("left", lambda _: self.move_square(True, -1))
        keyboard.on_press_key("d", lambda _: self.move_square(False, 1))
        keyboard.on_press_key("right", lambda _: self.move_square(True, 1))
        for char in self.master.game.puzzle.vals:
            self.create_keyboard_event(char.lower(), char.lower())
        self.create_keyboard_event("backspace", "0")
        self.create_keyboard_event("delete", "0")
        self.create_keyboard_event("0", "0")
        if self.master.settings["dimensions"].get() == 4:
            h, w, self.pad = 4, 10, 5
        elif self.master.settings["dimensions"].get() == 9:
            h, w, self.pad = 2, 5, 5
        else:
            h, w, self.pad = 1, 2, 0
        self.squares = [tk.Button(self, text=master.game.puzzle.squares[i].val, height=h, width=w, bg="light grey",
                                  command=lambda val=i: self.button_clicked(val)) for i in
                        range(self.master.settings["dimensions"].get() ** 2)]
        self.guesses = [tk.Button(self, text=" ", height=1, width=w, bg="light grey",
                                  command=lambda val=i: self.button_clicked(val + 1000), font="SegoeIU 6", fg="gray23")
                        for i in range(self.master.settings["dimensions"].get() ** 2)]
        self.complete = tk.Button(self, text="Complete puzzle", command=self.solve)
        self.give_up = tk.Button(self, text="Return to menu",
                                 command=lambda: self.master.new_frame(LoadGameFrame(self.master)))
        self.reset_button = tk.Button(self, text="Reset puzzle", command=self.reset_puzzle)
        self.hint_request = tk.Button(self, text=f"Show hint ({self.master.settings['hint_num'].get()} left)",
                                      command=self.show_hint)
        for i in range(self.master.settings["dimensions"].get() ** 2):
            if master.game.puzzle.squares[i].val == "0":
                self.squares[i].config(text=" ")
            else:
                self.squares[i].config(font='SegoeIU 9 bold')
        self.settings = tk.Button(self, text="Settings", command=self.master.open_settings)
        if self.master.settings["dimensions"].get() == 16:
            self.hint_request.config(state="disabled")
            self.complete.config(state="disabled")
        self.add_all_guesses()
        self.all_guesses_shown = self.master.settings["display_moves"]
        self.sandwich = False
        self.master.coord.set(0)
        self.place_widgets()
        self.update_timer()

    def move_square(self, arrow_key, val):
        try:
            if not self.solved:
                if arrow_key:
                    self.arrow = True
                if 0 <= self.master.coord.get() + val < len(self.squares):
                    self.button_clicked(self.master.coord.get() + val)
        except tk.TclError:
            pass

    def update_timer(self):
        """
        Changes the text displayed by the self.timer object to the difference between the current time and the starting
        time every second after being called while the puzzle is not completed
        """
        if self.master.settings["timer_on"].get() and self.master.settings["limit_on"].get():
            self.timer.config(text=f"Time: {int(time.time() - self.start_time) // 60:02d}:"
                                   f"{int(time.time() - self.start_time) % 60:02d} / "
                                   f"{int((self.master.settings['time_limit'].get() * 60)) // 60:02d}:"
                                   f"{int((self.master.settings['time_limit'].get() * 60)) % 60:02d}")
        elif self.master.settings["timer_on"].get() and not self.master.settings["limit_on"].get():
            self.timer.config(text=f"Time: {int(time.time() - self.start_time) // 60:02d}:"
                                   f"{int(time.time() - self.start_time) % 60:02d}")
        else:
            self.timer.config(text="")
        tk.Tk.update(self)
        if not self.solved:
            if self.master.settings["limit_on"].get() and self.master.settings["time_limit"].get() * 60 <= int(
                    time.time() - self.start_time):
                self.solve()
            else:
                self.after(1000, self.update_timer)

    def reset_puzzle(self):
        """Resets any guesses, highlights, cell values entered, the timer and hint number"""
        self.master.game.puzzle.reset(True)
        self.hints_taken = 0
        self.hint_request.config(text=f"Show hint ({self.master.settings['hint_num'].get()} left)")
        self.start_time = time.time()
        for i in range(len(self.squares)):
            self.guesses[i].config(text="")
            self.squares[i].config(text=self.master.game.puzzle.squares[i].val)
            if self.master.game.puzzle.squares[i].val == "0":
                self.squares[i].config(text=" ")
        self.solved = False
        self.remove_highlights()
        self.highlight_errors()
        self.update_timer()

    def create_keyboard_event(self, trigger, response):
        """
        Creates a keyboard event that allows the value of self.val to be controlled by key presses
        Parameters
        ----------
        trigger: str
            The value that will trigger the response
        response: str
            The result of the keypress (usually same as input)
        """
        keyboard.on_press_key(trigger, lambda _: self.keypress(response))

    def keypress(self, x):
        """
        When the "x" key is pressed, self.val is changed
        Parameters
        ----------
        x: str
            The value to set self.val to
        """
        try:
            if not self.arrow:
                self.val.set(x)
                self.change_val()
            else:
                self.arrow = False
        except tk.TclError:
            pass

    def solve(self):
        """
        If not solved, solves the puzzle and colors cells depending on if the user inputted the correct value
        """
        if not self.solved:
            self.solved = True
            previous_vals = [cell.val for cell in self.master.game.puzzle.squares]
            for cell in self.master.game.puzzle.squares:
                cell.reset()
            self.master.game.puzzle.solve.cache_clear()
            self.master.game.puzzle.solve()
            for i in range(len(self.squares)):
                self.guesses[i].config(bg="light grey")
                if self.master.game.puzzle.squares[i].original:
                    self.squares[i].config(text=self.master.game.puzzle.squares[i].val, bg="light grey")
                elif previous_vals[i] == self.master.game.puzzle.squares[i].val:
                    self.squares[i].config(text=self.master.game.puzzle.squares[i].val, bg="spring green")
                else:
                    self.squares[i].config(text=self.master.game.puzzle.squares[i].val, bg="brown1")

    def button_clicked(self, val: int):
        """
        Responds to a button being clicked on
        Parameters
        ----------
        val: int
            The coordinate of the cell clicked on (if a normal cell val < 1000, if a guess val >= 1000)
        """
        if not self.solved:
            if self.master.coord.get() >= 1000:
                self.guesses[self.master.coord.get() - 1000].config(bg="light grey")
            else:
                self.squares[self.master.coord.get()].config(bg="light grey")
                self.remove_highlights()
            self.master.coord.set(val)
            if self.master.coord.get() >= 1000:
                self.guesses[self.master.coord.get() - 1000].config(bg="DeepSkyBlue2")
            else:
                self.highlight(self.master.game.puzzle.squares[self.master.coord.get()].val)
                self.squares[self.master.coord.get()].config(bg="DeepSkyBlue2")
            self.highlight_errors()

    def highlight(self, val):
        """
        Highlights all cells containing a specific value in pale blue
        Parameters
        ----------
        val: str
            The value the highlighted cells should contain
        """
        if val != "0" and self.master.settings["highlights"].get():
            for i in range(len(self.squares)):
                if self.master.game.puzzle.squares[i].val == val.upper():
                    self.squares[i].config(bg="lightblue1")
        self.squares[self.master.coord.get()].config(bg="DeepSkyBlue2")

    def remove_highlights(self):
        """All cells that are highlighted light blue have their highlights removed"""
        for cell in self.squares:
            if cell["bg"] == "lightblue1":
                cell.config(bg="light grey")

    def change_val(self):
        """The currently selected cell has its value changed to the value held by self.val"""
        if not self.solved:
            if self.master.coord.get() >= 1000:
                self.master.game.puzzle.add_guess(self.master.coord.get() - 1000,
                                                  str(self.val.get()).upper())
                if self.val.get() != "0":
                    self.guesses[self.master.coord.get() - 1000].config(
                        text=",".join(self.master.game.puzzle.squares[self.master.coord.get() - 1000].guesses))
                else:
                    self.guesses[self.master.coord.get() - 1000].config(text=" ")
                self.place_widgets()
            else:
                self.master.game.puzzle.change_value(self.master.coord.get(),
                                                     str(self.val.get()).upper())
                self.squares[self.master.coord.get()].config(
                    text=str(self.master.game.puzzle.squares[self.master.coord.get()].val), fg="gray15")
                if self.master.game.puzzle.squares[self.master.coord.get()].val == "0":
                    self.squares[self.master.coord.get()].config(text=" ")
                if self.master.game.puzzle.completed:
                    self.solve()
                else:
                    self.remove_highlights()
                    self.highlight(str(self.val.get()))
                    self.squares[self.master.coord.get()].config(bg="DeepSkyBlue2")
                    self.place_widgets()
                self.add_all_guesses()
        if not self.solved:
            self.highlight_errors()

    def highlight_errors(self):
        """Any clashing cells are highlighted in red"""
        for square in self.squares:
            if square["bg"] in ["brown1", "spring green"]:
                square.config(bg="light grey")
        if self.master.settings["clashes"].get():
            for i in self.master.game.puzzle.return_clashes():
                self.squares[i].config(bg="brown1")

    def add_all_guesses(self):
        """The guesses cells are updated to all possible values which would not cause a clash if the dimensions of
        the puzzle are 4x4 or 9x9"""
        if self.master.settings["display_moves"].get() and self.master.settings["dimensions"].get() != 16:
            self.master.game.puzzle.add_all_guesses()
        for i in range(len(self.guesses)):
            self.guesses[i].config(text=",".join(self.master.game.puzzle.squares[i].guesses))

    def setting_update(self):
        """Respond to any changes in the settings by changing the hint number, adding/removing highlights and changing
         guesses"""
        if not self.solved:
            if self.master.settings['hint_num'].get() > self.hints_taken:
                self.hint_request.config(
                    text=f"Show hint ({self.master.settings['hint_num'].get() - self.hints_taken} left)")
            else:
                self.hint_request.config(text="Show hint (0 left)")
            self.remove_highlights()
            self.highlight(self.master.game.puzzle.squares[self.master.coord.get()].val)
            self.highlight_errors()
            if self.all_guesses_shown and not self.master.settings['display_moves'].get():
                for cell in self.master.game.puzzle.squares:
                    cell.guesses = []
            else:
                self.add_all_guesses()
            if self.master.settings["sandwich"].get() and len(self.squares) == 81:
                self.add_sandwich()
            elif not self.master.settings["sandwich"].get() and self.sandwich:
                self.remove_sandwich()

    def show_hint(self):
        """If the cell is not one of the original cells, reveals the value that should be held by that cell and
        increments self.hints_taken by 1"""
        if self.master.coord.get() < 1000 and self.hints_taken < self.master.settings["hint_num"].get() and not \
                self.master.game.puzzle.squares[self.master.coord.get()].original:
            previous_vals = [cell.val for cell in self.master.game.puzzle.squares]
            self.master.game.puzzle.reset()
            self.master.game.puzzle.solve.cache_clear()
            self.master.game.puzzle.solve()
            self.val.set([square.val for square in self.master.game.puzzle.squares][self.master.coord.get()])
            for i in range(len(self.master.game.puzzle.squares)):
                self.master.game.puzzle.squares[i].set_value(previous_vals[i])
            self.change_val()
            self.hints_taken += 1
            self.hint_request.config(
                text=f"Show hint ({self.master.settings['hint_num'].get() - self.hints_taken} left)")
            for i in range(len(self.master.game.puzzle.squares)):
                if i != self.master.coord.get():
                    self.master.game.puzzle.squares[i].set_value(previous_vals[i])

    def add_sandwich(self):
        """Add required values for sandwich sudoku at end of rows/columns"""
        self.sandwich = True
        if self.sandwich_vals is None:
            self.sandwich_vals = self.master.game.puzzle.sandwich()
        for i in range(9):
            tk.Label(self, text=str(self.sandwich_vals[0][i])).grid(row=2 * i + i // 3 + 1, column=12)
            tk.Label(self, text=str(self.sandwich_vals[1][i])).grid(row=20, column=i + i // 3)

    def remove_sandwich(self):
        """Make the values at end of rows/columns blank"""
        self.sandwich = False
        for i in range(9):
            tk.Label(self, text="   ").grid(row=2 * i + i // 3 + 1, column=12)
            tk.Label(self, text="   ").grid(row=20, column=i + i // 3)

    def place_widgets(self):
        """Places the required widgets on the screen"""
        for i in range(self.master.settings["dimensions"].get() ** 2):
            self.squares[i].grid(row=i // self.master.settings["dimensions"].get() * 2 + 1 + i // int(
                self.master.settings["dimensions"].get() ** 1.5),
                                 column=i % int(self.master.settings["dimensions"].get()) + i % self.master.settings[
                                     "dimensions"].get() // int(self.master.settings["dimensions"].get() ** .5),
                                 padx=self.pad, pady=self.pad)
        for i in range(self.master.settings["dimensions"].get() ** 2):
            self.guesses[i].grid(row=i // int(self.master.settings["dimensions"].get()) * 2 + i // int(
                self.master.settings["dimensions"].get() ** 1.5),
                                 column=i % int(self.master.settings["dimensions"].get()) + i % int(
                                     self.master.settings["dimensions"].get()) // int(
                                     self.master.settings["dimensions"].get() ** .5), padx=self.pad, pady=0)
        for i in range(int(self.master.settings["dimensions"].get() ** 0.5 - 1)):
            tk.Label(self, text="_" * 100).grid(
                row=int((self.master.settings["dimensions"].get() ** 0.5) * 2 * (i + 1) + i), column=0,
                columnspan=int(self.master.settings["dimensions"].get() ** 0.5) + self.master.settings[
                    "dimensions"].get())
            tk.Label(self, text="|\n" * 35).grid(row=0, column=int(
                (self.master.settings["dimensions"].get() ** 0.5) * (i + 1) + i),
                    rowspan=int(self.master.settings["dimensions"].get() ** 0.5) +
                    self.master.settings["dimensions"].get() * 2)
        if self.master.settings["sandwich"].get() and len(self.squares) == 81:
            self.add_sandwich()
        self.timer.grid(row=1, column=50)
        self.hint_request.grid(row=2, column=50)
        self.complete.grid(row=3, column=50)
        self.give_up.grid(row=4, column=50)
        self.reset_button.grid(row=5, column=50)
        self.settings.grid(row=6, column=50)


class SettingsFrame(tk.Frame):
    """The frame that displays the settings selected"""

    def __init__(self, master: GameApp):
        """
        Parameters
        ----------
        master: GameApp
            The object that holds this frame
        Notes
        ----------
        hint_num: the maximum number of hints the user can be given
        timer_on: if the time taken will be displayed
        sandwich: if the sudoku should be a sandwich sudoku (9x9 only)
        dimensions: 4x4, 9x9, 16x16 puzzle
        clashes: if clashing cells should be highlighted in red
        highlights: if cells should be highlighted in blue if they contain the same value
        display_moves: if guesses should be automatically filled in (4x4 and 9x9 only)
        """
        super().__init__()
        self.master: GameApp = master
        self.hint_number = tk.Scale(self, from_=0, to=10, variable=self.master.settings["hint_num"],
                                    orient="horizontal")
        self.return_button = tk.Button(self, command=self.master.close_settings, text="Close settings")
        self.timer = tk.Checkbutton(self, variable=self.master.settings["timer_on"])
        self.timer.select()
        # Time limit
        self.limit_on = tk.Checkbutton(self, variable=self.master.settings["limit_on"])
        self.time_limit = tk.Spinbox(self, from_=0.5, to=30, increment=0.5,
                                     textvariable=self.master.settings["time_limit"])
        self.sandwich = tk.Checkbutton(self, variable=self.master.settings["sandwich"])
        self.dimensions = [
            (tk.Radiobutton(self, text=f"{i ** 2}x{i ** 2}", value=i ** 2, variable=self.master.settings["dimensions"]))
            for i in range(2, 5)]
        difficulties = ["Easy", "Medium", "Hard"]
        self.difficulty = [(tk.Radiobutton(self, text=f"{difficulties[i]}", value=difficulties[i],
                                            variable=self.master.settings["difficulty"])) for i in range(3)]
        self.clash_highlight = tk.Checkbutton(self, variable=self.master.settings["clashes"])
        self.clash_highlight.select()
        self.hints_highlight = tk.Checkbutton(self, variable=self.master.settings["highlights"])
        self.hints_highlight.select()
        self.display_moves = tk.Checkbutton(self, variable=self.master.settings["display_moves"])
        self.place_widgets()

    def place_widgets(self):
        """Places the required widgets on the screen"""
        tk.Label(self, text="Hint number").grid(row=0, column=0)
        self.hint_number.grid(row=0, column=1)
        tk.Label(self, text="Display timer").grid(row=1, column=0)
        self.timer.grid(row=1, column=1)
        tk.Label(self, text="Time limit").grid(row=2, column=0)
        self.limit_on.grid(row=2, column=1)
        self.time_limit.grid(row=2, column=2)
        tk.Label(self, text="Sandwich sudoku").grid(row=3, column=0)
        self.sandwich.grid(row=3, column=1)
        tk.Label(self, text="Highlight clashes").grid(row=4, column=0)
        self.clash_highlight.grid(row=4, column=1)
        tk.Label(self, text="Highlight hints").grid(row=5, column=0)
        self.hints_highlight.grid(row=5, column=1)
        tk.Label(self, text="Display moves").grid(row=6, column=0)
        self.display_moves.grid(row=6, column=1)
        for i in range(3):
            self.dimensions[i].grid(row=7, column=i)
        tk.Label(self, text="Difficulty level").grid(row=8, column=0)
        for i in range(3):
            self.difficulty[i].grid(row=9, column=i)
        self.return_button.grid(row=10, column=0)
        tk.Label(self, text="""Hint number: the maximum number of hints the user can be given\n
        Time limit: number of minutes\n
        Sandwich sudoku: sum of values between 1 and 9 displayed (9x9 only)\n
        Highlight clashes: clashing cells highlighted in red\n
        Highlights hints: cells highlighted in blue if they contain the same value\n
        Display moves: guesses are automatically filled in (4x4 and 9x9 only)""").grid(row=11, column=0, columnspan=3)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
