from graphics import  Cell, Window


def main():
    win = Window(800, 600)

    c1 = Cell(win)
    c2 = Cell(win)
    c3 = Cell(win)

    c1.draw(100, 200, 150, 250)
    c2.draw(150, 200, 200, 250)
    c3.draw(400, 500, 450, 550)

    c1.draw_move(c2)
    c2.draw_move(c3, True)
    
    win.wait_for_close()

if __name__ == "__main__":
    main()
