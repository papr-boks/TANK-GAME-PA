from tkinter import Canvas

from PIL import Image, ImageOps, ImageTk

from assets import ASSETS_PATH
from game import Game

SCOREBOARD_IMAGE = Image.open(ASSETS_PATH / "scoreboard.png")
DIGIT_IMAGES = [
    Image.open(ASSETS_PATH / "digits.png").crop((i * 10, 0, (i + 1) * 10, 16))
    for i in range(10)
]


class Scoreboard:
    def __init__(self, game: Game):
        self.score_tank_1 = 0
        self.score_tank_2 = 0

        self.scoreboard_image = ImageOps.contain(
            SCOREBOARD_IMAGE,
            (int(game.map.width), int(game.map.height)),
            method=Image.Resampling.NEAREST,
        )
        self.scoreboard_photo_image = ImageTk.PhotoImage(self.scoreboard_image)

        self.scale = self.scoreboard_image.width / SCOREBOARD_IMAGE.width

        self.digit_images = [
            digit_image.resize(
                (
                    int(digit_image.width * self.scale),
                    int(digit_image.height * self.scale),
                ),
                Image.Resampling.NEAREST,
            )
            for digit_image in DIGIT_IMAGES
        ]
        self.digit_photo_images = [
            ImageTk.PhotoImage(digit_image) for digit_image in self.digit_images
        ]

        self.canvas = Canvas(
            game.window,
            width=self.scoreboard_image.width,
            height=self.scoreboard_image.height,
        )
        self.canvas.pack(expand=True, fill="both")

        self.update_score()

    def update_score(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.scoreboard_photo_image, anchor="nw")

        for i, digit in enumerate(str(self.score_tank_1)):
            digit = int(digit)
            pos_x = (129 + i * 10) * self.scale
            pos_y = (42) * self.scale
            self.canvas.create_image(
                pos_x, pos_y, image=self.digit_photo_images[digit], anchor="nw"
            )

        for i, digit in enumerate(str(self.score_tank_2)):
            digit = int(digit)
            pos_x = (307 + i * 10) * self.scale
            pos_y = (42) * self.scale
            self.canvas.create_image(
                pos_x, pos_y, image=self.digit_photo_images[digit], anchor="nw"
            )
