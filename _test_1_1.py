import io
import os.path
import unittest
from tkinter import Tk

from map import Tile, create_map


class Test11(unittest.TestCase):
    tk: Tk

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()

    def test_read_from__size_3_3(self):
        game_map = create_map(". . .\n" ". . .\n" ". . .\n")
        self.assertEqual(game_map.cols, 3)
        self.assertEqual(game_map.rows, 3)

    def test_read_from__size_10_10(self):
        game_map = create_map(
            ". . . . . . . . . .\n"
            ". . . . . . . . . .\n"
            ". . . . . . . . . .\n"
            ". . . . . . . . . .\n"
            ". . . . . . . . . .\n"
            ". . . . . . . . . .\n"
            ". . . . . . . . . .\n"
            ". . . . . . . . . .\n"
            ". . . . . . . . . .\n"
            ". . . . . . . . . .\n"
        )
        self.assertEqual(game_map.cols, 10)
        self.assertEqual(game_map.rows, 10)

    def test_read_from__size_9_3(self):
        game_map = create_map(
            ". . . . . . . . .\n" ". . . . . . . . .\n" ". . . . . . . . .\n"
        )
        self.assertEqual(game_map.cols, 9)
        self.assertEqual(game_map.rows, 3)

    def test_read_from__empty_tile(self):
        game_map = create_map(". . .\n" ". . .\n" ". . .\n")

        self.assertEqual(game_map.map[0][0], Tile.EMPTY)
        self.assertEqual(game_map.map[0][1], Tile.EMPTY)
        self.assertEqual(game_map.map[0][2], Tile.EMPTY)
        self.assertEqual(game_map.map[1][0], Tile.EMPTY)
        self.assertEqual(game_map.map[1][1], Tile.EMPTY)
        self.assertEqual(game_map.map[1][2], Tile.EMPTY)
        self.assertEqual(game_map.map[2][0], Tile.EMPTY)
        self.assertEqual(game_map.map[2][1], Tile.EMPTY)
        self.assertEqual(game_map.map[2][2], Tile.EMPTY)

    def test_read_from__rock(self):
        game_map = create_map(". . .\n" ". # .\n" ". . .\n")

        self.assertEqual(game_map.map[0][0], Tile.EMPTY)
        self.assertEqual(game_map.map[0][1], Tile.EMPTY)
        self.assertEqual(game_map.map[0][2], Tile.EMPTY)
        self.assertEqual(game_map.map[1][0], Tile.EMPTY)
        self.assertEqual(game_map.map[1][1], Tile.ROCK)
        self.assertEqual(game_map.map[1][2], Tile.EMPTY)
        self.assertEqual(game_map.map[2][0], Tile.EMPTY)
        self.assertEqual(game_map.map[2][1], Tile.EMPTY)
        self.assertEqual(game_map.map[2][2], Tile.EMPTY)

    def test_read_from__bomb(self):
        game_map = create_map(". . .\n" ". @ .\n" ". . .\n")

        self.assertEqual(game_map.map[0][0], Tile.EMPTY)
        self.assertEqual(game_map.map[0][1], Tile.EMPTY)
        self.assertEqual(game_map.map[0][2], Tile.EMPTY)
        self.assertEqual(game_map.map[1][0], Tile.EMPTY)
        self.assertEqual(game_map.map[1][1], Tile.BOMB)
        self.assertEqual(game_map.map[1][2], Tile.EMPTY)
        self.assertEqual(game_map.map[2][0], Tile.EMPTY)
        self.assertEqual(game_map.map[2][1], Tile.EMPTY)
        self.assertEqual(game_map.map[2][2], Tile.EMPTY)

    def test_read_from__tank(self):
        game_map = create_map("0 . .\n" ". . .\n" ". . 1\n")

        self.assertEqual(game_map.tank_position_map[0], (0.5, 0.5))
        self.assertEqual(game_map.tank_position_map[1], (2.5, 2.5))

    def test_read_from__tank_coordinate(self):
        game_map = create_map(". 0 .\n" ". . .\n" ". . 1\n")

        self.assertEqual(game_map.tank_position_map[0], (1.5, 0.5))
        self.assertEqual(game_map.tank_position_map[1], (2.5, 2.5))

    def test_read_from__complete(self):
        game_map = create_map("0 . .\n" ". # .\n" ". @ 1\n")

        self.assertEqual(game_map.cols, 3)
        self.assertEqual(game_map.rows, 3)

        self.assertEqual(game_map.map[0][0], Tile.EMPTY)
        self.assertEqual(game_map.map[0][1], Tile.EMPTY)
        self.assertEqual(game_map.map[0][2], Tile.EMPTY)
        self.assertEqual(game_map.map[1][0], Tile.EMPTY)
        self.assertEqual(game_map.map[1][1], Tile.ROCK)
        self.assertEqual(game_map.map[1][2], Tile.EMPTY)
        self.assertEqual(game_map.map[2][0], Tile.EMPTY)
        self.assertEqual(game_map.map[2][1], Tile.BOMB)
        self.assertEqual(game_map.map[2][2], Tile.EMPTY)

        self.assertEqual(game_map.tank_position_map[0], (0.5, 0.5))
        self.assertEqual(game_map.tank_position_map[1], (2.5, 2.5))

def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test11."
    tests = list(filter(lambda _: _.startswith("test"), Test11.__dict__.keys()))
    append_len = len(tests) // 10
    prompt = f"{0:{append_len}}: All tests\n" + "\n".join([f"{i + 1:{append_len}}: {j}" for i, j in enumerate(tests)]) + "\nEnter a test number: "

    test_num = None
    while test_num is None:
        try:
            if interactive:
                test_num = int(input(prompt)) - 1
            else:
                test_num = -1
            if test_num < -1 or test_num >= len(tests):
                raise ValueError
        except ValueError:
            print("Invalid input.")
            test_num = None

    temp_stream = io.StringIO()
    if test_num != -1:
        suite = unittest.TestLoader().loadTestsFromName(name + tests[test_num])
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test11)
    result = unittest.TextTestRunner(stream=temp_stream, verbosity=1).run(suite)
    match result.wasSuccessful(), test_num:
        case True, -1:
            print(f"All tests of {file_name} passed.")
        case False, -1:
            print(f"Some or all tests of {file_name} failed. Details:\n" + temp_stream.getvalue())
        case True, n:
            print(f"Test \"{tests[n]}\" passed.")
        case False, n:
            print(f"Test \"{tests[n]}\" failed. Details:\n" + temp_stream.getvalue())

if __name__ == "__main__":
    main()

