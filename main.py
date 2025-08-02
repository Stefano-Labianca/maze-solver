from graphics import Window
from maze import Maze
from math import floor
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROWS = 15
COLUMNS = 20
MAZE_MARGIN_X = 10
MAZE_MARGIN_Y = 10

ANIMATION_SPEED = 0.01
SEED = 0

RECURSION_LIMIT = 10000

def main():
    sys.setrecursionlimit(10000)
    win = Window(SCREEN_WIDTH, SCREEN_HEIGHT)

    cell_size_x = floor((SCREEN_WIDTH - 2 * MAZE_MARGIN_X) / COLUMNS)
    cell_size_y = floor((SCREEN_HEIGHT - 2 * MAZE_MARGIN_Y) / ROWS)

    maze = Maze(MAZE_MARGIN_X, MAZE_MARGIN_Y, ROWS, COLUMNS, cell_size_x, cell_size_y , win, SEED, ANIMATION_SPEED)
    
    print(f"Solved? {maze.solve()}")


    win.wait_for_close()

if __name__ == "__main__":
    main()
