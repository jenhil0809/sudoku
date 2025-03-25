import main
from time import perf_counter

puzzles = []
times = []
with (open("euler96.txt", "r") as file):
    puzzle = ""
    for line in [line.strip() for line in file]:
        if line[0] == "G":
            if puzzle != "":
                t_start = perf_counter()
                puzzle = main.Puzzle(puzzle)
                puzzle.solve()
                puzzles.append(puzzle)
                t_end = perf_counter()
                times.append(t_end - t_start)
            puzzle = ""
        else:
            puzzle += line
    t_start = perf_counter()
    puzzle = main.Puzzle(puzzle)
    puzzle.solve()
    puzzles.append(puzzle)
    t_end = perf_counter()
    times.append(t_end - t_start)

total = 0
for puzzle in puzzles:
    total += int(puzzle.squares[0].val+puzzle.squares[1].val+puzzle.squares[2].val)
print(total, times)
print(sum(times)/len(puzzles), len(puzzles), min(times), max(times))
