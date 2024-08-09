import main
import tkinter as tk


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.row = tk.IntVar()
        self.col = tk.IntVar()
        self.val = tk.IntVar()
        self.game = main.Game()
        self.game.load_game("user",
                            "070583020059200300340006507795000632003697100680002700914835076030701495567429013")
        self.sudoku_grid = Game(self)
        self.sudoku_grid.pack()


class Game(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.master: GameApp = master
        self.squares = [tk.Button(self, text=master.game.puzzle.squares[i].val, height=2, width=5, bg="light grey",
                                  command=lambda val=i: self.button_clicked(val)) for i in range(81)]
        for i in range(81):
            if master.game.puzzle.squares[i].val == "0":
                self.squares[i].config(text=" ")
        self.val_input = tk.Scale(self, from_=0, to=9, orient="horizontal", variable=master.val)
        self.submit_button = tk.Button(self, text="Submit", command=self.change_val)
        self.error_message = tk.Label(self, text="", wraplength=100)
        self.place_widgets()

    def button_clicked(self, val):
        self.squares[(self.master.row.get()) * 9 + (self.master.col.get())].config(bg="light grey")
        self.master.row.set(val // 9)
        self.master.col.set(val % 9)
        self.squares[(self.master.row.get()) * 9 + (self.master.col.get())].config(bg="lightblue1")

    def changed_coord(self):
        for square in self.squares:
            square.config(bg="light grey")
        self.squares[(self.master.row.get()) * 9 + (self.master.col.get())].config(bg="lightblue1")

    def change_val(self):
        self.master.game.puzzle.change_value(9*(self.master.row.get())+self.master.col.get(),
                                             str(self.master.val.get()))
        self.squares[9*(self.master.row.get())+self.master.col.get()].config(text=str(self.master.val.get()))
        self.place_widgets()

    def place_widgets(self):
        for i in range(81):
            self.squares[i].grid(row=i // 9 + i // 27, column=i % 9 + i % 9 // 3, padx=5, pady=5)
        tk.Label(self, text="_" * 100).grid(row=3, column=0, columnspan=11)
        tk.Label(self, text="_" * 100).grid(row=7, column=0, columnspan=11)
        tk.Label(self, text="|\n" * 35).grid(row=0, column=3, rowspan=11)
        tk.Label(self, text="|\n" * 35).grid(row=0, column=7, rowspan=11)
        tk.Label(self, text="Value:").grid(row=0, column=12)
        self.val_input.grid(row=0, column=13)
        self.submit_button.grid(row=3, column=13)
        self.error_message.grid(row=4, column=12, columnspan=2, rowspan=3)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
