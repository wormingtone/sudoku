import sudoku_solver as ss
import unittest
import numpy as np

#based on https://www.youtube.com/watch?v=6tNS--WetLI

class TestSudokuSolver(unittest.TestCase):

    #TODO make helper method to test solving methods on empty grid, taking the function to be tested as an argument

    #hard from Android Sudoku game

    #TODO make this work
    def setUp(self):
        #initialize some variables, code run before every test
        # empty grid
        empty = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        all_possibles = [[[num for num in range(1, 10)] for column in range(9)] for row in range(9)]

        #make empty grid of this

    # Helper method used before comparing cell arrays
    def compare_grid_with_ss(self, digit_array, sudoku_grid):
        for rowIndex, row in enumerate(sudoku_grid.grid):
            for columnIndex, cell in enumerate(row):
                self.assertEqual(cell.value, digit_array[rowIndex][columnIndex])

    def test_cell_num_within_square(self):
        should_be_0_a = ss.cell_num_within_square(0, 0)
        self.assertEqual(should_be_0_a, 0)

        should_be_0_b = ss.cell_num_within_square(6, 0)
        self.assertEqual(should_be_0_b, 0)

        should_be_0_c = ss.cell_num_within_square(3, 6)
        self.assertEqual(should_be_0_c, 0)

        should_be_4 = ss.cell_num_within_square(1, 1)
        self.assertEqual(should_be_4, 4)

        should_be_5 = ss.cell_num_within_square(7, 2)
        self.assertEqual(should_be_5, 5)

        should_be_7 = ss.cell_num_within_square(5, 1)
        self.assertEqual(should_be_7, 7)

        should_be_8 = ss.cell_num_within_square(8, 8)
        self.assertEqual(should_be_8, 8)

    def test_coords_to_square(self):
        should_be_0_a = ss.coords_to_square(0, 0)
        self.assertEqual(should_be_0_a, 0)

        should_be_0_b = ss.coords_to_square(1, 1)
        self.assertEqual(should_be_0_b, 0)

        should_be_0_c = ss.coords_to_square(2, 0)
        self.assertEqual(should_be_0_c, 0)

    def test_square_to_coords(self):
        pass

    def test_update_grid_empty(self):

        # get this to work from setUp
        empty = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        all_possibles = [[[num for num in range(1, 10)] for column in range(9)] for row in range(9)]

        s1 = ss.SudokuSolver()
        s1.give_initial_digits(empty)

        empty_cells = grids_to_cell_array(empty, all_possibles)
        print(empty_cells)

        self.assertEqual(s1.grid, empty_cells)

        self.assertTrue(s1.rows[0][0] is s1.columns[0][0])
        self.assertTrue(s1.rows[0][0] is s1.squares[0][0])
        self.assertTrue(s1.rows[1][1] is s1.columns[1][1])

        self.assertTrue(s1.rows[4][4] is s1.squares[4][4])

    #TODO test update possibles_by_house
    def test_update_grid_hard(self):
        hard_one = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 4, 9, 3, 0, 0, 2, 1, 0],
                    [5, 1, 0, 0, 0, 9, 0, 0, 0],
                    [0, 3, 1, 9, 0, 4, 0, 7, 6],
                    [0, 0, 0, 0, 7, 0, 0, 0, 0],
                    [0, 8, 5, 1, 0, 3, 0, 2, 9],
                    [3, 5, 0, 0, 0, 1, 0, 0, 0],
                    [0, 7, 8, 4, 0, 0, 9, 3, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        s1 = ss.SudokuSolver()

        self.assertTrue(s1.rows[0][0] is s1.columns[0][0])
        self.assertTrue(s1.rows[0][0] is s1.squares[0][0])
        self.assertTrue(s1.rows[1][1] is s1.columns[1][1])

        self.assertTrue(s1.rows[4][4] is s1.squares[4][4])

        s1.give_initial_digits(hard_one)

        hard_one_possibles = [[[2, 6, 7, 8], [2, 6], [2, 3, 6, 7], [2, 5, 6, 7, 8], [1, 2, 4, 5, 6, 8], [2, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8], [4, 5, 6, 8, 9], [3, 4, 5, 7, 8]],
                              [[6, 7, 8], [], [], [], [5, 6, 8], [5, 6, 7, 8], [], [], [5, 7, 8]],
                              [[], [], [2, 3, 6, 7], [2, 6, 7, 8], [2, 4, 6, 8], [], [3, 4, 6, 7, 8], [4, 6, 8], [3, 4, 7, 8]],
                              [[2], [], [], [], [2, 5, 8], [], [5, 8], [], []],
                              [[2, 4, 6, 9], [2, 6, 9], [2, 4, 6], [2, 5, 6, 8], [], [2, 5, 6, 8], [1, 3, 4, 5, 8], [4, 5, 8], [1, 3, 4, 5, 8]],
                              [[4, 6, 7], [], [], [], [6], [], [4], [], []],
                              [[], [], [2, 4, 6], [2, 6, 7, 8], [2, 6, 8, 9], [], [4, 6, 7, 8], [4, 6, 8], [2, 4, 7, 8]],
                              [[1, 2, 6], [], [], [], [2, 5, 6], [2, 5, 6], [], [], [1, 2, 5]],
                              [[1, 2, 4, 6, 9], [2, 6, 9], [2, 4, 6], [2, 5, 6, 7, 8], [2, 3, 5, 6, 8, 9], [2, 5, 6, 7, 8], [1, 4, 5, 6, 7, 8], [4, 5, 6, 8], [1, 2, 4, 5, 7, 8]]]

        # for rowIndex, row in enumerate(s1.grid):
        #     for columnIndex, cell in enumerate(row):
        #         self.assertEqual(cell.possibes, hard_one_possibles[rowIndex][columnIndex])

        hard_one_cells = grids_to_cell_array(hard_one, hard_one_possibles)
        self.assertEqual(s1.grid, hard_one_cells)

        self.assertTrue(s1.rows[0][0] is s1.columns[0][0])
        self.assertTrue(s1.rows[0][0] is s1.squares[0][0])
        self.assertTrue(s1.rows[1][1] is s1.columns[1][1])

        self.assertTrue(s1.rows[4][4] is s1.squares[4][4])
        self.assertTrue(s1.rows[1][2] is s1.columns[2][1])

        self.assertTrue(s1.squares[7][2] is s1.columns[5][6])

        #do it with an iteration? zip?


        # test that grid takes on initial values

        # test that possibles takes appropriate values

        # test possibles by house

    #TODO change method name when you want to run it
    def test_find_naked_single(self):
        all_possibles = [[[num for num in range(1, 10)] for column in range(9)] for row in range(9)]

        sparse_empty_0_ = [[[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []]]

        s0 = ss.SudokuSolver()
        s0.possiblesByCell = sparse_empty_0_

        empty = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        s0.find_naked_single()
        cell_array = grids_to_cell_array(empty, all_possibles)
        self.assertEqual(s0.grid, cell_array)

        sparse_empty_1_ = [[[5], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []]]

        s1 = ss.SudokuSolver()
        s1.possiblesByCell = sparse_empty_1_

        just5 = [[5, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        s1.find_naked_single()
        cell_array = grids_to_cell_array(just5, sparse_empty_1_)
        self.assertEqual(s1.grid, cell_array)

        sparse_empty_2_ = [[[], [], [], [], [], [], [3, 6, 7], [], []],
                           [[], [], [7], [], [], [1, 2, 8], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [8], [], []],
                           [[], [3], [], [], [], [4, 7, 8, 9], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [2, 4, 6], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], [9]]]

        s2 = ss.SudokuSolver()
        s2.possiblesByCell = sparse_empty_2_

        justN = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 7, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 8, 0, 0],
                 [0, 3, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 9]]

        s2.find_naked_single()

        self.assertEqual(s2.grid, justN)

    def T_test_find_hidden_single(self):
        sparse_empty_0_ = [[[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []],
                           [[], [], [], [], [], [], [], [], []]]

        s0 = ss.SudokuSolver()

        empty = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        all_possibles = [[[num for num in range(1, 10)] for column in range(9)] for row in range(9)]

        s0.give_initial_digits(empty)
        s0.find_hidden_single()

        cell_array = grids_to_cell_array(empty, all_possibles)
        self.assertEqual(s0.grid, cell_array)

        s0 = ss.SudokuSolver()

        five_ = [[1, 2, 3, 4, 0, 0, 6, 9, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 5, 5, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        fiveH = [[1, 2, 3, 4, 0, 0, 6, 9, 5],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 5, 5, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        #cell has right possibles before find_hidden_single
        #house has right possibles

        s0.give_initial_digits(five_)
        s0.find_hidden_single()
        self.assertEqual(s0.grid, fiveH)


def grids_to_cell_array(values_grid, possibles_grid):
    cell_array = [[] for row in range(9)]

    for rowIndex, row in enumerate(cell_array):
        for columnIndex in range(9):
            cell = ss.Cell(rowIndex, columnIndex)
            cell.value = values_grid[rowIndex][columnIndex]
            cell.possibles = possibles_grid[rowIndex][columnIndex]
            row.append(cell)

    return cell_array


if __name__ == "__main__":
    unittest.main()
