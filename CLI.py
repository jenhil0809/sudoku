import main
from random import randint


def load_game(size: int = 81):
    return main.Game(size)


def get_puzzle(game: main.Game):
    typ = input("Generate, load or user input: ").lower()
    if typ == "user":
        return game.load_game(typ, input("Puzzle: "))
    elif typ == "load":
        return game.load_game(typ, input("Line No: "))
    else:
        return game.load_game(typ, randint(10, 30))


def print_puzzle(puzzle: main.Puzzle):
    txt = "{:^3}{:^3}{:^3}|{:^3}{:^3}{:^3}|{:^3}{:^3}{:^3}"
    for i in range(9):
        print(txt.format(*[cell.val for cell in puzzle.squares[i * 9:i * 9 + 9]]))
        if i == 2 or i == 5:
            print("-" * 30)


def solve_puzzle(puzzle: main.Puzzle):
    print_puzzle(puzzle)
    while not puzzle.completed:
        row = int(input("row"))-1
        col = int(input("col"))-1
        val = input("val")
        puzzle.change_value(col + row * 9, val)
        # if move != "Valid":
        #    print(error message)
        print_puzzle(puzzle)


if __name__ == "__main__":
    game = load_game()
    while not get_puzzle(game):
        print("Invalid input")
    solve_puzzle(game.puzzle)
