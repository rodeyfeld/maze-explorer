import arcade


class Tile(arcade.Sprite):

    mirror_directions = {
        'N': 'S',
        'E': 'W',
        'S': 'N',
        'W': 'E',
    }

    def __init__(self, y, x):
        super().__init__()
        self.walls = {
            'N': True,
            'E': True,
            'S': True,
            'W': True,
        }
        self.y = y
        self.x = x
        self.visited = False

    def destroy_wall(self, wall, mirror_tile):
        self.walls[wall] = False
        mirror_tile.walls[Tile.mirror_directions[wall]] = False

