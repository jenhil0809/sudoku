import main
from random import randint

game = main.Game()
puzzles = []
for i in range(5):
    x = randint(50, 55)
    print(x)
    game.load_game("generate", str(x), 9)
    puzzle = "".join([cell.val for cell in game.puzzle.squares])
    puzzles.append(puzzle)
    (print(i))
for puzzle in puzzles:
    with open("puzzles9.txt", "a") as file:
        file.write(puzzle+"\n")
