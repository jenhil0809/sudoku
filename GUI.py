import main
import tkinter as tk
from time import sleep


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry("700x600")
        self.coord = tk.IntVar()
        self.val = tk.IntVar()
        self.game = main.Game()
        self.frame = LoadGameFrame(self)
        self.new_frame(LoadGameFrame(self))

    def new_frame(self, frame):
        self.frame.destroy()
        self.frame = frame
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
        self.user_game_input = tk.Entry(self, textvariable=self.user_game)
        self.line_input = tk.Entry(self, textvariable=self.line_number)
        self.place_widgets()

    def generate_game(self):
        if self.master.game.load_game("generate", 10):
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


class SudokuGrid(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.master: GameApp = master
        self.squares = [tk.Button(self, text=master.game.puzzle.squares[i].val, height=2, width=5, bg="light grey",
                                  command=lambda val=i: self.button_clicked(val)) for i in range(81)]
        self.guesses = [tk.Button(self, text=" ", height=1, width=5, bg="light grey",
                                  command=lambda val=i: self.button_clicked(val + 1000), font='SegoeIU 6') for i in
                        range(81)]
        for i in range(81):
            if master.game.puzzle.squares[i].val == "0":
                self.squares[i].config(text=" ")
            else:
                self.squares[i].config(font='SegoeIU 9 bold')
        self.val_input = tk.Scale(self, from_=0, to=9, orient="horizontal", variable=master.val)
        self.submit_button = tk.Button(self, text="Submit", command=self.change_val)
        # self.error_message = tk.Label(self, text="", wraplength=100)
        self.place_widgets()

    def button_clicked(self, val):
        if self.master.coord.get() >= 1000:
            self.guesses[self.master.coord.get() - 1000].config(bg="light grey")
        else:
            self.squares[self.master.coord.get()].config(bg="light grey")
        self.master.coord.set(val)
        if self.master.coord.get() >= 1000:
            self.guesses[self.master.coord.get() - 1000].config(bg="lightblue1")
        else:
            self.squares[self.master.coord.get()].config(bg="lightblue1")

    def changed_coord(self):
        for square in self.squares:
            square.config(bg="light grey")
        self.squares[self.master.coord.get()].config(bg="lightblue1")

    def change_val(self):
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
            if self.master.val.get() != 0:
                self.master.game.puzzle.change_value(self.master.coord.get(),
                                                     str(self.master.val.get()))
                self.squares[self.master.coord.get()].config(text=str(self.master.val.get()))
            else:
                self.squares[self.master.coord.get()].config(text=" ")
            if self.master.game.puzzle.completed:
                for cell in self.squares:
                    cell.config(bg="green")
                self.master.frame.update_idletasks()
                sleep(2)
                self.master.new_frame(LoadGameFrame(self.master))
            else:
                self.place_widgets()

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
        # self.error_message.grid(row=4, column=12, columnspan=2, rowspan=3)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
