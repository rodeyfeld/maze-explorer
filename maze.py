import random
import arcade
from tile import Tile
from wall import Wall

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

WALL_OPTIONS = {
    'N': {
        'asset': "./assets/horizontal_wall.png",
        'y_offset': 12.5,
        'x_offset': 0
    },
    'E': {
        'asset': "./assets/vertical_wall.png",
        'y_offset': 0,
        'x_offset': 12.5
    },
    'S': {
        'asset': "./assets/horizontal_wall.png",
        'y_offset': -12.5,
        'x_offset': 0
    },
    'W': {
        'asset': "./assets/vertical_wall.png",
        'y_offset': 0,
        'x_offset': -12.5
    }
}


class Maze(arcade.Window):

    def __init__(self, len_y, len_x, init_y=0, init_x=0):
        super().__init__(len_y * 25, len_x * 25, "Maze")
        self.map = []
        self.len_y = len_y
        self.len_x = len_x
        self.init_y = init_y
        self.init_x = init_x
        self.tile_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        arcade.set_background_color(arcade.color.GREEN)

    def __str__(self):
        maze_rows = ['-' * self.len_y * 2]
        for y in range(self.len_y):
            maze_row = ['|']
            for x in range(self.len_x):
                if self.map[y][x].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.len_x):
                if self.map[y][x].walls['S']:
                    maze_row.append('00')
                else:
                    maze_row.append(' 0')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def setup(self):
        self.create_blank_map()
        self.create_maze()
        self.get_walls()

    def on_draw(self):
        arcade.start_render()
        self.tile_list.draw()
        self.wall_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.tile_list.update()
        self.wall_list.update()

    def has_unvisited_tiles(self):
        for y in range(0, self.len_y):
            for x in range(0, self.len_x):
                if not self.map[y][x].visited:
                    return True
        return False

    def get_tile_neighbors(self, tile):
        tile_neighbors = []
        x = tile.x
        y = tile.y
        if x-1 >= 0:
            if not self.map[y][x-1].visited:
                tile_neighbors.append({'tile': self.map[y][x-1], 'direction': 'W'})
        if y-1 >= 0:
            if not self.map[y-1][x].visited:
                tile_neighbors.append({'tile': self.map[y-1][x], 'direction': 'N'})
        if x+1 < self.len_x:
            if not self.map[y][x+1].visited:
                tile_neighbors.append({'tile': self.map[y][x+1], 'direction': 'E'})
        if y+1 < self.len_y:
            if not self.map[y+1][x].visited:
                tile_neighbors.append({'tile': self.map[y+1][x], 'direction': 'S'})
        return tile_neighbors

    def create_blank_map(self):
        for y in range(0, self.len_y):
            self.map.append([])
            for x in range(0, self.len_x):
                tile = Tile("./assets/tile.png", 1, x, y, self.len_x-1, self.len_y-1)
                self.map[y].append(tile)
                self.tile_list.append(tile)

    def get_walls(self):
        for row in self.map:
            for tile in row:
                print(tile.walls)
                for key, value in tile.walls.items():
                    if value:
                        wall = Wall(WALL_OPTIONS[key]['asset'], 1, tile.center_x + WALL_OPTIONS[key]['x_offset'],
                                    tile.center_y + WALL_OPTIONS[key]['y_offset'])
                        print(key, tile.x, tile.y)
                        print(key,  tile.center_x, tile.center_y, wall.center_x, wall.center_y)
                        self.wall_list.append(wall)

    def create_maze(self):
        tile_stack = []
        curr_tile = self.map[self.init_y][self.init_x]
        curr_tile.visited = True
        while self.has_unvisited_tiles():
            tile_neighbors = self.get_tile_neighbors(curr_tile)
            if tile_neighbors:
                tile_stack.append(curr_tile)
                rand_tile = tile_neighbors[random.randint(0, len(tile_neighbors)-1)]
                curr_tile.destroy_wall(rand_tile['direction'], rand_tile['tile'])
                curr_tile = rand_tile['tile']
                curr_tile.visited = True
            elif tile_stack:
                curr_tile = tile_stack.pop()