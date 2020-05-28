from maze import Maze
import arcade

LEN_X = 10
LEN_Y = 10


def main():
    maze = Maze(LEN_X, LEN_Y)
    maze.setup()
    print(maze)
    arcade.run()


main()
