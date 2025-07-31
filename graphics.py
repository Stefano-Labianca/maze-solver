from tkinter import Tk, BOTH, Canvas
from typing import Literal

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.__p1 = p1
        self.__p2 = p2
    
    def draw(self, canvas: Canvas, fill_color: str):
        if fill_color != "red" and fill_color != "black":
            raise ValueError("fill_color should be red or black")
        
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

    def draw_line(self, line: Line, fill_color: Literal["red", "black"] = "black"):
        line.draw(self.__canvas, fill_color)


class Cell: 
    def __init__(self, window: Window):
            self.has_left_wall: bool = True
            self.has_right_wall: bool = True
            self.has_top_wall: bool = True
            self.has_bottom_wall: bool = True

            self.__x1: float = -1
            self.__y1: float = -1
            self.__x2: float = -1
            self.__y2: float = -1

            self.__win = window

    def draw(self, x1: float, y1: float, x2: float, y2: float):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        p1 = Point(self.__x1, self.__y1)
        p2 = Point(self.__x2, self.__y2)
        
        if self.has_left_wall:
            left_line = Line(p1, Point(p1.x, p2.y))
            self.__win.draw_line(left_line, 'black')

        if self.has_top_wall:
            top_line = Line(p1, Point(p2.x, p1.y))
            self.__win.draw_line(top_line, 'black')

        if self.has_right_wall:
            right_line = Line(Point(p2.x, p1.y), p2)
            self.__win.draw_line(right_line, 'black')

        if self.has_bottom_wall:
            bottom_line = Line(Point(p1.x, p2.y), p2)
            self.__win.draw_line(bottom_line, 'black')
    