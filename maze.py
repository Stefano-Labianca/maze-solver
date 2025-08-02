from graphics import Line, LineColorType, Point, Window
import time
import random

SeedType = int | float | str | bytes | bytearray | None

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
            self.visited = False

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
        seed: SeedType = None, animation_speed: float = 0.05
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
        self.animation_speed = animation_speed

        self.__cells: list[list[Cell]] = []
        self.__create_cells()
        self.__break_entrance_and_exit()

        random.seed(seed)
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def solve(self):
        return self.__solve_r()

    def get_cells(self) -> list[list[Cell]]: return self.__cells

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        
        exit_col = self.__num_cols - 1
        exit_row = self.__num_rows - 1

        self.__cells[exit_col][exit_row].has_bottom_wall = False
        self.__draw_cell(exit_col, exit_row)


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
        time.sleep(self.animation_speed)

    # Use random walk
    def __break_walls_r(self, i: int, j: int):
        self.__cells[i][j].visited = True

        while True:
            to_visit: list[tuple[int, int]] = []

            if i + 1 < self.__num_cols and (not self.__cells[i + 1][j].visited): # right
                to_visit.append((i + 1, j)) 
            
            if i - 1 >= 0 and (not self.__cells[i - 1][j].visited): # left
                to_visit.append((i - 1, j))
            
            if j + 1 < self.__num_rows and (not self.__cells[i][j + 1].visited): # bottom
                to_visit.append((i, j + 1))

            if j - 1 >= 0 and (not self.__cells[i][j - 1].visited): # top
                to_visit.append((i, j - 1))

            if len(to_visit) == 0:
                self.__draw_cell(i, j)
                return
            else:
                random_choice = random.choice(to_visit)

                if i + 1 == random_choice[0]:
                    self.__cells[i][j].has_right_wall = False
                    self.__cells[random_choice[0]][random_choice[1]].has_left_wall = False
                if i - 1 == random_choice[0]:
                    self.__cells[i][j].has_left_wall = False
                    self.__cells[random_choice[0]][random_choice[1]].has_right_wall = False
                if j + 1 == random_choice[1]:
                    self.__cells[i][j].has_bottom_wall = False
                    self.__cells[random_choice[0]][random_choice[1]].has_top_wall = False
                if j - 1 == random_choice[1]:
                    self.__cells[i][j].has_top_wall = False
                    self.__cells[random_choice[0]][random_choice[1]].has_bottom_wall = False
                
                self.__break_walls_r(random_choice[0], random_choice[1])
                
    def __reset_cells_visited(self):
        for col_idx in range(self.__num_cols):
            for row_idx in range(self.__num_rows):
                self.__cells[col_idx][row_idx].visited = False

    def __solve_r(self, i: int = 0, j: int = 0):
        self.__animate()
        current_cell = self.__cells[i][j]
        current_cell.visited = True

        exit_col = self.__num_cols - 1
        exit_row = self.__num_rows - 1

        if i == exit_col and j == exit_row:
            return True
        
        if i + 1 < self.__num_cols: # right
            right_cell = self.__cells[i + 1][j]
            is_free_path = (not current_cell.has_right_wall) and (not right_cell.has_left_wall)
            
            if is_free_path and (not right_cell.visited):
                current_cell.draw_move(right_cell)

                if self.__solve_r(i + 1, j):
                    return True

                current_cell.draw_move(right_cell, True)

        
        if i - 1 >= 0: # left
            left_cell = self.__cells[i - 1][j]
            is_free_path = (not current_cell.has_left_wall) and (not left_cell.has_right_wall)

            if is_free_path and (not left_cell.visited):
                current_cell.draw_move(left_cell)

                if self.__solve_r(i - 1, j):
                    return True

                current_cell.draw_move(left_cell, True)

        
        if j + 1 < self.__num_rows: # bottom
            bottom_cell = self.__cells[i][j + 1]
            is_free_path = (not current_cell.has_bottom_wall) and (not bottom_cell.has_top_wall)

            if is_free_path and (not bottom_cell.visited):
                current_cell.draw_move(bottom_cell)

                if self.__solve_r(i, j + 1):
                    return True

                current_cell.draw_move(bottom_cell, True)


        if j - 1 >= 0: # top
            top_cell = self.__cells[i][j - 1]
            is_free_path = (not current_cell.has_top_wall) and (not top_cell.has_bottom_wall)

            if is_free_path and (not top_cell.visited):
                current_cell.draw_move(top_cell)

                if self.__solve_r(i, j - 1):
                    return True

                current_cell.draw_move(top_cell, True)


        return False
