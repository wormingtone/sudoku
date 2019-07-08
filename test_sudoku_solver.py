import sudoku_solver as ss
import unittest
import numpy as np

#based on https://www.youtube.com/watch?v=6tNS--WetLI

class TestSudokuSolver(unittest.TestCase):


    #hard from Android Sudoku game


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

    def test_updateGrid(self):
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
        s1.give_initial_digits(hard_one)

        hard_one_possibles = [[[2, 6, 7, 8], [2, 6], [2, 3, 6, 7], [2, 5, 6, 7, 8], [1, 2, 4, 5, 6, 8], [2, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8], [4, 5, 6, 8, 9], [3, 4, 5, 7, 8]],
                              [[7, 8, 6], [], [], [], [5, 6, 8], [5, 6, 7, 8], [], [], [5, 7, 8]],
                              [[], [], [2, 3, 6, 7], [2, 6, 7, 8], [2, 4, 6, 8], [], [3, 4, 6, 7, 8], [4, 6, 8], [3, 4, 7, 8]],
                              [[2], [], [], [], [2, 5, 8], [], [5, 8], [], []],
                              [[2, 4, 6, 9], [2, 6, 9], [2, 4, 6], [2, 5, 6, 8], [], [2, 5, 6, 8], [1, 3, 4, 5, 8], [4, 5, 8], [1, 3, 4, 5, 8]],
                              [[4, 6, 7], [], [], [], [6], [], [4], [], []],
                              [[], [], [2, 4, 6], [2, 6, 7, 8], [2, 6, 8, 9], [], [4, 6, 7, 8], [4, 6, 8], [2, 4, 7, 8]],
                              [[1, 2, 6], [], [], [], [2, 5, 6], [2, 5, 6], [], [], [1, 2, 5]],
                              [[1, 2, 4, 6, 9], [2, 6, 9], [2, 4, 6], [2, 5, 6, 7, 8], [2, 3, 5, 6, 8, 9], [2, 5, 6, 7, 8], [1, 4, 5, 6, 7, 8], [4, 5, 6, 8], [1, 2, 4, 5, 7, 8]]]

        print(s1.possiblesByCell)
        self.assertEqual(s1.grid, hard_one)

        #do it with an iteration? zip?


        # test that grid takes on initial values

        # test that possibles takes appropriate values

        # test possibles by house

if __name__ == "__main__":
    unittest.main()
