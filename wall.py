import arcade


class Wall(arcade.Sprite):

    def __init__(self, asset, scaling, center_x, center_y, direction):
        super().__init__(asset, scaling)
        self.direction = direction
        self.center_y = center_y
        self.center_x = center_x
