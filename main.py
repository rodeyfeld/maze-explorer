from maze import Maze

LEN_X = 5
LEN_Y = 5


def main():
    maze = Maze(LEN_X, LEN_Y)
    maze.create_blank_map()
    maze.create_maze()
    print(maze)

main()