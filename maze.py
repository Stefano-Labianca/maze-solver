from graphics import Line, LineColorType, Point, Window
import time

class Cell: 
    def __init__(self, window: Window | None = None):
            self.has_left_wall: bool = True
            self.has_right_wall: bool = True
            self.has_top_wall: bool = True
            self.has_bottom_wall: bool = True

            self.__x1: int = -1
            self.__y1: int = -1
            self.__x2: int = -1
            self.__y2: int = -1

            self.__win = window

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        if not self.__win:
            return

        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        p1 = Point(self.__x1, self.__y1)
        p2 = Point(self.__x2, self.__y2)

        left_line = Line(p1, Point(p1.x, p2.y))
        top_line = Line(p1, Point(p2.x, p1.y))
        right_line = Line(Point(p2.x, p1.y), p2)
        bottom_line = Line(Point(p1.x, p2.y), p2)

        if self.has_left_wall:
            self.__win.draw_line(left_line)
        else:
            self.__win.draw_line(left_line, "white")

        if self.has_top_wall:
            self.__win.draw_line(top_line)
        else:
            self.__win.draw_line(top_line, "white")

        if self.has_right_wall:
            self.__win.draw_line(right_line)
        else:
            self.__win.draw_line(right_line, "white")

        if self.has_bottom_wall:
            self.__win.draw_line(bottom_line)
        else:
            self.__win.draw_line(bottom_line, "white")

    def get_x1(self): return self.__x1

    def get_x2(self): return self.__x2
    
    def get_y1(self): return self.__y1
    
    def get_y2(self): return self.__y2

    def draw_move(self, to_cell, undo: bool = False):
        if not isinstance(to_cell, Cell): 
            raise ValueError("Not a Cell instance")
        
        current_half_len = self.__calculate_half_length() // 2
        to_cell_half_len = to_cell.__calculate_half_length() // 2
        
        current_cell_center = Point(
            self.__x1 + current_half_len, 
            self.__y1 + current_half_len
        )

        to_cell_center = Point(
            to_cell.get_x1() + to_cell_half_len, 
            to_cell.get_y1() + to_cell_half_len
        )

        line_color: LineColorType = "gray"

        if undo:
            line_color = "red"
        
        if not self.__win: 
            return
        
        path = Line(current_cell_center, to_cell_center)
        self.__win.draw_line(path, line_color)

    def __calculate_half_length(self):
        return abs(self.__x1 - self.__x2)
    

class Maze:
    def __init__(self, x1: int, y1: int, num_rows: int, num_cols: int,
        cell_size_x: int, cell_size_y: int, win: Window | None = None,
    ):
        
        if num_cols <= 0:
            raise ValueError(f"Invalid amount of columns: {num_cols}")
        
        if num_rows <= 0:
            raise ValueError(f"Invalid amount of rows: {num_rows}")
        
        if cell_size_x <= 0 or cell_size_y <= 0:
            raise ValueError(f"Invalid cell size. x={cell_size_x}, y={cell_size_y}")

        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win

        self.__cells: list[list[Cell]] = []
        self.__create_cells()
        self.__break_entrance_and_exit()

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        
        exit_col = self.__num_cols - 1
        exit_row = self.__num_rows - 1

        self.__cells[exit_col][exit_row].has_bottom_wall = False
        self.__draw_cell(exit_col, exit_row)

    def get_cells(self) -> list[list[Cell]]: return self.__cells

    def __create_cells(self):
        for _ in range(self.__num_cols):
            row = [ Cell(self.__win) for _ in range(self.__num_rows) ]
            self.__cells.append(row)

        for col_idx in range(self.__num_cols):
            for row_idx in range(self.__num_rows):
                self.__draw_cell(col_idx, row_idx)    


    def __draw_cell(self, col: int, row: int):
        cell_obj = self.__cells[col][row]
        
        p1 = Point(
            self.__x1 + col * self.__cell_size_x, 
            self.__y1 + row * self.__cell_size_y, 
        )
        
        p2 = Point(
            p1.x + self.__cell_size_x, 
            p1.y + self.__cell_size_y, 
        )

        cell_obj.draw(p1.x, p1.y, p2.x, p2.y)
        self.__animate()
    
    def __animate(self):
        if not self.__win:
            return

        self.__win.redraw()
        time.sleep(0.01)