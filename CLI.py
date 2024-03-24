import main

txt = "{:^3}{:^3}{:^3}|{:^3}{:^3}{:^3}|{:^3}{:^3}{:^3}"
while True:
    row = int(input("row"))
    col = int(input("col"))
    val = input("val")
    x = main.do_move(val, row, col)
    if x != "Valid":
        print(x)
    for i in range(9):
        print(txt.format(*[square.val for square in main.rows[i].vals]))
        if i == 2 or i == 5:
            print("-"*30)
