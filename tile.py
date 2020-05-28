import arcade

TILE_SIZE = 100


class Tile(arcade.Sprite):

    # Opposite directions for each direction
    mirror_directions = {
        'N': 'S',
        'E': 'W',
        'S': 'N',
        'W': 'E',
    }

    def __init__(self, asset, scaling, x, y, maze_length):
        super().__init__(asset, scaling)
        # TODO: Replace booleans with objects
        self.walls = {
            'N': True,
            'E': True,
            'S': True,
            'W': True,
        }
        self.x = x
        self.y = y
        self.visited = False
        self.center_x = x * TILE_SIZE + TILE_SIZE / 2
        self.center_y = (maze_length - y) * TILE_SIZE + (TILE_SIZE / 2)

    def destroy_wall(self, wall, mirror_tile):
        self.walls[wall] = False
        # Remove current wall and the wall mirrored by it
        mirror_tile.walls[Tile.mirror_directions[wall]] = False

