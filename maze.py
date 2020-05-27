import random
import arcade
from tile import Tile


class Maze(object):

    def __init__(self, len_y, len_x, init_y=0, init_x =0):
        self.map = []
        self.len_y = len_y
        self.len_x = len_x
        self.init_y = init_y
        self.init_x = init_x
        self.tile_list = arcade.sprite_list

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
                tile = Tile(y, x)
                self.map[y].append(tile)

    def create_maze(self):
        tile_stack = []
        curr_tile = self.map[self.init_y][self.init_x]
        curr_tile.visited = True
        while self.has_unvisited_tiles():
            tile_neighbors = self.get_tile_neighbors(curr_tile)
            if tile_neighbors:
                print(curr_tile)
                tile_stack.append(curr_tile)
                rand_tile = tile_neighbors[random.randint(0, len(tile_neighbors)-1)]
                curr_tile.destroy_wall(rand_tile['direction'], rand_tile['tile'])
                curr_tile = rand_tile['tile']
                curr_tile.visited = True
            elif tile_stack:
                curr_tile = tile_stack.pop()
