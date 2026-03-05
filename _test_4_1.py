import io
import os.path
import unittest

from game import Game
from tank import Tank


def decorator__two_message(before=None, after=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                Test41.addLog(before)
            result = func(*args, **kwargs)
            if after:
                Test41.addLog(after)
            return result

        return wrapper

    return decorator


def decorator__log_param(before=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if before:
                Test41.addLog(before, end="")
            Test41.addLog(args)
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


class Test41(unittest.TestCase):
    tank0: Tank
    tank1: Tank

    @classmethod
    def setUpClass(cls):
        cls.game = Game(
            "maps/test.txt"
        )  # Must use this map, otherwise the tests are not strong enough

    def setUp(self):
        Test41.log = ""
        Test41.game.scoreboard.score_tank_1 = 0
        Test41.game.scoreboard.score_tank_2 = 0

    @classmethod
    def tearDownClass(cls):
        cls.game.window.destroy()

    @classmethod
    def addLog(cls, message, end="\n"):
        cls.log += f"{message}{end}"

    @classmethod
    def setTank(cls):
        for tank in cls.game.tanks:
            if tank.tank_id == 0:
                cls.tank0 = tank
            elif tank.tank_id == 1:
                cls.tank1 = tank

    def test_destroy__increase_score(self):
        Test41.game.destroy_tank(0)
        self.assertEqual(self.game.scoreboard.score_tank_1, 0)
        self.assertEqual(self.game.scoreboard.score_tank_2, 1)
        Test41.game.destroy_tank(0)
        self.assertEqual(self.game.scoreboard.score_tank_1, 0)
        self.assertEqual(self.game.scoreboard.score_tank_2, 2)
        Test41.game.destroy_tank(1)
        self.assertEqual(self.game.scoreboard.score_tank_1, 1)
        self.assertEqual(self.game.scoreboard.score_tank_2, 2)

    def test_destroy__update_score(self):

        def add_scores_to_log(*args, **kwargs):
            Test41.addLog(
                f"update_score() called with score_a={Test41.game.scoreboard.score_tank_1} score_b={Test41.game.scoreboard.score_tank_2}"
            )

        Test41.game.scoreboard.update_score, o_us = (
            decorator__two_functions(add_scores_to_log)(
                Test41.game.scoreboard.update_score
            ),
            Test41.game.scoreboard.update_score,
        )

        Test41.game.destroy_tank(0)
        Test41.game.destroy_tank(0)
        Test41.game.destroy_tank(0)
        Test41.game.destroy_tank(1)
        Test41.game.destroy_tank(1)
        Test41.game.destroy_tank(1)

        target_log = "update_score() called with score_a=0 score_b=1\nupdate_score() called with score_a=0 score_b=2\nupdate_score() called with score_a=0 score_b=3\nupdate_score() called with score_a=1 score_b=3\nupdate_score() called with score_a=2 score_b=3\nupdate_score() called with score_a=3 score_b=3\n"
        self.assertEqual(Test41.log, target_log)

        Test41.game.scoreboard.update_score = o_us

    def test_destroy__kill_tank_and_reset_game(self):
        Test41.setTank()

        Test41.game.reset_game, org = (
            lambda: Test41.addLog("reset_game()"),
            Test41.game.reset_game,
        )
        Test41.tank0.kill, ok0 = (
            decorator__two_message("tank0.kill()")(Test41.tank0.kill),
            Test41.tank0.kill,
        )
        Test41.tank1.kill, ok1 = (
            decorator__two_message("tank1.kill()")(Test41.tank1.kill),
            Test41.tank1.kill,
        )

        Test41.game.destroy_tank(0)
        Test41.game.destroy_tank(1)
        Test41.game.destroy_tank(1)

        target_log = "tank0.kill()\nreset_game()\ntank1.kill()\nreset_game()\ntank1.kill()\nreset_game()\n"

        self.assertEqual(Test41.log, target_log)

        Test41.tank0.kill = ok0
        Test41.tank1.kill = ok1
        Test41.game.reset_game = org


def main(interactive=True):
    file_name = os.path.basename(__file__)
    name = f"{file_name[:-2]}Test41."
    tests = list(filter(lambda _: _.startswith("test"), Test41.__dict__.keys()))
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
        suite = unittest.TestLoader().loadTestsFromTestCase(Test41)
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
