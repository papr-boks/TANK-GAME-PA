from pathlib import Path

import numpy as np

import assets
from explosion import Explosion
from game import Game
from projectile import Projectile
from sprite import Sprite, Direction
from utils import colorize

ASSETS_PATH = Path("assets")
TANK_IMAGES = assets.load_frames("tank")
TANK_FRAMES = [
    {
        None: TANK_IMAGES,
        Direction.N: [image.rotate(0) for image in TANK_IMAGES],
        Direction.S: [image.rotate(180) for image in TANK_IMAGES],
        Direction.W: [image.rotate(90) for image in TANK_IMAGES],
        Direction.E: [image.rotate(270) for image in TANK_IMAGES],
    },
    {
        None: [colorize(image, 0) for image in TANK_IMAGES],
        Direction.N: [colorize(image, 0).rotate(0) for image in TANK_IMAGES],
        Direction.S: [colorize(image, 0).rotate(180) for image in TANK_IMAGES],
        Direction.W: [colorize(image, 0).rotate(90) for image in TANK_IMAGES],
        Direction.E: [colorize(image, 0).rotate(270) for image in TANK_IMAGES],
    },
]

TANK_WIDTH = 0.5
TANK_HEIGHT = 0.5


class Tank(Sprite):
    """A tank controlled by a player (or AI) on the game map.

    A Tank is a :class:`Sprite` with simple directional movement logic.

    Inputs
    ------
    game: Game
        The game instance the tank belongs to. Used to access the map and
        canvas for launching sprites and projectiles.
    x, y: float
        Initial position of the tank (centre coordinates in map units).
    tank_id: int
        Index selecting the tank's sprite frames and used as a key into
        the game's position map.
    """

    def __init__(self, game: Game, x: float, y: float, tank_id: int) -> None:
        super().__init__(x, y, TANK_FRAMES[tank_id], fps=24)
        self.tank_id: int = tank_id

        self.game: Game = game
        # Current facing key (Direction)
        self.key: Direction = Direction.N

        # The stack for storing the directions. If empty the tank is idle.
        # The top of the stack represents the current moving direction.
        self.direction_stack: list[Direction] = []

    def launch_tank(self, direction: Direction) -> None:
        """Start moving the tank in ``direction``.

        If the tank is already moving in the requested direction this is a
        no-op. Otherwise the direction is pushed to the internal stack and
        the sprite velocity is updated.
        """
        if direction in self.direction_stack:
            # If the tank is already moving in the same direction, do nothing
            return
        else:
            # Push the new direction to the stack
            self.direction_stack.append(direction)
            # Otherwise, pause the current movement
            for d in Direction:
                self.cancel(self.game.canvas, key=d)

        # Launch the tank in the new direction
        velocity_x, velocity_y = np.array(direction.value) * 15
        super().launch(self.game.canvas, (velocity_x, velocity_y), key=direction)

    def stop_tank(self, direction: Direction) -> None:
        """Stop movement in ``direction``.

        If the tank is currently moving in ``direction`` the movement is
        cancelled and the stack is popped. If there are remaining directions
        on the stack the tank will resume the last one.
        """
        if self.moving_direction == direction:
            # If the tank is moving in the same direction, cancel the movement
            self.direction_stack.pop()
            super().cancel(self.game.canvas, key=direction)
            # Resume the movement in the last direction
            if len(self.direction_stack) > 0:
                # Use the stack directly so the type is known to be Direction
                last_direction = self.direction_stack[-1]
                velocity_x, velocity_y = np.array(last_direction.value) * 15
                super().launch(
                    self.game.canvas, (velocity_x, velocity_y), key=last_direction
                )
        else:
            # Otherwise, remove the direction from the stack
            if direction in self.direction_stack:
                self.direction_stack.remove(direction)

    def on_new_position(self, new_x: float, new_y: float) -> tuple[float, float]:
        """Adjust a proposed new position to avoid collisions.

        The game map provides collision helpers. This method returns the
        final acceptable (x, y) for the tank.
        """
        if self.game.map.collides(new_x, new_y, TANK_WIDTH, TANK_HEIGHT) == {}:
            pass
        elif self.game.map.collides(self.x, self.y, TANK_WIDTH, TANK_HEIGHT) != {}:
            pass
        else:
            new_x, new_y = self.game.map.nearest_position(
                self.x, self.y, new_x, new_y, TANK_WIDTH, TANK_HEIGHT
            )
        self.game.map.tank_position_map[self.tank_id] = (new_x, new_y)
        return new_x, new_y

    def fire(self) -> None:
        """Fire a projectile in the current facing direction.

        Spawns both a :class:`Projectile` and a small visual :class:`Explosion`.
        """
        projectile_x, projectile_y = np.array((self.x, self.y)) + (
            np.array(self.direction.value) * 0.75
        )
        projectile = Projectile(
            self.game, projectile_x, projectile_y, self.direction, self.tank_id
        )
        explosion = Explosion(projectile_x, projectile_y, scale=0.5)

        projectile.launch_projectile(self.game.canvas)
        explosion.launch_explosion(self.game.canvas)

    @property
    def direction(self) -> Direction:
        """Return the current facing direction (Direction)."""
        return self.key

    @property
    def moving_direction(self) -> Direction | None:
        """Return the current moving direction from the stack or ``None``.
        """
        return self.direction_stack[-1] if self.direction_stack else None

    def kill(self) -> None:
        """Kill the tank and launch a large explosion visual."""
        for d in Direction:
            self.cancel(self.game.canvas, key=d)
        explosion = Explosion(self.x, self.y, scale=2)
        explosion.launch_explosion(self.game.canvas)
