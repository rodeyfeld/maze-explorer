import random
import arcade

from player import Player
from tile import Tile, TILE_SIZE
from wall import Wall

SCALING = 1
MOVEMENT_SPEED = 1
WALL_OPTIONS = {
    'N': {
        'asset': "./assets/horizontal_wall.png",
        'y_offset': TILE_SIZE / 2 - 1,
        'x_offset': 0
    },
    'E': {
        'asset': "./assets/vertical_wall.png",
        'y_offset': 0,
        'x_offset': TILE_SIZE / 2 - 1,
    },
    'S': {
        'asset': "./assets/horizontal_wall.png",
        'y_offset': -TILE_SIZE / 2 + 1,
        'x_offset': 0
    },
    'W': {
        'asset': "./assets/vertical_wall.png",
        'y_offset': 0,
        'x_offset': -TILE_SIZE / 2 + 1
    }
}


class Maze(arcade.Window):

    def __init__(self, len_y, len_x, init_y=0, init_x=0):
        super().__init__(len_y * TILE_SIZE, len_x * TILE_SIZE, "Maze")
        self.map = []
        self.len_y = len_y
        self.len_x = len_x
        self.init_y = init_y
        self.init_x = init_x
        self.tile_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player = None
        self.player_list = arcade.SpriteList()
        self.collisions = []
        arcade.set_background_color(arcade.color.GREEN)

    def setup(self):
        self.create_blank_map()
        self.create_maze()
        self.create_player()
        self.get_walls()

    def on_draw(self):
        arcade.start_render()
        self.tile_list.draw()
        self.player_list.draw()
        self.wall_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.tile_list.update()
        self.player_list.update()
        self.wall_list.update()
        self.collisions = self.player.collides_with_list(self.wall_list)
        print(self.collisions)
        if self.collisions:
            for wall in self.collisions:
                if wall.direction == 'N':
                    self.player.center_y -= MOVEMENT_SPEED
                    self.player.change_y = 0
                if wall.direction == 'E':
                    self.player.center_x -= MOVEMENT_SPEED
                    self.player.change_x = 0
                if wall.direction == 'S':
                    self.player.center_y += MOVEMENT_SPEED
                    self.player.change_y = 0
                if wall.direction == 'W':
                    self.player.center_x += MOVEMENT_SPEED
                    self.player.change_x = 0

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

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
        if y - 1 >= 0:
            if not self.map[y - 1][x].visited:
                tile_neighbors.append({'tile': self.map[y - 1][x], 'direction': 'N'})
        if x + 1 < self.len_x:
            if not self.map[y][x + 1].visited:
                tile_neighbors.append({'tile': self.map[y][x + 1], 'direction': 'E'})
        if y + 1 < self.len_y:
            if not self.map[y + 1][x].visited:
                tile_neighbors.append({'tile': self.map[y + 1][x], 'direction': 'S'})
        if x - 1 >= 0:
            if not self.map[y][x - 1].visited:
                tile_neighbors.append({'tile': self.map[y][x - 1], 'direction': 'W'})
        return tile_neighbors

    def create_player(self):
        start_tile = self.map[0][0]
        player = Player("./assets/player.png", SCALING - .50, start_tile.center_x, start_tile.center_y)
        self.player = player
        self.player_list.append(player)

    def create_blank_map(self):
        for y in range(0, self.len_y):
            self.map.append([])
            for x in range(0, self.len_x):
                if y == 0 and x == 0:
                    asset = "./assets/start.png"
                elif y == self.len_x - 1 and x == self.len_x - 1:
                    asset = "./assets/end.png"
                else:
                    asset = "./assets/tile.png"
                tile = Tile(asset, SCALING, x, y, self.len_x - 1)
                self.map[y].append(tile)
                self.tile_list.append(tile)

    def get_walls(self):
        for row in self.map:
            for tile in row:
                print(tile.walls)
                for key, value in tile.walls.items():
                    if value:
                        wall = Wall(
                            asset=WALL_OPTIONS[key]['asset'],
                            scaling=SCALING,
                            center_x=tile.center_x + WALL_OPTIONS[key]['x_offset'],
                            center_y=tile.center_y + WALL_OPTIONS[key]['y_offset'],
                            direction=key
                        )
                        self.wall_list.append(wall)

    def create_maze(self):
        tile_stack = []
        curr_tile = self.map[self.init_y][self.init_x]
        curr_tile.visited = True
        while self.has_unvisited_tiles():
            tile_neighbors = self.get_tile_neighbors(curr_tile)
            if tile_neighbors:
                tile_stack.append(curr_tile)
                rand_tile = tile_neighbors[random.randint(0, len(tile_neighbors) - 1)]
                curr_tile.destroy_wall(rand_tile['direction'], rand_tile['tile'])
                curr_tile = rand_tile['tile']
                curr_tile.visited = True
            elif tile_stack:
                curr_tile = tile_stack.pop()
