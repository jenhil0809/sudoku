import main
from time import perf_counter
from matplotlib import pyplot as plt

with open("puzzles9.txt", "r") as file:
    lines = [line.strip() for line in file]
print(len([puzzle for puzzle in lines if 41 <= puzzle.count("0") <= 51]))
print(len([puzzle for puzzle in lines if 30 <= puzzle.count("0") < 41]))
print(len([puzzle for puzzle in lines if puzzle.count("0") < 30]))
with open("puzzles4.txt", "r") as file:
    print(len([line.strip() for line in file]))
with open("puzzles16.txt", "r") as file:
    print(len([line.strip() for line in file]))
print("______")

game = main.Game()
times = []
blanks = [i for i in range(0, 40)]
for i in range(0, 40):
    t_start = perf_counter()
    print(i)
    for n in range(3):
        game.load_game("generate", i)
    t_end = perf_counter()
    times.append((t_end - t_start)/3)

plt.scatter(blanks, times)
plt.show()
