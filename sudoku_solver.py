# Have list of finished cells?
import numpy as np

class Cell:
    """doc string goes here"""
    def __init__(self, row, column):
        self.row = row
        self.column = column

        self.possibles = list(range(1, 10))
        self.value = 0 # the cell's final value

        # TODO check out dictionary literal
        # TODO what is a literal, e.g. String literal?
        # perhaps have to update the cells with houses after all cells created?
        # make function that returns house for given cells
        self.houses = {}

    def __eq__(self, other):
        if not isinstance(other, Cell):
            raise Exception("Other is not a Cell")

        return self.value == other.value and self.possibles == other.possibles


class SudokuSolver:
    """doc string goes here"""

    def __init__(self):

        # give the cell a name when it is created for faster lookup?
        self.grid = [[Cell(row, column) for row in range(9)] for column in range(9)]

        # the remaining digits needed to complete a house
        self.possiblesByHouse = [[list(range(1, 10)) for houseNum in range(9)] for houseType in range(3)]

        # house types as lists of lists: each type lists its 9 houses,
        # and each house lists the possible values of each cell
        self.rows = []
        self.columns = []
        self.squares = []

        #list of lists of lists
        self.houses = [self.rows, self.columns, self.squares]

        for row in range(9):
            self.rows.append(self.grid[row])

        #TODO do this once by house?
        for row in self.rows:
            for cell in row:
                cell.houses["row"] = row

        for column in range(9):
            self.columns.append([self.grid[row][column] for row in range(9)])

        for column in self.columns:
            for cell in column:
                cell.houses["column"] = column

        for square in range(9):
            self.squares.append([self.grid[coord_pair[0]][coord_pair[1]]
                                 for coord_pair in square_to_coords(square)])

        for square in self.squares:
            for cell in square:
                cell.houses["square"] = square

    # pass in given values in the form of a 2d array with 0s as empty spaces
    # TODO exclude invalid arrays
    def give_initial_digits(self, digit_array):
        for row in range(9):
            for column in range(9):
                if digit_array[row][column] != 0:
                    self.update_grid(row, column, digit_array[row][column])

    # possiblesByCell is primary, so first update that, then find the relevant houses and update those only
    def update_grid(self, i, j, digit):

        cell = self.grid[i][j]
        cell.value = digit
        cell.possibles.clear()

        for house in cell.houses.values():
            for neighbour in house:
                sRemove(neighbour.possibles, digit)

        # updating the possibles of other cells that share a house
        # for cell in self.rows[i]:
        #     sRemove(cell.possibes, digit)
        #
        # for cell in self.columns[j]:
        #     sRemove(cell.possibles, digit)
        #
        # for cell in self.squares[coords_to_square(i, j)]:
        #     sRemove(cell.possibles, digit)

        #update possiblesByHouse
        # TODO refactor this
        sRemove(self.possiblesByHouse[0][i], digit)
        # self.possiblesByHouse[0][i].remove(digit)  # update column
        sRemove(self.possiblesByHouse[1][j], digit)
        # self.possiblesByHouse[1][j].remove(digit)  # update row

        sRemove(self.possiblesByHouse[2][cell_num_within_square(i, j)], digit) # update square TODO fix this
        # self.possiblesByHouse[2][i].remove(digit)  # update square TODO fix this

    def find_naked_single(self):

        for row in self.rows:
            for cell in row:
                if len(cell.possibles) == 1:
                    self.update_grid(cell.row, cell.column, cell.possibles[0])

    def find_hidden_single(self):

        # get the remaining candidate digits for the house
        for type_index, house_type in enumerate(self.houses):
            for house_num, house in enumerate(house_type):
                remaining_digits = self.possiblesByHouse[type_index][house_num]

                cells_in_house = house

                # for each candidate digit, count its occurrences over every cell in the house
                for digit in remaining_digits:
                    digit_count = 0

                    for cell in cells_in_house:
                        if digit in cell.possibles:
                            digit_count += 1

                    # if the digit has only one possible location in house, fill in that grid cell
                    if digit_count == 1:
                        self.update_grid(cell.row, cell.column, digit)

    #TODO naked pair/triple
    #If there is a naked pair of digits A, B in a house then neither A nor B is a candidate possible in any other
    #cell in that house

    #TODO locked candidates
    #(1) "If in a block all candidates of a certain digit are confined to a row or column, that digit cannot appear
    #outside of that block in that row or column."
    #
    #(2)"Locked Candidates Type 2 works exactly the other way round: If in a row (or column) all candidates of
    # a certain digit are confined to one block, that candidate that be eliminated from all other cells in that block."

    def lockedCandidatesUpdate(self):
        #type (1) first
        #for each possible digit in a square, get the coords of that digit's occurence
        #if they are all in the same row or column
        #remove that digit from the possibles in that row or column outside of that square
        for squareIndex in range(9):
            possibleDigits = self.possiblesByHouse[2, squareIndex]
            for digit in possibleDigits:
                possibleCells = self.getPossibleCellsForDigitInHouse(digit, 2, squareIndex)
                #there should always be at least one cell in possibleCells
                row = possibleCells[0][0]
                column = possibleCells[0][1]

                sameRowFlag = True
                sameColumnFlag = True

                #all cells in same row?
                for cell in possibleCells:
                    if cell[0] != row:
                        sameRowFlag = False
                        break

                #all cells in same column?
                for cell in possibleCells:
                    if cell[1] != column:
                        sameColumnFlag = False
                        break

                if sameRowFlag:
                    #remove note from all other cells in that row
                    firstColumnInSquare = (squareIndex % 3)*3
                    rowSet = set(range(1,10))
                    squareSet = set(range(firstColumnInSquare, firstColumnInSquare + 2))

                    for columnIndex in rowSet-squareSet:
                        sRemove(self.possiblesByCell[row][columnIndex], digit)

                if sameColumnFlag:
                    #remove note from all other cells in that column
                    firstRowInSquare = (squareIndex // 3) * 3
                    columnSet = set(range(1,10))
                    squareSet = set(range(firstRowInSquare, firstRowInSquare + 2))

                    for rowIndex in columnSet-squareSet:
                        sRemove(self.possiblesByCell[rowIndex][column], digit)

    #if there is a pair of digits that can only exist in 2 cells in a house, you can eliminate all other candiate
    #possibles for those two cells
    def hiddenPairUpdate(self):

        for houseType in range(3):
            for houseNum in range(9):

                #create dictionary to store the locations of each possible digit in a house
                digit2CellCoords = {}
                for possibleDigit in self.possiblesByHouse[houseType][houseNum]:
                    digit2CellCoords.update(possibleDigit, [])

                #add the locations of the digits that occur exactly twice
                digitPairs = {}
                for digit, coords in digit2CellCoords.items():
                    if coords.len == 2:
                        digitPairs.update(digit, coords)

                #find any two cells containing a pair
                for digit, coords in digitPairs.items():
                    for digit2, coords2 in digitPairs.items():
                        if digit != digit2:
                            if coords == coords2:
                                for cell in coords:

                                    #remove all other digits
                                    for possibleCandidate in self.possiblesByCell[cell[0]][cell[1]]:
                                        if possibleCandidate not in [digit, digit2]:
                                            sRemove(self.possiblesByCell[cell[0]][cell[1]], possibleCandidate)






    #Checks if adding a given digit to a cell violates the uniqueness conditions on houses.
    #Does not check if it creates an impossible board state, i.e. where no digit can fill an empty cell
    #Is this even possible?
    def isMoveLegal(self, moveRow, moveColumn, digit):
        if digit in self.rows[moveRow]:
            return False

        if digit in self.columns[moveColumn]:
            return False

        if digit in self.houses[coords_to_square(moveRow, moveColumn)]:
            return False

        return True

    #order spaces to be searched by fewest possibilities first.
    #is this DFS with a feasibility check?
    def exhaustiveSearch(self):
        #first get coords of all unfilled cells.
        #sort them into an order

        #list of triples representing unfilled cells, defined by row, column, and number of possibles values the cell
        #can take
        unfilledTriples = []


        for row in range(9):
            for column in range(9):

                if self.isCellEmpty(row, column):
                    possibles = self.possiblesByCell[row, column].len
                    unfilledTriples.append([row, column, possibles])

        #sort in ascending order of remaining possibilities.
        def getPossibles(listElement):
            return listElement[2]

        unfilledTriples.sort(key = getPossibles)

        #create indices for each cell expressing the current child
        #lower nodes indices must be scrubbed each time

        nodeIndices = np.full(shape = unfilledTriples.len, fill_value = 0)
        currentNode = 0

        while True:

            currentTriple = unfilledTriples[currentNode]

            currentCellPossibles = self.possiblesByCell[currentTriple[0], currentTriple[1]]

            if self.isMoveLegal(currentTriple[0], currentTriple[1], currentCellPossibles[nodeIndices[currentNode]]):

                # break condition: legal value is assigned to max depth node
                if currentNode == nodeIndices.len:
                    return

                #Update the grid with the current legal move
                self.grid[currentTriple[0], currentTriple[1]] = [currentCellPossibles[nodeIndices[currentNode]]]
                currentNode += 1

            else:
                #try next branch
                nodeIndices[currentNode] += 1

                # when no legal move is possible for a node, go back a level to the node's parent and refresh the children's
                # indices
                if nodeIndices[currentNode] >= currentCellPossibles.len:
                    self.grid[currentTriple[0], currentTriple[1]] = 0
                    nodeIndices[currentNode] = 0
                    currentNode -= 1


    def getPossibleCellsForDigitInHouse(self, digit, houseType, houseNum):
        occurences = []

        cellsInHouse = self.houses[houseType][houseNum]

        for cell in cellsInHouse:
            if digit in self.possiblesByCell[cell[0]][cell[1]]:
                occurences.append(cell)

# given a cell's coordinates, find the square it is in.
def coords_to_square(i, j):
    return 3 * (i // 3) + j // 3


# return a list 9 coord pairs for a given square
def square_to_coords(square_index):
    coords_list = []

    i = 3 * (square_index // 3)
    j = 3 * (square_index % 3)

    for row in range(i, i + 3):
        for column in range(j, j + 3):
            coords_list.append([row, column])

    return coords_list

# 0 1 2
# 3 4 5
# 6 7 8
def cell_num_within_square(i, j):
    return 3 * (i % 3) + j % 3

def sRemove(l, element): #TODO
    if not isinstance(l, list):
        raise TypeError("Trying to remove from something that isn't a list")

    if element in l:
        l.remove(element)



