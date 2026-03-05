import colorsys
import re

import numpy as np
from PIL import Image


def natural_key(text):
    return [int(c) if c.isdigit() else c for c in re.split(r"(\d+)", text)]


rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)


def shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv(r, g, b)
    h = hout
    r, g, b = hsv_to_rgb(h, s, v)
    arr = np.dstack((r, g, b, a))
    return arr


def colorize(image, hue):
    """
    Colorize PIL image `original` with the given
    `hue` (hue within 0-360); returns another PIL image.
    """
    img = image.convert("RGBA")
    arr = np.array(np.asarray(img).astype("float"))
    new_img = Image.fromarray(shift_hue(arr, hue / 360.0).astype("uint8"), "RGBA")

    return new_img


"""
A user-defined type for a rectangle. 

A rectangle is defined by a tuple of four floats (x1, y1, x2, y2) where (x1, y1) is the top-left corner and (x2, y2) is 
the bottom-right corner.
"""
Rect = tuple[float, float, float, float]


def overlap(ra: Rect, rb: Rect):
    """
    Check if two rectangles, A and B, overlap with each other.

    See type Rect for the definition of a rectangle.

    :param ra: the rectangle A
    :param rb: the rectangle B
    :return: True if the two rectangles overlap with each other, False otherwise
    """

    ax1, ay1, ax2, ay2 = ra
    bx1, by1, bx2, by2 = rb

    return ax1 <= bx2 and ax2 >= bx1 and ay1 <= by2 and ay2 >= by1
