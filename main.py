from graphics import  Line, Point, Window


def main():
    win = Window(800, 600)

    line1 = Line(Point(10, 10), Point(500, 100))
    line2 = Line(Point(400, 400), Point(100, 100))
    
    win.draw_line(line1, 'red')
    win.draw_line(line2)
    
    win.wait_for_close()

if __name__ == "__main__":
    main()
