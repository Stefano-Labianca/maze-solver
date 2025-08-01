from tkinter import Tk, BOTH, Canvas
from typing import Literal

LineColorType = Literal["red", "black", "gray", "white"]

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.__p1 = p1
        self.__p2 = p2
    
    def draw(self, canvas: Canvas, fill_color: str):
        if fill_color != "red" and fill_color != "black" and fill_color != "gray" and fill_color != "white":
            raise ValueError("fill_color should be red, black, gray or white")
        
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

