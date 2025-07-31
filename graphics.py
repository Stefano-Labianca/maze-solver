from tkinter import Tk, BOTH, Canvas
from typing import Literal
from time import sleep

LineColorType = Literal["red", "black", "gray"]

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.__p1 = p1
        self.__p2 = p2
    
    def draw(self, canvas: Canvas, fill_color: str):
        if fill_color != "red" and fill_color != "black" and fill_color != "gray":
            raise ValueError("fill_color should be red, black, or gray")
        
        canvas.create_line(self.__p1.x, self.__p1.y, self.__p2.x,self.__p2.y, fill=fill_color, width=2)


class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        
        self.__is_window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_window_running = True

        while self.__is_window_running:
            self.redraw()

        print("window closed...")

    def close(self):
        self.__is_window_running = False

    def draw_line(self, line: Line, fill_color: LineColorType = "black"):
        line.draw(self.__canvas, fill_color)


class Cell: 
    def __init__(self, window: Window):
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
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        p1 = Point(self.__x1, self.__y1)
        p2 = Point(self.__x2, self.__y2)
        
        if self.has_left_wall:
            left_line = Line(p1, Point(p1.x, p2.y))
            self.__win.draw_line(left_line)

        if self.has_top_wall:
            top_line = Line(p1, Point(p2.x, p1.y))
            self.__win.draw_line(top_line)

        if self.has_right_wall:
            right_line = Line(Point(p2.x, p1.y), p2)
            self.__win.draw_line(right_line)

        if self.has_bottom_wall:
            bottom_line = Line(Point(p1.x, p2.y), p2)
            self.__win.draw_line(bottom_line)

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
        
        path = Line(current_cell_center, to_cell_center)
        self.__win.draw_line(path, line_color)

    def __calculate_half_length(self):
        return abs(self.__x1 - self.__x2)
    

class Maze:
    def __init__(self, x1: int, y1: int, num_rows: int, num_cols: int,
        cell_size_x: int, cell_size_y: int, win: Window,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win

        self.__cells: list[list[Cell]] = []
        self.__create_cells()

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
        self.__win.redraw()
        sleep(0.01)