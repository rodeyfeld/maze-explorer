import arcade


class Player(arcade.Sprite):

    def __init__(self, asset, scaling, x, y):
        super().__init__(asset, scaling)
        self.center_x = x
        self.center_y = y
