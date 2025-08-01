from graphics import  Maze, Window


ROWS = 10
COLUMNS = 10
CELL_SIZE_X = 20
CELL_SIZE_Y = 20
MAZE_X = 4
MAZE_Y = 4

def main():
    win = Window(800, 600)
    maze = Maze(MAZE_X, MAZE_Y,ROWS, COLUMNS, CELL_SIZE_X, CELL_SIZE_Y , win)
    
    win.wait_for_close()

if __name__ == "__main__":
    main()
