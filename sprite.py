import time
from enum import Enum
from math import sqrt
from tkinter import Canvas
from typing import Any

import PIL.Image
import numpy as np
from PIL.ImageTk import PhotoImage

from map import TILE_SIZE


class Sprite:
    """Represent a drawable, animated object on a Tkinter Canvas.

    The Sprite class is intentionally small and designed to be subclassed for
    game-specific behaviour. It maintains position in tile units (floating
    point), converts PIL Images to Tkinter PhotoImage objects for rendering,
    and manages an animation loop that both advances frames (at `fps`) and
    updates position/rendering at `rps` using the canvas `after` method.

    Attributes
    ----------
    x, y : float
        Current position in tile coordinates. Sub-pixel (sub-tile) positions
        are supported for smooth motion.
    frames : dict[Any, list[PhotoImage]]
        Mapping from a rendering `key` to a list of PhotoImage frames. If the
        user passed a list to the constructor, it is stored under the `None`
        key.
    frame_num : float
        Current (possibly fractional) animation frame index. The integer
        part is used to select the shown frame, while the fractional part
        allows smooth frame progression when `fps` and `rps` differ.
    fps : float
        Target frames-per-second for animation playback (affects frame_num
        advancement).
    rps : float
        Renderings-per-second (how often the update loop runs). Movement is
        computed per rendering step as velocity / rps.
    canvas_id : int | None
        Tkinter canvas object id for the currently drawn image (or None).
    update_id : dict[Any, str | None]
        Mapping from keys to the `after` callback id used to schedule the
        next `update` call. Used by `launch`/`cancel` to control animation
        loops.
    key : Any
        The last `key` passed to `draw_on`/`update` (useful for subclasses).

    Hooks for subclasses
    ---------------------
    - on_new_position(new_x, new_y) -> (x, y): return corrected/validated
      coordinates (for collision resolution).
    - is_life_over(new_x, new_y, new_frame_num) -> bool: return True when
      the sprite should be removed (e.g. moved off-screen or exploded).
    - on_life_over(canvas, new_x, new_y, new_frame_num): called once when
      the sprite's life ends to allow custom effects.
    """

    def __init__(
        self,
        x: float,
        y: float,
        frames: list[PIL.Image.Image] | dict[Any, list[PIL.Image.Image]],
        fps: float = 10,
        rps: float = 60,
    ):
        self.x: float = x
        self.y: float = y
        
        if isinstance(frames, list):
            self.frames = {
                None: [PhotoImage(image) for image in frames]
            }
        else:
            self.frames = {
                key: [PhotoImage(image) for image in images]
                for key, images in frames.items()
            }
        
        self.frame_num: float = 0.0

        self.fps: float = fps
        self.rps: float = rps

        self.canvas_id = None
        self.update_id: dict[Any, str | None] = {}

        self.key = None

    def draw_on(self, canvas: Canvas, key: Any = None):
        """Draw the sprite's current frame on `canvas`.

        Parameters
        ----------
        canvas : tkinter.Canvas
            Canvas to draw the sprite onto.
        key : Any, optional
            Rendering key selecting which frame sequence to use (default is
            `None` which corresponds to the single-frame/list constructor
            form).

        Behaviour
        ---------
        - Deletes the previous canvas image (if any).
        - Creates a new image centered at `(x * TILE_SIZE, y * TILE_SIZE)`.
        - Uses `int(self.frame_num)` to index into the selected frames list.
        """

        if self.canvas_id is not None:
            canvas.delete(self.canvas_id)

        frames = self.frames[key]
        self.canvas_id = canvas.create_image(
            ((self.x) * TILE_SIZE, (self.y) * TILE_SIZE),
            image=frames[int(self.frame_num)],
            anchor="center",
        )

    def update(self, canvas: Canvas, velocity: tuple[float, float], key: Any = None):
        """Advance animation, move the sprite, and schedule the next update.

        This method performs the following steps atomically:
        1. Draw the current frame (via :meth:`draw_on`).
        2. Compute the candidate new position by adding `velocity / rps`.
        3. Advance the `frame_num` by `fps / rps` (wraps modulo the number
           of frames in the selected frame list).
        4. Call :meth:`is_life_over` with the candidate values; if True, the
           sprite is removed and :meth:`on_life_over` is invoked.
        5. Otherwise call :meth:`on_new_position` to allow subclasses to
           adjust the position (collision resolution), then commit the
           position and frame number.
        6. Schedule the next update call via `canvas.after`, storing the after-id in
           `self.update_id[key]`.

        Parameters
        ----------
        canvas : tkinter.Canvas
            Canvas used to draw and schedule updates.
        velocity : tuple[float, float]
            Movement vector expressed in tiles-per-second (x, y). The actual
            per-step delta is `velocity / rps`.
        key : Any, optional
            Rendering key selecting which frame sequence to use.
        """
        
        begin = time.time()
        self.draw_on(canvas, key=key)
        self.key = key
        new_x = self.x + velocity[0] / self.rps
        new_y = self.y + velocity[1] / self.rps
        frames = self.frames[key]
        new_frame_num = (self.frame_num + float(self.fps) / float(self.rps)) % len(frames)

        over = self.is_life_over(new_x, new_y, new_frame_num)
        if over and self.canvas_id is not None:
            canvas.delete(self.canvas_id)
            self.on_life_over(canvas, new_x, new_y, new_frame_num)
            return
        new_x, new_y = self.on_new_position(new_x, new_y)
        self.x = new_x
        self.y = new_y
        self.frame_num = new_frame_num
        duration = (time.time() - begin) * 1000
        self.update_id[key] = canvas.after(
            int(1000 / self.rps - duration), self.update, canvas, velocity, key
        )

    def launch(self, canvas: Canvas, velocity: tuple[float, float], key: Any = None):
        """Start (or resume) the sprite update loop for a given `key`.

        If an update loop is already scheduled for the provided key this
        method does nothing. Otherwise it immediately calls :meth:`update`
        which will draw and schedule future updates.

        Parameters
        ----------
        canvas : tkinter.Canvas
            Canvas used for rendering and scheduling.
        velocity : tuple[float, float]
            Movement vector in tiles-per-second.
        key : Any, optional
            Rendering key used to separate multiple concurrent animation
            loops (default: empty string).
        """
        # If the sprite is already moving, do nothing
        if key in self.update_id and self.update_id[key] is not None:
            return

        # Launch the sprite
        self.update(canvas, velocity, key=key)

    def cancel(self, canvas: Canvas, key: Any = ""):
        """Cancel a scheduled update loop for `key` if present.

        This will call `canvas.after_cancel` on the stored id and set
        `self.update_id[key]` to None so the sprite can be relaunched later.

        Parameters
        ----------
        canvas : tkinter.Canvas
            Canvas used to cancel the scheduled callback.
        key : Any, optional
            Key for the scheduled update to cancel.
        """
        if key in self.update_id:
            update_id = self.update_id[key]
            if update_id is not None:
                canvas.after_cancel(update_id)
                canvas.update()
                self.update_id[key] = None

    def on_new_position(self, new_x: float, new_y: float) -> tuple[float, float]:
        """Hook called before committing a new position.

        Subclasses can override this to perform collision detection or clamp
        coordinates. The default implementation returns the coordinates
        unchanged.

        Parameters
        ----------
        new_x, new_y : float
            Candidate coordinates in tile units.

        Returns
        -------
        (float, float)
            The coordinates that should actually be assigned to `self.x` and
            `self.y`.
        """
        return new_x, new_y

    def is_life_over(self, new_x: float, new_y: float, new_frame_num: float) -> bool:
        """Decide whether the sprite's life is over at the candidate state.

        The default implementation always returns False. Subclasses typically
        override this to detect conditions such as leaving the map bounds,
        colliding with solid tiles, or reaching an 'exploded' state.

        Parameters
        ----------
        new_x, new_y : float
            Candidate coordinates in tile units.
        new_frame_num : float
            The candidate (possibly fractional) frame index after advancement.

        Returns
        -------
        bool
            True if the sprite should be removed; False otherwise.
        """
        return False

    def on_life_over(
        self, canvas: Canvas, new_x: float, new_y: float, new_frame_num: float
    ):
        """Called once when `is_life_over` returns True.

        Override to perform cleanup or spawn effects (for example, create an
        Explosion sprite). This method is called with the candidate position
        and frame number that triggered life termination. The default does
        nothing.

        Parameters
        ----------
        canvas : tkinter.Canvas
            Canvas used to create any final effects.
        new_x, new_y : float
            Candidate coordinates that triggered termination.
        new_frame_num : float
            The frame index at termination.
        """
        pass


class Direction(Enum):
    N = (0, -1)
    S = (0, +1)
    W = (-1, 0)
    E = (+1, 0)

    @staticmethod
    def sum(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
        """Return the (normalized) vector sum of two direction vectors.

        The enum values are unit axis vectors (e.g. (0, -1) for north). When
        adding orthogonal directions (e.g. N + E) the result is normalized by
        dividing by sqrt(2) so the magnitude remains 1. This helper is useful
        to combine directional inputs while keeping consistent speed.

        Parameters
        ----------
        a, b : tuple[float, float]
            2D direction vectors to add.

        Returns
        -------
        tuple[float, float]
            Normalized result of a + b.
        """
        return tuple((np.array(a) + np.array(b)) / sqrt(2))
