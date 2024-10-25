import main
from random import randint

game = main.Game()
puzzles = []
for i in range(5):
    x = randint(10, 40)
    game.load_game("generate", x)
    puzzle = "".join([cell.val for cell in game.puzzle.squares])
    puzzles.append(puzzle)
for puzzle in puzzles:
    with open("puzzles9.txt", "a") as file:
        file.write(puzzle+"\n")
