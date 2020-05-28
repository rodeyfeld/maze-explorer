import arcade


class Tile(arcade.Sprite):

    mirror_directions = {
        'N': 'S',
        'E': 'W',
        'S': 'N',
        'W': 'E',
    }

    def __init__(self, asset, scaling, x, y, maze_width, maze_length):
        super().__init__(asset, scaling)
        self.walls = {
            'N': True,
            'E': True,
            'S': True,
            'W': True,
        }
        self.x = x
        self.y = y
        self.visited = False
        self.center_x = x * 25 + 12.5
        self.center_y = (maze_length - y) * 25 + 12.5

    def destroy_wall(self, wall, mirror_tile):
        self.walls[wall] = False
        mirror_tile.walls[Tile.mirror_directions[wall]] = False

