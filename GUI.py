import main
import tkinter as tk


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry("700x600")
        self.coord = tk.IntVar()
        self.val = tk.IntVar()
        self.show_highlights = tk.IntVar()
        self.game = main.Game()
        self.frame = LoadGameFrame(self)
        self.new_frame(LoadGameFrame(self))
        self.guess_num = tk.IntVar(value=3)
        self.timer_on = tk.IntVar()
        self.dimensions = tk.IntVar(value=9)
        self.setting_frame = SettingsFrame(self)

    def new_frame(self, frame):
        self.frame.destroy()
        self.frame = frame
        frame.pack()
        try:
            self.setting_frame.pack_forget()
        except AttributeError:
            pass

    def open_settings(self):
        self.setting_frame.pack()
        self.frame.pack_forget()

    def close_settings(self):
        self.setting_frame.pack_forget()
        self.frame.pack()


class LoadGameFrame(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.master: GameApp = master
        self.user_game = tk.StringVar()
        self.line_number = tk.StringVar()
        self.generate = tk.Button(self, text="Generate", command=self.generate_game)
        self.user = tk.Button(self, text="User input", command=self.input_game)
        self.load = tk.Button(self, text="Load", command=self.load_game)
        self.settings = tk.Button(self, text="Settings", command=self.go_to_settings)
        self.user_game_input = tk.Entry(self, textvariable=self.user_game)
        self.line_input = tk.Entry(self, textvariable=self.line_number)
        self.place_widgets()

    def go_to_settings(self):
        self.master.open_settings()

    def generate_game(self):
        if self.master.game.load_game("generate", 30):
            self.master.new_frame(SudokuGrid(self.master))

    def input_game(self):
        if self.master.game.load_game("user", self.user_game.get()):
            self.master.new_frame(SudokuGrid(self.master))

    def load_game(self):
        if self.master.game.load_game("load", self.line_number.get()):
            self.master.new_frame(SudokuGrid(self.master))

    def place_widgets(self):
        self.generate.grid(row=0, column=0, columnspan=2)
        self.user.grid(row=1, column=0)
        self.user_game_input.grid(row=1, column=1)
        self.load.grid(row=2, column=0)
        self.line_input.grid(row=2, column=1)
        self.settings.grid(row=3, column=0)


class SudokuGrid(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.solved = False
        self.master: GameApp = master
        self.squares = [tk.Button(self, text=master.game.puzzle.squares[i].val, height=2, width=5, bg="light grey",
                                  command=lambda val=i: self.button_clicked(val)) for i in range(81)]
        self.guesses = [tk.Button(self, text=" ", height=1, width=5, bg="light grey",
                                  command=lambda val=i: self.button_clicked(val + 1000), font='SegoeIU 6') for i in
                        range(81)]
        self.complete = tk.Button(self, text="Complete puzzle", command=self.solve)
        for i in range(81):
            if master.game.puzzle.squares[i].val == "0":
                self.squares[i].config(text=" ")
            else:
                self.squares[i].config(font='SegoeIU 9 bold')
        self.val_input = tk.Scale(self, from_=0, to=9, orient="horizontal", variable=master.val)
        self.submit_button = tk.Button(self, text="Submit", command=self.change_val)
        self.settings = tk.Button(self, text="Settings", command=self.go_to_settings)
        # self.error_message = tk.Label(self, text="", wraplength=100)
        self.place_widgets()

    def solve(self):
        if not self.solved:
            self.solved = True
            previous_vals = [cell.val for cell in self.master.game.puzzle.squares]
            for cell in self.master.game.puzzle.squares:
                if not cell.original:
                    cell.reset()
            self.master.game.puzzle.solve()
            for i in range(len(self.squares)):
                self.complete.config(text="New puzzle")
                if self.master.game.puzzle.squares[i].original:
                    pass
                elif previous_vals[i] == self.master.game.puzzle.squares[i].val:
                    self.squares[i].config(text=self.master.game.puzzle.squares[i].val, bg="palegreen")
                else:
                    self.squares[i].config(text=self.master.game.puzzle.squares[i].val, bg="firebrick1")
        else:
            self.master.new_frame(LoadGameFrame(self.master))

    def button_clicked(self, val):
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

    def highlight(self, val):
        if val != "0" and self.master.show_highlights.get():
            for i in range(len(self.squares)):
                if self.master.game.puzzle.squares[i].val == val:
                    self.squares[i].config(bg="lightblue1")

    def remove_highlights(self):
        for cell in self.squares:
            if cell["bg"] == "lightblue1":
                cell.config(bg="light grey")

    def changed_coord(self):
        for square in self.squares:
            square.config(bg="light grey")
        self.squares[self.master.coord.get()].config(bg="DeepSkyBlue2")

    def change_val(self):
        if not self.solved:
            if self.master.coord.get() >= 1000:
                if self.master.val.get() != 0:
                    self.master.game.puzzle.add_guess(self.master.coord.get() - 1000, str(self.master.val.get()))
                    self.guesses[self.master.coord.get() - 1000].config(
                        text="".join(self.master.game.puzzle.squares[self.master.coord.get() - 1000].guesses))
                    self.place_widgets()
                else:
                    self.master.game.puzzle.squares[self.master.coord.get() - 1000].guesses = []
                    self.guesses[self.master.coord.get() - 1000].config(text=" ")
                    self.place_widgets()
            else:
                self.master.game.puzzle.change_value(self.master.coord.get(),
                                                     str(self.master.val.get()))
                self.squares[self.master.coord.get()].config(
                    text=str(self.master.game.puzzle.squares[self.master.coord.get()].val))
                if self.master.game.puzzle.squares[self.master.coord.get()].val == "0":
                    self.squares[self.master.coord.get()].config(text=" ")
                if self.master.game.puzzle.completed:
                    self.solve()
                else:
                    self.remove_highlights()
                    self.highlight(str(self.master.val.get()))
                    self.squares[self.master.coord.get()].config(bg="DeepSkyBlue2")
                    self.place_widgets()

    def go_to_settings(self):
        self.master.open_settings()

    def place_widgets(self):
        for i in range(81):
            self.squares[i].grid(row=(i // 9) * 2 + 1 + i // 27, column=i % 9 + i % 9 // 3, padx=5, pady=0)
        for i in range(81):
            self.guesses[i].grid(row=(i // 9) * 2 + i // 27, column=i % 9 + i % 9 // 3, padx=5, pady=0)
        tk.Label(self, text="_" * 100).grid(row=6, column=0, columnspan=11)
        tk.Label(self, text="_" * 100).grid(row=13, column=0, columnspan=11)
        tk.Label(self, text="|\n" * 35).grid(row=0, column=3, rowspan=22)
        tk.Label(self, text="|\n" * 35).grid(row=0, column=7, rowspan=22)
        tk.Label(self, text="Value:").grid(row=1, column=12)
        self.val_input.grid(row=0, column=13, rowspan=2)
        self.submit_button.grid(row=3, column=13)
        self.complete.grid(row=4, column=13)
        self.settings.grid(row=5, column=13)


class SettingsFrame(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.master: GameApp = master
        self.hint_number = tk.Scale(self, from_=0, to=10, variable=self.master.guess_num, orient="horizontal")
        self.return_button = tk.Button(self, command=self.return_to_frame, text="Close settings")
        self.timer = tk.Checkbutton(self, variable=self.master.timer_on)
        self.timer.select()
        # Time limit
        self.sandwich = tk.Checkbutton(self)
        self.dimensions = [
            (tk.Radiobutton(self, text=f"{i ** 2}x{i ** 2}", value=i ** 2, variable=self.master.dimensions)) for i in
            range(2, 5)]
        self.clash_highlight = tk.Checkbutton(self)
        self.clash_highlight.select()
        self.hints_highlight = tk.Checkbutton(self, variable=self.master.show_highlights)
        self.hints_highlight.select()
        self.display_moves = tk.Checkbutton(self)
        self.place_widgets()

    def return_to_frame(self):
        self.master.close_settings()

    def place_widgets(self):
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
