import unittest

from graphics import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        
        self.assertEqual(
            len(m1.get_cells()),
            num_cols,
        )

        self.assertEqual(
            len(m1.get_cells()[0]),
            num_rows,
        )

    def test_maze_with_negative_rows(self):
        num_cols = 12
        num_rows = -10

        self.assertRaises(ValueError, lambda: Maze(0, 0, num_rows, num_cols, 10, 10))

    
    def test_maze_with_negative_columns(self):
        num_cols = -12
        num_rows = 10

        self.assertRaises(ValueError, lambda: Maze(0, 0, num_rows, num_cols, 10, 10))

    def test_maze_with_invalid_cell_size(self):
        num_cols = 12
        num_rows = 10

        self.assertRaises(ValueError, lambda: Maze(0, 0, num_rows, num_cols, -10, 0))

    def test_create_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        cells = m1.get_cells()

        entrance_cell = cells[0][0]
        exit_cell = cells[num_cols - 1][num_rows - 1]

        self.assertEqual(entrance_cell.has_top_wall, False)
        self.assertEqual(exit_cell.has_bottom_wall, False)

if __name__ == "__main__":
    unittest.main()