import numpy as np

class SudokuSolver:
    """doc string goes here"""


    def __init__(self):

        self.given_digits = [] #list of triples (i, j, digit)

        self.grid = np.array((9, 9), dtype=int)

        self.possibles = np.array((9, 9), dtype=list)

        for row in range(9):
            for column in range(9):
                self.possibles[row, column] = [1,2,3,4,5,6,7,8,9] #TODO replace

        #update possibles

        # make houses as lists
        self.rows = []
        self.columns = []
        self.squares = []

        #updates possibles with given digits before making houses out of possibles!

        for row in range(9):
            self.rows.append(self.possibles[row])

        for column in range(9):
            column_list = []
            for row in range(9):
                column_list.append(self.possibles[row, column])

        for square in range(9):
            self.squares[square] = square_to_coords(square)


    def update_grid(self, i, j, digit):
        self.grid[i, j] = digit
        self.possibles[i, j] = []

        for cell in range(self.rows[i]):
            if self.rows[i][cell] > digit:
                break
            if self.rows[i][cell] == digit:
                self.rows[i].remove(digit)

        for cell in range(self.columns[j]):
            if self.columns[j][cell] > digit:
                break
            if self.columns[j][cell] == digit:
                self.columns[j].remove(digit)

        #update squares


    #use separate driver method, or just have the method take no coordinate parameter and iterate over grid itself?
    def find_naked_single(self, i, j):
        if self.possibles[i, j].len() == 0:
            self.grid[i, j] = self.possibles[i, j][0]
            #update

    def find_hidden_single(self, list):
        pass
        #search by house list

    #TODO define safe remove method

def coords_to_square(i, j):
    return (i // 3) + j % 3

# return a list 9 coord pairs
def square_to_coords(square_num):
    coords_list = []

    i = square_num // 3
    j = square_num % 3

    for row in range(i + 3):
        for column in range(j + 3):
            coords_list.append((row, column))

    return coords_list



