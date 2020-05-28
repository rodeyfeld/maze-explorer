import arcade


class Wall(arcade.Sprite):

    def __init__(self, asset, scaling, center_y, center_x):
        super().__init__(asset, scaling)
        self.center_y = center_y
        self.center_x = center_x
