import arcade


class Wall(arcade.Sprite):

    def __init__(self, asset, scaling, center_x, center_y):
        super().__init__(asset, scaling)
        self.center_y = center_y
        self.center_x = center_x
