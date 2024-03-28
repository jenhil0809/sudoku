import main
import tkinter as tk


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = "Sudoku"
        self.row = tk.IntVar()
        self.col = tk.IntVar()
        self.val = tk.IntVar()
        self.game = Game(self)
        self.game.pack()


class Game(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.master: GameApp = master
        self.squares = [tk.Button(self, text=main.puzzle[i], height=2, width=5, bg="light grey",
                                  command=lambda val=i: self.button_clicked(val)) for i in range(81)]
        self.squares[0].config(bg="lightblue1")
        self.val_input = tk.Scale(self, from_=0, to=9, orient="horizontal", variable=master.val)
        self.row_input = tk.Scale(self, from_=1, to=9, orient="horizontal", variable=master.row, command=self.changed_coord)
        self.col_input = tk.Scale(self, from_=1, to=9, orient="horizontal", variable=master.col, command=self.changed_coord)
        self.submit_button = tk.Button(self, text="Submit", command=self.change_val)
        self.error_message = tk.Label(self, text="", wraplength=100)
        self.place_widgets()

    def button_clicked(self, val):
        self.squares[(self.master.row.get() - 1) * 9 + (self.master.col.get() - 1)].config(bg="light grey")
        self.master.row.set(val // 9 + 1)
        self.master.col.set(val % 9 + 1)
        self.squares[(self.master.row.get() - 1) * 9 + (self.master.col.get() - 1)].config(bg="lightblue1")

    def changed_coord(self, *args):
        for square in self.squares:
            square.config(bg="light grey")
        self.squares[(self.master.row.get() - 1) * 9 + (self.master.col.get() - 1)].config(bg="lightblue1")


    def change_val(self):
        if main.do_move(str(self.master.val.get()), self.master.row.get() - 1, self.master.col.get() - 1) == "Valid":
            if self.master.val.get() != 0:
                self.squares[(self.master.row.get() - 1) * 9 + (self.master.col.get() - 1)] = tk.Button(self, text=str(
                    self.master.val.get()), height=2, width=5)
            else:
                self.squares[(self.master.row.get() - 1) * 9 + (self.master.col.get() - 1)] = tk.Button(self, text="",
                                                                                                        height=2,
                                                                                                        width=5)
            self.error_message.config(text="")
        else:
            self.error_message.config(
                text=main.do_move(str(self.master.val.get()), self.master.row.get() - 1, self.master.col.get() - 1))
        self.place_widgets()

    def place_widgets(self):
        for i in range(81):
            self.squares[i].grid(row=i // 9 + i // 27, column=i % 9 + i % 9 // 3, padx=5, pady=5)
        tk.Label(self, text="_" * 100).grid(row=3, column=0, columnspan=11)
        tk.Label(self, text="_" * 100).grid(row=7, column=0, columnspan=11)
        tk.Label(self, text="|\n" * 35).grid(row=0, column=3, rowspan=11)
        tk.Label(self, text="|\n" * 35).grid(row=0, column=7, rowspan=11)
        tk.Label(self, text="Value:").grid(row=0, column=12)
        tk.Label(self, text="Column").grid(row=2, column=12)
        tk.Label(self, text="Row").grid(row=1, column=12)
        self.val_input.grid(row=0, column=13)
        self.row_input.grid(row=1, column=13)
        self.col_input.grid(row=2, column=13)
        self.submit_button.grid(row=3, column=13)
        self.error_message.grid(row=4, column=12, columnspan=2, rowspan=3)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
