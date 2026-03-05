import io
import os.path
import unittest
from tkinter import Tk

from map import Map


class Test22(unittest.TestCase):
    tk: Tk

    @classmethod
    def setUpClass(cls):
        cls.tk = Tk()

    @classmethod
    def tearDownClass(cls):
        cls.tk.destroy()

    def test_collides_with_tank__point(self):
        game_map = Map(3, 3)
        game_map.tank_position_map[0] = (1.5, 1.5)

        self.assertEqual(None, game_map.collides_with_tank(0.5, 0.5))
        self.assertEqual(None, game_map.collides_with_tank(1.5, 0.5))
        self.assertEqual(None, game_map.collides_with_tank(2.5, 0.5))
        self.assertEqual(None, game_map.collides_with_tank(0.5, 1.5))
        self.assertEqual(0, game_map.collides_with_tank(1.5, 1.5))
        self.assertEqual(None, game_map.collides_with_tank(2.5, 1.5))
        self.assertEqual(None, game_map.collides_with_tank(0.5, 2.5))
        self.assertEqual(None, game_map.collides_with_tank(1.5, 2.5))
        self.assertEqual(None, game_map.collides_with_tank(2.5, 2.5))

    def test_collides_with_tank__rect(self):
        game_map = Map(3, 3)
        game_map.tank_position_map[0] = (1.5, 1.5)

        self.assertEqual(None, game_map.collides_with_tank(0.5, 0.5, 0.5, 0.5))
        self.assertEqual(None, game_map.collides_with_tank(1.5, 0.5, 0.5, 0.5))
        self.assertEqual(None, game_map.collides_with_tank(2.5, 0.5, 0.5, 0.5))
        self.assertEqual(None, game_map.collides_with_tank(0.5, 1.5, 0.5, 0.5))
        self.assertEqual(0, game_map.collides_with_tank(1.5, 1.5, 0.5, 0.5))
        self.assertEqual(None, game_map.collides_with_tank(2.5, 1.5, 0.5, 0.5))
        self.assertEqual(None, game_map.collides_with_tank(0.5, 2.5, 0.5, 0.5))
        self.assertEqual(None, game_map.collides_with_tank(1.5, 2.5, 0.5, 0.5))
        self.assertEqual(None, game_map.collides_with_tank(2.5, 2.5, 0.5, 0.5))

    def test_collides_with_tank__partial(self):
        game_map = Map(3, 3)
        game_map.tank_position_map[0] = (1.5, 1.5)

        self.assertEqual(0, game_map.collides_with_tank(0.75, 0.75, 1, 1))
        self.assertEqual(0, game_map.collides_with_tank(1.5, 0.75, 0.75, 0.75))
        self.assertEqual(0, game_map.collides_with_tank(2.25, 0.75, 1, 1))
        self.assertEqual(0, game_map.collides_with_tank(0.75, 1.5, 0.75, 0.75))
        self.assertEqual(0, game_map.collides_with_tank(2.25, 1.5, 0.75, 0.75))
        self.assertEqual(0, game_map.collides_with_tank(0.75, 2.25, 1, 1))
        self.assertEqual(0, game_map.collides_with_tank(1.5, 2.25, 0.75, 0.75))
        self.assertEqual(0, game_map.collides_with_tank(2.25, 2.25, 1, 1))

    def test_collides_with_tank__inclusive(self):
        game_map = Map(3, 3)
        game_map.tank_position_map[0] = (1.5, 1.5)

        self.assertEqual(0, game_map.collides_with_tank(0.75, 0.75, 0.5, 0.5))
        self.assertEqual(0, game_map.collides_with_tank(1.75, 0.75, 0.5, 0.5))
        self.assertEqual(0, game_map.collides_with_tank(2.25, 0.75, 0.5, 0.5))
        self.assertEqual(0, game_map.collides_with_tank(0.75, 1.50, 0.5, 0.5))
        self.assertEqual(0, game_map.collides_with_tank(1.50, 1.50, 0.5, 0.5))
        self.assertEqual(0, game_map.collides_with_tank(2.25, 1.50, 0.5, 0.5))
        self.assertEqual(0, game_map.collides_with_tank(0.75, 2.25, 0.5, 0.5))
        self.assertEqual(0, game_map.collides_with_tank(1.75, 2.25, 0.5, 0.5))
        self.assertEqual(0, game_map.collides_with_tank(2.25, 2.25, 0.5, 0.5))


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test22."
    tests = list(filter(lambda _: _.startswith("test"), Test22.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test22)
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
