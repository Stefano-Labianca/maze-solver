from graphics import  Cell, Window


def main():
    win = Window(800, 600)

    c1 = Cell(win)
    c2 = Cell(win)
    c3 = Cell(win)

    c1.draw(50, 50, 150, 150)
    c2.draw(150, 50, 250, 150)
    c2.draw(250, 50, 350, 150)

    win.wait_for_close()

if __name__ == "__main__":
    main()
