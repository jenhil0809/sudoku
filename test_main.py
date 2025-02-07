import pytest

import main

puzzles = [main.Puzzle("070583020059200300340006507795000632003697100680002700914835076030701495567429013"),
           main.Puzzle("790058200004607058503002670040270506039500180670019002900701004068005700307480025"),
           main.Puzzle("913000500607000024050080070079000000002090043000004090040001900706009005001006407"),
           main.Puzzle("926571483351486279874923516582367194149258367763100825238700651617835942495612738"),
           main.Puzzle("270583020059200300340006507795000632003697100680002700914835076030701495567429013"),
           main.Puzzle("000000000000000000000000000000000000000000000000000000000000000000000000000000000"),
           main.Puzzle("071583020059200300340006507795000632003697100680002700914835076030701495567429013"),
           main.Puzzle("176583924859274361342916587795148632423697158681352749914835276238761495567429813"),
           main.Puzzle("0201100424133002", 4),
           main.Puzzle("0211100424133002", 4),
           main.Puzzle("308DC05B790F200G290CDAE00B0G6000500B00700623C00000060903D0E004000500900031070C0D000451C0000200G01000AD48509EFB20C2E80B37GD049100B00E1F000A0D030008C5009000B04GD040000CBA6E0518F2F03AG5004008B00984A30ED0005000009B0032F100D00E006C00000003FBD000E00008G01000390B", 4),
           main.Puzzle("308DC05B790F208G290CDAE00B0G6000500B00700623C00000060903D0E004000500900031070C0D000451C0000200G01000AD48509EFB20C2E80B37GD049100B00E1F000A0D030008C5009000B04GD040000CBA6E0518F2F03AG5004008B00984A30ED0005000009B0032F100D00E006C00000003FBD000E00008G01000390B", 4),
           ]

game = main.Game()


def test_num_solutions():
    assert puzzles[0].num_solutions() == 1 # valid
    assert puzzles[7].num_solutions() == 1 # completed
    assert puzzles[3].num_solutions() == 2 # multiple solutions
    assert puzzles[4].num_solutions() == 0 # clashing vals
    assert puzzles[5].num_solutions() == 2 # empty grid
    assert puzzles[6].num_solutions() == 0 # no solutions, but no clashes


def test_solve():
    puzzles[0].solve() # valid 9x9
    puzzles[1].solve() # valid 9x9
    puzzles[8].solve() # valid 4x4
    puzzles[7].solve() # already solved
    assert ("".join([cell.val for cell in puzzles[0].squares]) ==
            '176583924859274361342916587795148632423697158681352749914835276238761495567429813')
    assert ("".join([cell.val for cell in puzzles[1].squares]) ==
            "796358241124697358583142679841273596239564187675819432952731864468925713317486925")
    assert ("".join([cell.val for cell in puzzles[8].squares]) ==
            "4231132424133142")
    assert ("".join([cell.val for cell in puzzles[7].squares]) ==
            "176583924859274361342916587795148632423697158681352749914835276238761495567429813")


def test_reset():
    puzzles[0].change_value(1, "1")
    puzzles[0].change_value(2, "7")
    puzzles[0].change_value(2, "2")
    puzzles[0].change_value(9, "4")
    puzzles[0].reset() # values entered
    puzzles[2].reset() # no values entered
    assert ("".join([cell.val for cell in puzzles[0].squares]) ==
            '070583020059200300340006507795000632003697100680002700914835076030701495567429013')
    assert ("".join([cell.val for cell in puzzles[2].squares]) ==
            '913000500607000024050080070079000000002090043000004090040001900706009005001006407')


def test_check_valid():
    assert puzzles[0].check_valid() is True # 9x9 valid
    assert puzzles[4].check_valid() is False # 9x9 error
    assert puzzles[8].check_valid() is True # 4x4 valid
    assert puzzles[9].check_valid() is False # 4x4 error
    assert puzzles[10].check_valid() is True # 16x16 valid
    assert puzzles[11].check_valid() is False # 16x16 error


def test_change_value():
    puzzles[0].change_value(1, "1") # Original
    puzzles[0].change_value(2, "6") # Valid
    puzzles[0].change_value(6, "6") # Valid
    puzzles[0].change_value(2, "8") # Overwrite
    puzzles[0].change_value(6, "0") # Clear
    puzzles[0].change_value(100, "2")
    puzzles[0].change_value(8, "A")
    assert ("".join([cell.val for cell in puzzles[0].squares]) ==
            '078583020059200300340006507795000632003697100680002700914835076030701495567429013')


def test_completed():
    assert puzzles[0].completed is False
    assert puzzles[7].completed is True


def test_load_game():
    assert game.puzzle is None
    assert game.load_game("user",
                          "070583020059200300340006507795000632003697100680002700914835076030701495567429013") is True
    assert game.load_game("user",
                          "07058302005920030034000650779500063200369710068000270091483507603070149556742901") is False
    assert ("".join([cell.val for cell in game.puzzle.squares]) ==
            "070583020059200300340006507795000632003697100680002700914835076030701495567429013")
    assert game.load_game("load", "10") is True
    assert game.load_game("load", "1000") is False
    assert game.load_game("load_random", "hard") is True
    assert [square.val for square in game.puzzle.squares].count("0") >= 42
    assert game.load_game("generate", "20") is True
    assert game.puzzle.check_valid()

def test_sandwich():
    assert puzzles[0].sandwich() == ([29, 22, 0, 5, 7, 21, 0, 4, 8], [28, 10, 10, 0, 4, 0, 14, 0, 17])
    assert puzzles[1].sandwich() == ([28, 12, 19, 17, 15, 0, 17, 14, 25], [21, 35, 0, 22, 17, 0, 19, 17, 8])

def test_add_guess():
    puzzles[0].add_guess(1, "2")
    puzzles[0].add_guess(1, "1")
    assert puzzles[0].squares[1].guesses == ["1", "2"]
    puzzles[0].add_guess(1, "0")
    assert puzzles[0].squares[1].guesses == []

def test_add_all_guesses():
    puzzles[0].add_all_guesses()
    assert puzzles[0].squares[0].guesses == ["1"]
    assert puzzles[0].squares[1].guesses == []
    assert puzzles[0].squares[2].guesses == ["1", "6"]

def test_return_clashes():
    assert puzzles[1].return_clashes() == set()
    assert puzzles[4].return_clashes() == set([0, 7])
    assert puzzles[7].return_clashes() == set()
