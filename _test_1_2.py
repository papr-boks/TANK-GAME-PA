import io
import os.path
import unittest
from tkinter import Tk

from map import Map, Tile


class Test12(unittest.TestCase):
    tk: Tk

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()

    def test_map_diff__prev_none(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.ROCK

        self.assertEqual(
            [[True, True, True], [True, True, True], [True, True, True]],
            game_map.map_diff().tolist(),
        )

    def test_map_diff__no_change(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.ROCK
        game_map.map_diff()

        self.assertEqual(
            [[False, False, False], [False, False, False], [False, False, False]],
            game_map.map_diff().tolist(),
        )

    def test_map_diff__change(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.ROCK
        game_map.map_diff()

        game_map.map[1][1] = Tile.EMPTY

        self.assertEqual(
            [[False, False, False], [False, True, False], [False, False, False]],
            game_map.map_diff().tolist(),
        )


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test12."
    tests = list(filter(lambda _: _.startswith("test"), Test12.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test12)
    result = unittest.TextTestRunner(stream=temp_stream, verbosity=1).run(suite)
    match result.wasSuccessful(), test_num:
        case True, -1:
            print(f"All tests of {file_name} passed.")
        case False, -1:
            print(f"Some or all tests of {file_name} failed. Details:\n" + temp_stream.getvalue())
        case True, _:
            print(f"Test \"{tests[test_num]}\" passed.")
        case False, _:
            print(f"Test \"{tests[test_num]}\" failed. Details:\n" + temp_stream.getvalue())

if __name__ == "__main__":
    main()