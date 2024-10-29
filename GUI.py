import main
import tkinter as tk
import keyboard
import time


class GameApp(tk.Tk):
    """Holds the frames to be displayed and settings"""
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry("700x600")
        self.coord = tk.IntVar()
        self.show_highlights = tk.IntVar()
        self.game = main.Game()
        self.frame = LoadGameFrame(self)
        self.new_frame(LoadGameFrame(self))
        self.settings = {"hint_num": tk.IntVar(value=3),
                         "timer_on": tk.IntVar(),
                         "clashes": tk.IntVar(),
                         "dimensions": tk.IntVar(value=9),
                         "highlights": tk.IntVar(),
                         "sandwich": tk.IntVar(),
                         "display_moves": tk.IntVar(), }
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
        self.generate = tk.Button(self, text="Generate", command=self.generate_game)
        self.user = tk.Button(self, text="User input", command=self.input_game)
        self.load = tk.Button(self, text="Load", command=self.load_game)
        self.settings = tk.Button(self, text="Settings", command=self.master.open_settings)
        self.user_game_input = tk.Entry(self, textvariable=self.user_game)
        self.line_input = tk.Entry(self, textvariable=self.line_number)
        self.place_widgets()

    def generate_game(self):
        """Generates a new puzzle"""
        if self.master.game.load_game("generate", "30", self.master.settings["dimensions"].get()):
            self.master.new_frame(SudokuGrid(self.master))

    def input_game(self):
        """Loads a user inputted game"""
        if self.master.game.load_game("user", self.user_game.get(), self.master.settings["dimensions"].get()):
            self.master.new_frame(SudokuGrid(self.master))

    def load_game(self):
        """Load a game from memory"""
        if self.master.game.load_game("load", self.line_number.get(), self.master.settings["dimensions"].get()):
            self.master.new_frame(SudokuGrid(self.master))

    def place_widgets(self):
        """Places the required widgets on the screen"""
        self.generate.grid(row=0, column=0, columnspan=2)
        self.user.grid(row=1, column=0)
        self.user_game_input.grid(row=1, column=1)
        self.load.grid(row=2, column=0)
        self.line_input.grid(row=2, column=1)
        self.settings.grid(row=3, column=0)

    def setting_update(self):
        """If the dimensions of the puzzle are 16x16, a puzzle cannot be generated, so this option should be disabled"""
        if self.master.settings["dimensions"].get() == 16:
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
        for char in self.master.game.puzzle.vals:
            self.create_keyboard_event(char.lower())
        self.create_keyboard_event("0")
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
                                  command=lambda val=i: self.button_clicked(val + 1000), font='SegoeIU 6') for i in
                        range(self.master.settings["dimensions"].get() ** 2)]
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
        self.submit_button = tk.Button(self, text="Submit", command=self.change_val)
        self.settings = tk.Button(self, text="Settings", command=self.master.open_settings)
        if self.master.settings["dimensions"].get() == 16:
            self.hint_request.config(state="disabled")
            self.complete.config(state="disabled")
        self.add_all_guesses()
        self.all_guesses_shown = self.master.settings["display_moves"]
        self.place_widgets()
        self.update_timer()

    def update_timer(self):
        """
        Changes the text displayed by the self.timer object to the difference between the current time and the starting
        time every second after being called while the puzzle is not completed
        """
        if self.master.settings["timer_on"].get():
            self.timer.config(
                text=f"Time: {int(time.time() - self.start_time) // 60:02d}:"
                     f"{int(time.time() - self.start_time) % 60:02d}")
        else:
            self.timer.config(text="")
        tk.Tk.update(self)
        if not self.solved:
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
        self.remove_highlights()
        self.highlight_errors()

    def create_keyboard_event(self, x):
        """
        Creates a keyboard event that allows the value of self.val to be controlled by key presses
        Parameters
        ----------
        x: str
            The value that will trigger the response
        """
        keyboard.on_press_key(x, lambda _: self.output(x))

    def output(self, x):
        """
        When the "x" key is pressed, self.val is changed
        Parameters
        ----------
        x: str
            The value to set self.val to
        """
        if not self.solved:
            self.val.set(x)
            self.change_val()

    def solve(self):
        """
        If not solved, solves the puzzle and colors cells depending on if the user inputted the correct value
        """
        if not self.solved:
            self.solved = True
            previous_vals = [cell.val for cell in self.master.game.puzzle.squares]
            for cell in self.master.game.puzzle.squares:
                cell.reset()
            self.master.game.puzzle.solve()
            for i in range(len(self.squares)):
                self.complete.config(text="New puzzle")
                self.guesses[i].config(bg="light grey")
                if self.master.game.puzzle.squares[i].original:
                    self.squares[i].config(text=self.master.game.puzzle.squares[i].val, bg="light grey")
                elif previous_vals[i] == self.master.game.puzzle.squares[i].val:
                    self.squares[i].config(text=self.master.game.puzzle.squares[i].val, bg="palegreen")
                else:
                    self.squares[i].config(text=self.master.game.puzzle.squares[i].val, bg="firebrick1")

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
                if self.master.game.puzzle.squares[i].val == val:
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
                if self.val.get() != "0":
                    self.master.game.puzzle.add_guess(self.master.coord.get() - 1000,
                                                      str(self.val.get()).upper())
                    self.guesses[self.master.coord.get() - 1000].config(
                        text="".join(self.master.game.puzzle.squares[self.master.coord.get() - 1000].guesses))
                    self.place_widgets()
                else:
                    self.master.game.puzzle.squares[self.master.coord.get() - 1000].guesses = []
                    self.guesses[self.master.coord.get() - 1000].config(text=" ")
                    self.place_widgets()
            else:
                self.master.game.puzzle.change_value(self.master.coord.get(),
                                                     str(self.val.get()).upper())
                self.squares[self.master.coord.get()].config(
                    text=str(self.master.game.puzzle.squares[self.master.coord.get()].val))
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
        self.highlight_errors()

    def highlight_errors(self):
        """Any clashing cells are highlighted in red"""
        for square in self.squares:
            if square["bg"] == "firebrick1":
                square.config(bg="light grey")
        if self.master.settings["clashes"].get():
            for i in self.master.game.puzzle.return_clashes():
                self.squares[i].config(bg="firebrick1")

    def add_all_guesses(self):
        """The guesses cells are updated to all possible values which would not cause a clash if the dimensions of
        the puzzle are 4x4 or 9x9"""
        if self.master.settings["display_moves"].get() and self.master.settings["dimensions"].get() != 16:
            self.master.game.puzzle.add_all_guesses()
        for i in range(len(self.guesses)):
            self.guesses[i].config(text="".join(self.master.game.puzzle.squares[i].guesses))

    def setting_update(self):
        """Respond to any changes in the settings by changing the hint number, adding/removing highlights and changing
         guesses"""
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

    def show_hint(self):
        """If the cell is not one of the original cells, reveals the value that should be held by that cell and
        increments self.hints_taken by 1"""
        if self.master.coord.get() < 1000 and self.hints_taken < self.master.settings["hint_num"].get() and not \
                self.master.game.puzzle.squares[self.master.coord.get()].original:
            previous_vals = [cell.val for cell in self.master.game.puzzle.squares]
            self.master.game.puzzle.reset()
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

    def place_widgets(self):
        """Places the required widgets on the screen"""
        for i in range(self.master.settings["dimensions"].get() ** 2):
            self.squares[i].grid(row=i // self.master.settings["dimensions"].get() * 2 + 1 + i // int(
                self.master.settings["dimensions"].get() ** 1.5),
                                 column=i % int(self.master.settings["dimensions"].get()) + i % self.master.settings[
                                     "dimensions"].get() // int(self.master.settings["dimensions"].get() ** .5),
                                 padx=self.pad,
                                 pady=self.pad)
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

        self.timer.grid(row=1, column=50)
        self.hint_request.grid(row=2, column=50)
        self.submit_button.grid(row=3, column=50)
        self.complete.grid(row=4, column=50)
        self.settings.grid(row=5, column=50)
        self.give_up.grid(row=6, column=50)
        self.reset_button.grid(row=7, column=50)


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
        self.sandwich = tk.Checkbutton(self, variable=self.master.settings["sandwich"])
        self.dimensions = [
            (tk.Radiobutton(self, text=f"{i ** 2}x{i ** 2}", value=i ** 2, variable=self.master.settings["dimensions"]))
            for i in
            range(2, 5)]
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
        tk.Label(self, text="Sandwich sudoku").grid(row=2, column=0)
        self.sandwich.grid(row=2, column=1)
        tk.Label(self, text="Highlight clashes").grid(row=3, column=0)
        self.clash_highlight.grid(row=3, column=1)
        tk.Label(self, text="Highlight hints").grid(row=4, column=0)
        self.hints_highlight.grid(row=4, column=1)
        tk.Label(self, text="Display moves").grid(row=5, column=0)
        self.display_moves.grid(row=5, column=1)
        for i in range(3):
            self.dimensions[i].grid(row=6, column=i)
        self.return_button.grid(row=7, column=0)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
