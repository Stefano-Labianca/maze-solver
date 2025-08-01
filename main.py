from graphics import Window
from maze import Maze


ROWS = 15
COLUMNS = 20
CELL_SIZE_X = 30
CELL_SIZE_Y = 30
MAZE_X = 10
MAZE_Y = 10

def main():
    win = Window(800, 600)
    maze = Maze(MAZE_X, MAZE_Y,ROWS, COLUMNS, CELL_SIZE_X, CELL_SIZE_Y , win)

    win.wait_for_close()

if __name__ == "__main__":
    main()
