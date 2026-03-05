from tkinter import Tk, Canvas
from map import create_map


def read_from_file(file_path: str) -> str:
    """
    Reads the content from a file.
    :param file_path: The path to the file
    :return: The content of the file as a string
    """
    with open(file_path, "r") as f:
        file_content = f.read()
    return file_content


class Game:
    """
    The class representing the Tank War Game.
    """
    def __init__(self, map_file: str):
        # The Tkinter window setup.
        # This is the object representing the game window shown on the computer screen.
        self.window: Tk = Tk()
        self.window.title("Tank War Game")
        self.window.geometry(f"+0+0")

        # Create the game map.
        # This is the logical object representing the game map.
        # We will perform all the game calculation on this map.
        self.map_file = map_file
        self.map = create_map(read_from_file(map_file))

        # Create the scoreboard.
        # This handles the score rendering and displaying.
        from scoreboard import Scoreboard
        self.scoreboard = Scoreboard(self)

        # The Tkinter canvas setup.
        # This is the object representing the game canvas shown on the game window.
        # We are going to draw everything on this canvas.
        self.canvas = Canvas(
            self.window, width=self.map.width, height=self.map.height)
        self.canvas.pack(expand=True, fill="both")

        # Create the tanks.
        # These are the logical objects representing the tanks in the game.
        from tank import Tank
        self.tanks = [
            Tank(self, x, y, i) for i, (x, y) in self.map.tank_position_map.items()
        ]

        # Draw the map on the canvas.
        self.map.draw_on(self.canvas)
        # Draw the tanks on the canvas.
        for tank in self.tanks:
            tank.draw_on(self.canvas)

        # Bind the keys to control the tanks.
        self.bind_keys()
    def destroy_tank(self, tank_id: int):
        """
        Destroys the tank with the given tank_id because it was hit by a projectile.

        This function does the following:

        1. Increments the score of the opponent tank. If the tank_id is 0, the score of tank 2 (self.scoreboard.score_tank_2) is incremented by 1. If the tank_id is 1, the score of tank 1 (self.scoreboard.score_tank_1) is incremented by 1.
        2. Updates the score displayed on the scoreboard. (Hint: there is a function called update_score in a certain file. You need to call this function in a proper way to update the score.)
        3. Kills the tank with the given tank_id by calling the `kill` method of the tank.
        4. Resets the game by calling the `reset_game` method.

        You can assume that the tank_id is always valid.
        """

        # TODO 4.1
        if tank_id == 0:
            # 坦克0被摧毁，坦克2得分
            self.scoreboard.score_tank_2 += 1
        elif tank_id == 1:
            # 坦克1被摧毁，坦克1得分
            self.scoreboard.score_tank_1 += 1
        
        # 更新分数显示
        self.scoreboard.update_score()
        
        # 杀死坦克
        self.tanks[tank_id].kill()
        
        # 重置游戏
        self.reset_game()
        # TODO 4.1 END

    def reset_game(self):
        """
        Resets the game by reinitializing the map and tanks.

        The function does the following:

        1. Unbinds all the keys to prevent any further input.
        2. Stops all the tanks by calling the `stop_tank` method for each tank for each direction.
        3. Re-initializes the map by reading the map from the file again.
        4. Re-initializes the tanks by creating new tanks at the positions specified in the map.
        5. Re-binds the keys again.
        6. Draws the map and the tanks on the canvas.

        You may refer to the constructor for the initialization of the map and the tanks, binding of the keys,
        and drawing of the map and the tanks.
        """
        from tank import Tank
        from sprite import Direction

        # TODO 4.2
        self.unbind_keys()
    
        for tank in self.tanks:
            for direction in Direction:
                tank.stop_tank(direction)
    

        self.map = create_map(read_from_file(self.map_file))
    

        self.tanks = [
            Tank(self, x, y, i) for i, (x, y) in self.map.tank_position_map.items()
        ]
    

        self.bind_keys()
    

        self.canvas.delete("all")
    

        self.map.draw_on(self.canvas)
    

        for tank in self.tanks:
            tank.draw_on(self.canvas)



    def bind_keys(self):
        """
        Binds the keys for tank 1 and tank 2.
        """

        from sprite import Direction

        # Bind Keys for Tank 1
        self.window.bind(
            "<KeyPress-w>", lambda _: self.tanks[0].launch_tank(Direction.N)
        )
        self.window.bind(
            "<KeyPress-s>", lambda _: self.tanks[0].launch_tank(Direction.S)
        )
        self.window.bind(
            "<KeyPress-a>", lambda _: self.tanks[0].launch_tank(Direction.W)
        )
        self.window.bind(
            "<KeyPress-d>", lambda _: self.tanks[0].launch_tank(Direction.E)
        )
        self.window.bind(
            "<KeyRelease-w>", lambda _: self.tanks[0].stop_tank(Direction.N)
        )
        self.window.bind(
            "<KeyRelease-s>", lambda _: self.tanks[0].stop_tank(Direction.S)
        )
        self.window.bind(
            "<KeyRelease-a>", lambda _: self.tanks[0].stop_tank(Direction.W)
        )
        self.window.bind(
            "<KeyRelease-d>", lambda _: self.tanks[0].stop_tank(Direction.E)
        )
        self.window.bind("<KeyPress-f>", lambda _: self.tanks[0].fire())

        # Bind Keys for Tank 2
        self.window.bind(
            "<KeyPress-Up>", lambda _: self.tanks[1].launch_tank(Direction.N)
        )
        self.window.bind(
            "<KeyPress-Down>", lambda _: self.tanks[1].launch_tank(Direction.S)
        )
        self.window.bind(
            "<KeyPress-Left>", lambda _: self.tanks[1].launch_tank(Direction.W)
        )
        self.window.bind(
            "<KeyPress-Right>", lambda _: self.tanks[1].launch_tank(
                Direction.E)
        )
        self.window.bind(
            "<KeyRelease-Up>", lambda _: self.tanks[1].stop_tank(Direction.N)
        )
        self.window.bind(
            "<KeyRelease-Down>", lambda _: self.tanks[1].stop_tank(Direction.S)
        )
        self.window.bind(
            "<KeyRelease-Left>", lambda _: self.tanks[1].stop_tank(Direction.W)
        )
        self.window.bind(
            "<KeyRelease-Right>", lambda _: self.tanks[1].stop_tank(
                Direction.E)
        )
        self.window.bind("<KeyPress-space>", lambda _: self.tanks[1].fire())

    def unbind_keys(self):
        """
        Unbinds the keys for tank 1 and tank 2.
        """

        self.window.unbind("<KeyPress-w>")
        self.window.unbind("<KeyPress-s>")
        self.window.unbind("<KeyPress-a>")
        self.window.unbind("<KeyPress-d>")
        self.window.unbind("<KeyRelease-w>")
        self.window.unbind("<KeyRelease-s>")
        self.window.unbind("<KeyRelease-a>")
        self.window.unbind("<KeyRelease-d>")
        self.window.unbind("<KeyPress-f>")
        self.window.unbind("<KeyPress-Up>")
        self.window.unbind("<KeyPress-Down>")
        self.window.unbind("<KeyPress-Left>")
        self.window.unbind("<KeyPress-Right>")
        self.window.unbind("<KeyRelease-Up>")
        self.window.unbind("<KeyRelease-Down>")
        self.window.unbind("<KeyRelease-Left>")
        self.window.unbind("<KeyRelease-Right>")
        self.window.unbind("<KeyPress-space>")

    def mainloop(self):
        """
        Runs the main loop of the game window. 
        """
        self.window.mainloop()
