import main
from time import perf_counter
from matplotlib import pyplot as plt

game = main.Game()
times = []
blanks = [i for i in range(0, 50)]
for i in range(0, 50):
    t_start = perf_counter()
    print(i)
    for n in range(1):
        game.load_game("generate", i)
    t_end = perf_counter()
    times.append((t_end-t_start)/1)

plt.scatter(blanks, times)
plt.show()
