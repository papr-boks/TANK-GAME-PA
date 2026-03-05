import io
import os.path
import unittest
from tkinter import Tk

from map import Map, Tile


class Test21(unittest.TestCase):
    tk: Tk

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()

    def test_collides__point(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.ROCK

        self.assertEqual({}, game_map.collides(0.5, 0.5))
        self.assertEqual({}, game_map.collides(1.5, 0.5))
        self.assertEqual({}, game_map.collides(2.5, 0.5))
        self.assertEqual({}, game_map.collides(0.5, 1.5))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(1.5, 1.5))
        self.assertEqual({}, game_map.collides(2.5, 1.5))
        self.assertEqual({}, game_map.collides(0.5, 2.5))
        self.assertEqual({}, game_map.collides(1.5, 2.5))
        self.assertEqual({}, game_map.collides(2.5, 2.5))

    def test_collides__rect(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.ROCK

        self.assertEqual({}, game_map.collides(0.5, 0.5, 0.5, 0.5))
        self.assertEqual({}, game_map.collides(1.5, 0.5, 0.5, 0.5))
        self.assertEqual({}, game_map.collides(2.5, 0.5, 0.5, 0.5))
        self.assertEqual({}, game_map.collides(0.5, 1.5, 0.5, 0.5))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(1.5, 1.5, 0.5, 0.5))
        self.assertEqual({}, game_map.collides(2.5, 1.5, 0.5, 0.5))
        self.assertEqual({}, game_map.collides(0.5, 2.5, 0.5, 0.5))
        self.assertEqual({}, game_map.collides(1.5, 2.5, 0.5, 0.5))
        self.assertEqual({}, game_map.collides(2.5, 2.5, 0.5, 0.5))

    def test_collides__partial(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.ROCK

        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(0.75, 0.75, 1, 1))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(1.5, 0.75, 0.75, 0.75))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(2.25, 0.75, 1, 1))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(0.75, 1.5, 0.75, 0.75))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(2.25, 1.5, 0.75, 0.75))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(0.75, 2.25, 1, 1))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(1.5, 2.25, 0.75, 0.75))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(2.25, 2.25, 1, 1))

    def test_collides__surrounding(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.ROCK

        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(1.5, 1.5, 2, 2))

    def test_collides__inclusive(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.ROCK

        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(0.75, 0.75, 0.5, 0.5))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(1.75, 0.75, 0.5, 0.5))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(2.25, 0.75, 0.5, 0.5))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(0.75, 1.50, 0.5, 0.5))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(1.50, 1.50, 0.5, 0.5))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(2.25, 1.50, 0.5, 0.5))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(0.75, 2.25, 0.5, 0.5))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(1.75, 2.25, 0.5, 0.5))
        self.assertEqual({(1, 1): Tile.ROCK}, game_map.collides(2.25, 2.25, 0.5, 0.5))

    def test_collides__boundary(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.ROCK

        self.assertEqual(None, game_map.collides(0, 0, 0.5, 0.5))
        self.assertEqual(None, game_map.collides(1.5, 0, 0.5, 0.5))
        self.assertEqual(None, game_map.collides(3, 0, 0.5, 0.5))
        self.assertEqual(None, game_map.collides(0, 1.5, 0.5, 0.5))
        self.assertEqual(None, game_map.collides(3, 1.5, 0.5, 0.5))
        self.assertEqual(None, game_map.collides(0, 3, 0.5, 0.5))
        self.assertEqual(None, game_map.collides(1.5, 3, 0.5, 0.5))
        self.assertEqual(None, game_map.collides(3, 3, 0.5, 0.5))

    def test_collides__with_bomb(self):
        game_map = Map(3, 3)
        game_map.map[1][1] = Tile.BOMB

        self.assertEqual({(1, 1): Tile.BOMB}, game_map.collides(1.5, 1.5))

    def test_collides__multiple_tiles(self):
        game_map = Map(2, 2)
        game_map.map[0][0] = Tile.ROCK
        game_map.map[0][1] = Tile.ROCK
        game_map.map[1][0] = Tile.ROCK
        game_map.map[1][1] = Tile.ROCK

        self.assertEqual(
            {(0, 0): Tile.ROCK, (1, 0): Tile.ROCK},
            game_map.collides(1, 0.5, 0.25, 0.25),
        )
        self.assertEqual(
            {(0, 0): Tile.ROCK, (0, 1): Tile.ROCK},
            game_map.collides(0.5, 1, 0.25, 0.25),
        )
        self.assertEqual(
            {
                (0, 0): Tile.ROCK,
                (0, 1): Tile.ROCK,
                (1, 0): Tile.ROCK,
                (1, 1): Tile.ROCK,
            },
            game_map.collides(1, 1, 0.25, 0.25),
        )

    def test_collides__precedence(self):
        game_map = Map(1, 1)
        game_map.map[0][0] = Tile.ROCK

        self.assertEqual(None, game_map.collides(0, 0, 0.25, 0.25))


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test21."
    tests = list(filter(lambda _: _.startswith("test"), Test21.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test21)
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
