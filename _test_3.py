import io
import os.path
import unittest
from tkinter import Tk, Canvas

from map import Map, Tile


class Test3(unittest.TestCase):
    tk: Tk

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()

    def test_trigger_bomb__one(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.BOMB

        canvas = Canvas(Test3.tk, width=game_map.width, height=game_map.height)

        def trigger_bomb_callback(col, row):
            self.assertEqual(1, col)
            self.assertEqual(1, row)

        game_map.trigger_bomb(canvas, 1, 1, trigger_bomb_callback)

        # test whether all bombs have been triggered
        self.assertTrue((Map(3, 3).map == game_map.map).all())

    def test_trigger_bomb__two(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.BOMB
        game_map.map[0][0] = Tile.BOMB

        canvas = Canvas(Test3.tk, width=game_map.width, height=game_map.height)

        to_be_triggered = [(0, 0), (1, 1)]

        def trigger_bomb_callback(col, row):
            self.assertIn((col, row), to_be_triggered)
            to_be_triggered.remove((col, row))

        game_map.trigger_bomb(canvas, 1, 1, trigger_bomb_callback)

        self.assertTrue((Map(3, 3).map == game_map.map).all())
        self.assertListEqual([], to_be_triggered)

    def test_trigger_bomb__many(self):
        game_map = Map(3, 3)
        game_map.map[0][0] = Tile.BOMB
        game_map.map[0][1] = Tile.BOMB
        game_map.map[0][2] = Tile.BOMB
        game_map.map[1][0] = Tile.BOMB
        game_map.map[1][1] = Tile.BOMB
        game_map.map[1][2] = Tile.BOMB
        game_map.map[2][0] = Tile.BOMB
        game_map.map[2][1] = Tile.BOMB
        game_map.map[2][2] = Tile.BOMB

        canvas = Canvas(Test3.tk, width=game_map.width, height=game_map.height)

        to_be_triggered = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        ]

        def trigger_bomb_callback(col, row):
            self.assertIn((col, row), to_be_triggered)
            to_be_triggered.remove((col, row))

        game_map.trigger_bomb(canvas, 1, 1, trigger_bomb_callback)

        self.assertTrue((Map(3, 3).map == game_map.map).all())
        self.assertListEqual([], to_be_triggered)

    def test_trigger_bomb__rock_and_gap(self):
        game_map = Map(3, 3)
        game_map.map[0][0] = Tile.BOMB
        game_map.map[0][1] = Tile.EMPTY
        game_map.map[0][2] = Tile.BOMB
        game_map.map[1][0] = Tile.ROCK
        game_map.map[1][1] = Tile.ROCK
        game_map.map[1][2] = Tile.BOMB
        game_map.map[2][0] = Tile.BOMB
        game_map.map[2][1] = Tile.BOMB
        game_map.map[2][2] = Tile.BOMB

        target_map = Map(3, 3)
        target_map.map[0][0] = Tile.EMPTY
        target_map.map[0][1] = Tile.EMPTY
        target_map.map[0][2] = Tile.BOMB
        target_map.map[1][0] = Tile.EMPTY
        target_map.map[1][1] = Tile.EMPTY
        target_map.map[1][2] = Tile.BOMB
        target_map.map[2][0] = Tile.BOMB
        target_map.map[2][1] = Tile.BOMB
        target_map.map[2][2] = Tile.BOMB

        canvas = Canvas(Test3.tk, width=game_map.width, height=game_map.height)

        to_be_triggered = [
            (0, 0),
        ]

        def trigger_bomb_callback(col, row):
            self.assertIn((col, row), to_be_triggered)
            to_be_triggered.remove((col, row))

        game_map.trigger_bomb(canvas, 0, 0, trigger_bomb_callback)

        self.assertTrue((target_map.map == game_map.map).all())
        self.assertListEqual([], to_be_triggered)

    def test_trigger_bomb__long_chain(self):
        game_map = Map(9, 1)
        game_map.map[0][0] = Tile.BOMB
        game_map.map[0][1] = Tile.BOMB
        game_map.map[0][2] = Tile.BOMB
        game_map.map[0][3] = Tile.BOMB
        game_map.map[0][4] = Tile.BOMB
        game_map.map[0][5] = Tile.BOMB
        game_map.map[0][6] = Tile.BOMB
        game_map.map[0][7] = Tile.BOMB
        game_map.map[0][8] = Tile.BOMB

        canvas = Canvas(Test3.tk, width=game_map.width, height=game_map.height)

        to_be_triggered = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (8, 0),
        ]

        def trigger_bomb_callback(col, row):
            self.assertIn((col, row), to_be_triggered)
            to_be_triggered.remove((col, row))

        game_map.trigger_bomb(canvas, 0, 0, trigger_bomb_callback)

        self.assertTrue((Map(9, 1).map == game_map.map).all())
        self.assertListEqual([], to_be_triggered)


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test3."
    tests = list(filter(lambda _: _.startswith("test"), Test3.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test3)
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
