from game import Game


def main():
    # A few maps to choose from:
    # game = Game("./maps/default.txt")
    # game = Game("./maps/demo.txt")
    game = Game("maps/small.txt")
    game.mainloop()


if __name__ == "__main__":
    main()
