from maze import Maze
import arcade

LEN_X = 5
LEN_Y = 5


def main():
    maze = Maze(LEN_X, LEN_Y)
    maze.setup()
    arcade.run()


main()
