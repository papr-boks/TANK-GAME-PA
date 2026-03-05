import io
import os.path
import unittest

from map import Map
from game import Game
from tank import Direction, Tank


def decorator__two_message(before=None, after=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                Test42.addLog(before)
            result = func(*args, **kwargs)
            if after:
                Test42.addLog(after)
            return result

        return wrapper

    return decorator


def decorator__log_param(before=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                Test42.addLog(before, end="")
            Test42.addLog(args)
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def decorator__two_functions(before=None, after=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                before(*args, **kwargs)
            result = func(*args, **kwargs)
            if after:
                after(*args, **kwargs)
            return result

        return wrapper

    return decorator


class Test42(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = Game("maps/small.txt")

    def setUp(self):
        Test42.log = ""

    @classmethod
    def tearDownClass(cls):
        cls.game.window.destroy()

    @classmethod
    def addLog(cls, message, end="\n"):
        cls.log += f"{message}{end}"

    def test_reset__1_stop_tank(self):
        tank0_stopped = {}
        tank1_stopped = {}

        def stop_tank0(d):
            tank0_stopped[d] = True

        def stop_tank1(d):
            tank1_stopped[d] = True

        for tank in Test42.game.tanks:
            if tank.tank_id == 0:
                tank.stop_tank = decorator__two_functions(
                    stop_tank0)(tank.stop_tank)
            if tank.tank_id == 1:
                tank.stop_tank = decorator__two_functions(
                    stop_tank1)(tank.stop_tank)

        Test42.game.reset_game()

        self.assertEqual(
            tank0_stopped,
            {
                Direction.E: True,
                Direction.S: True,
                Direction.W: True,
                Direction.N: True,
            },
        )
        self.assertEqual(
            tank1_stopped,
            {
                Direction.E: True,
                Direction.S: True,
                Direction.W: True,
                Direction.N: True,
            },
        )

    def test_reset__2_unbind_readmap_bind(self):
        Test42.game.bind_keys, or_bk = (
            decorator__two_message("GameTest.game.bind_keys()")(
                Test42.game.bind_keys
            ),
            Test42.game.bind_keys,
        )
        Test42.game.unbind_keys, or_uk = (
            decorator__two_message("GameTest.game.unbind_keys()")(
                Test42.game.unbind_keys
            ),
            Test42.game.unbind_keys,
        )

        Test42.game.reset_game()

        self.assertEqual(
            Test42.log,
            "GameTest.game.unbind_keys()\nGameTest.game.bind_keys()\n",
        )

        Test42.game.bind_keys = or_bk
        Test42.game.unbind_keys = or_uk

    def test_reset__3_new_tanks(self):
        Test42.game.map_file = "maps/test.txt"
        Test42.game.reset_game()

        self.assertEqual(len(Test42.game.tanks), 2)

        for tank_id in range(2):
            for i in range(3):
                if i == 2:
                    self.fail("Missing a tank")
                if Test42.game.tanks[i].tank_id == tank_id:
                    tank: Tank = Test42.game.tanks[i]
                    if tank_id == 0:
                        self.assertEqual(tank.x, 0.5)
                        self.assertEqual(tank.y, 1.5)
                    else:
                        self.assertEqual(tank.x, 1.5)
                        self.assertEqual(tank.y, 0.5)
                    break

        Test42.game.map_file = "maps/small.txt"

    def test_reset__4_draw_map(self):
        Map.draw_on, or_do = (
            decorator__two_message("Map.draw_on()")(Map.draw_on),
            Map.draw_on,
        )

        Test42.game.reset_game()

        self.assertEqual(
            Test42.log,
            "Map.draw_on()\n",
        )

        Map.draw_on = or_do

    def test_reset__5_draw_tanks(self):
        Tank.draw_on, or_do = (
            decorator__two_message("Tank.draw_on()")(Tank.draw_on),
            Tank.draw_on,
        )

        Test42.game.reset_game()

        self.assertEqual(
            Test42.log,
            "Tank.draw_on()\nTank.draw_on()\n",
        )

        Tank.draw_on = or_do


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test42."
    tests = list(filter(lambda _: _.startswith("test"), Test42.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test42)
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
