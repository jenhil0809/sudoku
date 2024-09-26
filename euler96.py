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
# 24702 [0.05682780034840107, 0.08727800007909536, 6.165082899853587, 0.5306251002475619, 0.019093699753284454, 25.34685009997338, 1.1452054996043444, 0.016722199972718954, 48.65100990002975, 1.748325000051409, 6.122653400059789, 0.34793240018188953, 82.52771410020068, 24.396770199760795, 1.6167669999413192, 0.01745510008186102, 0.012696099933236837, 0.5892262002453208, 0.17675109999254346, 0.5928247002884746, 0.3707643002271652, 15.09023919980973, 5.017434800043702, 4.528027700260282, 1.1991632003337145, 3.337378399912268, 1.3716903999447823, 13.127191899809986, 4.758780899923295, 11.639304199721664, 17.21149760019034, 8.763861999846995, 0.06132359988987446, 0.21088689984753728, 0.981069799978286, 0.0689799003303051, 0.427224799990654, 0.3335372000001371, 0.08222880028188229, 0.09623789973556995, 49.03598570032045, 1.9385047000832856, 1.4475288996472955, 1.8018528004176915, 8.731755400076509, 1.092038800008595, 0.46639670012518764, 47.87092739995569, 0.5757424999028444, 5.352280099876225]