import new

def display_puzzle(text):
    for i in range(9):
        print("{:^3}{:^3}{:^3}|{:^3}{:^3}{:^3}|{:^3}{:^3}{:^3}".format(*[text.squares[(i, j)].val for j in range(9)]))
        if i == 2 or i == 5:
            print("-"*30)


puzzle = new.Puzzle(" 7 583 2  592  3  34   65 7795   632  36971  68   27  914835 76 3 7 1495567429 13")
display_puzzle(puzzle)
while True:
    row = int(input("row"))
    col = int(input("col"))
    val = input("val")
    x = puzzle.do_move(val, row, col)
    display_puzzle(puzzle)
