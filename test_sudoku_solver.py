import sudoku_solver as ss
import unittest
import numpy as np

#based on https://www.youtube.com/watch?v=6tNS--WetLI

class TestSudokuSolver(unittest.TestCase):


    #hard from Android Sudoku game


    def setUp(self):
        #initialize some variables, code run before every test
        # empty grid
        empty = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0]])

    def test_updateGrid(self):
        hard_one = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 4, 9, 3, 0, 0, 2, 1, 0],
                             [5, 1, 0, 0, 0, 9, 0, 0, 0],
                             [0, 3, 1, 9, 0, 4, 0, 7, 6],
                             [0, 0, 0, 0, 7, 0, 0, 0, 0],
                             [0, 8, 5, 1, 0, 3, 0, 2, 9],
                             [3, 5, 0, 0, 0, 1, 0, 0, 0],
                             [0, 7, 8, 4, 0, 0, 9, 3, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]])

        s1 = ss.SudokuSolver()
        s1.give_initial_digits(hard_one)

        self.assertEqual(s1.grid, hard_one)

        #do it with an iteration? zip?


        # test that grid takes on initial values

        # test that possibles takes appropriate values

        # test possibles by house

if __name__ == "__main__":
    unittest.main()
