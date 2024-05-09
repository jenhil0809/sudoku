import new


# displays the puzzle
def display_puzzle(text):
    for i in range(9):
        print("{:^3}{:^3}{:^3}|{:^3}{:^3}{:^3}|{:^3}{:^3}{:^3}".format(*[text.squares[(i, j)].val for j in range(9)]))
        if i == 2 or i == 5:
            print("-" * 30)

solved = False
# puzzle = new.Puzzle(" 7 583 2  592  3  34   65 7795   632  36971  68   27  914835 76 3 7 1495567429 13")
puzzle = new.Puzzle("53467891267219534819834256785976142342685379171392485696153728428741963534528617 ")
display_puzzle(puzzle)
while not solved:
    row = input("row")
    col = input("col")
    val = input("val")
    x = puzzle.do_move(val, row, col)
    if x == 1:
        print("Error: this square is set originally")
    elif x == 2:
        print("Error: this square does not exist")
    elif x == 3:
        print("Error: value must be between 1 and 9")
    elif x == 0:
        display_puzzle(puzzle)
    else:
        display_puzzle(puzzle)
        print("Solved!")
        solved = True # end of while loop
