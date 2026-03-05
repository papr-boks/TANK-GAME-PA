from tkinter import Canvas

import numpy as np

import assets
from explosion import Explosion
from game import Game
from map import Tile
from sprite import Sprite, Direction

PROJECTILE_IMAGES = assets.load_frames("projectile")


class Projectile(Sprite):

    def __init__(
        self, game: Game, x: float, y: float, direction: Direction, tank_id: int
    ):
        super().__init__(x, y, PROJECTILE_IMAGES)
        self.game = game
        self.direction = direction
        self.tank_id = tank_id

        self.collision_tiles: dict[tuple[int, int], Tile] | None = {}
        self.collision_tank_id: int | None = None

    def launch_projectile(self, canvas):
        vx, vy = np.array(self.direction.value) * 30
        self.launch(canvas, (vx, vy))

    def on_life_over(
        self, canvas: Canvas, new_x: float, new_y: float, new_frame_num: float
    ):
        # if the projectile is destroyed by a tank
        if (
            self.collision_tank_id is not None
            and self.collision_tank_id != self.tank_id
        ):
            self.game.destroy_tank(self.collision_tank_id)

        # if the projectile is destroyed by a bomb
        elif self.collision_tiles and Tile.BOMB in self.collision_tiles.values():
            for (col, row), tile in self.collision_tiles.items():
                if tile == Tile.BOMB:
                    self.game.map.trigger_bomb(
                        canvas,
                        col,
                        row,
                        # (col, row) -> (x, y), therefore +0.5as
                        lambda c, r: Explosion(
                            c + 0.5, r + 0.5, scale=2
                        ).launch_explosion(canvas),
                    )
        # otherwise
        else:
            explosion = Explosion(new_x, new_y)
            explosion.launch_explosion(canvas)

    def is_life_over(self, new_x: float, new_y: float, new_frame_num: float):
        self.collision_tiles = self.game.map.collides(new_x, new_y)
        self.collision_tank_id = self.game.map.collides_with_tank(new_x, new_y)

        # The projectile is destroyed if it collides with a tank (other than itself) or some tiles.
        return self.collision_tiles != {} or (
            self.collision_tank_id is not None
            and self.collision_tank_id != self.tank_id
        )
