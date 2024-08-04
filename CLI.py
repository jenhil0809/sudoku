import main

puzzle = main.Puzzle("070583020059200300340006507795000632003697100680002700914835076030701495567429013")
txt = "{:^3}{:^3}{:^3}|{:^3}{:^3}{:^3}|{:^3}{:^3}{:^3}"
while not puzzle.completed:
    row = int(input("row"))
    col = int(input("col"))
    val = input("val")
    puzzle.change_value(col+row*9, val)
    # if move != "Valid":
    #    print(error message)
    for i in range(9):
        print(txt.format(*[cell.val for cell in puzzle.squares[i*9:i*9+9]]))
        if i == 2 or i == 5:
            print("-"*30)
