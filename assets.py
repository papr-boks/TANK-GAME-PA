from glob import glob
from pathlib import Path

import tkinter as tk
from PIL import Image, ImageTk

from utils import natural_key

ASSETS_PATH = Path("assets")


def get_scale():
    root = tk.Tk()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_height / 1080


RESIZE_SCALE = get_scale()


def open_and_resize_image(
    image_path: str | Path, scale: float = RESIZE_SCALE
) -> Image.Image:
    original_image = Image.open(image_path)

    new_size = (int(original_image.width * scale), int(original_image.height * scale))
    resized_image = original_image.resize(new_size)

    return resized_image


def open_and_resize_photoimage(
    image_path: str | Path, scale: float = RESIZE_SCALE
) -> ImageTk.PhotoImage:
    return ImageTk.PhotoImage(open_and_resize_image(image_path, scale))


def load_frames(asset_name: str) -> list[Image.Image]:
    image_paths = glob(str(ASSETS_PATH / f"{asset_name}*.png"))
    image_paths.sort(key=natural_key)
    images = [open_and_resize_image(path) for path in image_paths]
    for image in images:
        image.load()
    return images
