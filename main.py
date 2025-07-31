from graphics import  Cell, Maze, Window


ROWS = 20
COLUMNS = 30
CELL_SIZE_X = 20
CELL_SIZE_Y = 20

def main():
    win = Window(800, 600)
    maze = Maze(4, 4,
        ROWS, COLUMNS, CELL_SIZE_X, CELL_SIZE_Y , win
    )
    


    win.wait_for_close()

if __name__ == "__main__":
    main()
