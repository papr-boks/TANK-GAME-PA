from PIL.Image import Image
from typing import List

import assets
from sprite import Sprite

EXPLOSION_IMAGES: List[Image] = assets.load_frames("explosion")


class Explosion(Sprite):
    def __init__(self, x, y, scale: float = 1.0) -> None:
        """Create an Explosion sprite.

        Parameters
        ----------
        game
            Game instance the explosion belongs to (used by Sprite constructor).
        x, y : float
            Position for the explosion.
        scale : float, optional
            Scaling factor applied to the source frames. Allows creating
            smaller or larger explosion visuals.
        """
        if scale != 1.0:
            frames = [
                image.resize(
                    (int(round(image.width * scale)), int(round(image.height * scale)))
                )
                for image in EXPLOSION_IMAGES
            ]
        else:
            frames = EXPLOSION_IMAGES
        super().__init__(x, y, frames, fps=50)

    def launch_explosion(self, canvas) -> None:
        """Launch the explosion animation (no motion)."""
        self.launch(canvas, (0, 0))

    def is_life_over(self, new_x, new_y, new_frame_num) -> bool:
        return self.frame_num > new_frame_num
