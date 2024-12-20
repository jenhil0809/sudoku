import main
from time import perf_counter
from matplotlib import pyplot as plt

with open("puzzles9.txt", "r") as file:
    lines = [line.strip() for line in file]
print(len([puzzle for puzzle in lines if 43 <= puzzle.count("0") <= 51]))
print(len([puzzle for puzzle in lines if 30 <= puzzle.count("0") < 43]))
print(len([puzzle for puzzle in lines if puzzle.count("0") < 30]))
print("______")

game = main.Game()
times = []
blanks = [i for i in range(0, 50)]
for i in range(0, 50):
    t_start = perf_counter()
    print(i)
    for n in range(1):
        game.load_game("generate", i)
    t_end = perf_counter()
    times.append((t_end - t_start) / 2)

plt.scatter(blanks, times)
plt.show()
