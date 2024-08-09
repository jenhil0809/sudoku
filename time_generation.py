import main
from time import perf_counter
from matplotlib import pyplot as plt

game = main.Game()
times = []
blanks = [i for i in range(0, 60)]
for i in range(0, 60):
    t_start = perf_counter()
    for n in range(5):
        game.load_game("generate", 0)
    t_end = perf_counter()
    times.append((t_end-t_start)/5)

plt.scatter(blanks, times)
plt.show()
