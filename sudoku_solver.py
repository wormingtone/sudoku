import numpy as np


class SudokuSolver:
    """doc string goes here"""

    def __init__(self):

        #self.grid = np.array((9, 9), dtype=int)
        self.grid = [[0 for row in range(9)] for column in range(9)]

        #[[list(range(1, 10)) for row in range(9)] for column in range(9)]

        #given current information, the digits that the cell could take
        self.possiblesByCell = [[list(range(1, 10)) for row in range(9)] for column in range(9)]

        #the remaining digits needed to complete a house
        self.possiblesByHouse = [[list(range(1, 10)) for houseNum in range(9)] for houseType in range(3)]

        #house types as lists of lists: each type lists its 9 houses,
        #and each house lists the possible values of each cell
        self.rows = []
        self.columns = []
        self.squares = []

        #list of lists of lists
        self.houses = [self.rows, self.columns, self.squares]

        #feed in initial given values with a series of updates

        for row in range(9):
            row_list = []
            for column in range(9):
                row_list.append(self.possiblesByCell[row][column])
            self.rows.append(self.possiblesByCell[row])

        for column in range(9):
            column_list = []
            for row in range(9):
                column_list.append(self.possiblesByCell[row][column])
            self.columns.append(column_list)

        for square in range(9):
            square_list = []
            coords = square_to_coords(square)
            for coordPair in coords:
                square_list.append(self.possiblesByCell[coordPair[0]][coordPair[1]])
            self.squares.append(square_list)
        cheese = []

    #pass in given values in the form of a 2d array with 0s as empty spaces
    #TODO exclude invalid arrays
    def give_initial_digits(self, digit_array):
        for row in range(9):
            for column in range(9):
                self.update_grid(row, column, digit_array[row][column])

    #possiblesByCell is primary, so first update that, then find the relevant houses and update those only
    def update_grid(self, i, j, digit):
        self.grid[i][j] = digit
        if digit == 0:
            return

        self.possiblesByCell[i][j] = []

        #pruning away from the possibles
        for set_of_possibles in self.rows[i]:
            for cell in set_of_possibles:
                if cell > digit:
                    break
                if cell == digit:
                    sRemove(set_of_possibles, digit)
                    break

        for set_of_possibles in self.columns[j]:
            for cell in set_of_possibles:
                if cell > digit:
                    break
                if cell == digit:
                    sRemove(set_of_possibles, digit)
                    break

        # TODO this nonsense
        # for set_of_possibles in self.squares[coords_to_square(i, j)]:
        #     for cell in set_of_possibles:
        #         if cell > digit:
        #             break
        #         if cell == digit:
        #             sRemove(set_of_possibles, digit)
        #             break
        #update squares I THINK THIS IS UNNECESSARY??? IT IS DEFINITELY NECESSARY!

        #update possiblesByHouse
        self.possiblesByHouse[0][i].remove(digit)  # update column
        self.possiblesByHouse[1][j].remove(digit)  # update row
        self.possiblesByHouse[2][i].remove(digit)  # update square

    def find_naked_single(self):
        for row in self.possiblesByCell:
            for column in self.possiblesByCell:
                if self.possiblesByCell[row][column].len() == 1:
                    self.update_grid(row, column, self.possiblesByCell[row][column][0])

    def find_hidden_single(self):

        #get the remaining candidate digits for the house
        for houseType in range(3):
            for houseNum in range(9):
                remainingDigits = self.possiblesByHouse[houseType][houseNum]
                cells = self.getCellsInHouse(houseType, houseNum)


                #for each candidate digit, count its occurrences over every cell in the house
                for digit in remainingDigits:
                    digitCount = 0

                    for cell in cells:
                        cellPossibles = self.houses[cell[0]][cell[1]]
                        if digit in cellPossibles:
                            digitCount += 1

                #if the digit has only one possible location in house, fill in that grid cell
                if digitCount == 1:
                    self.update_grid(cell[0], cell[1], digit)

    #TODO naked pair
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

    #Assuming cells have a default value of 0
    def isCellEmpty(self, cellRow, cellColumn):
        return self.grid[cellRow, cellColumn] == 0


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

        while (True):

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

    #returns a list of 9 coordinate pairs for a given house
    def getCellsInHouse(houseType, houseNum):
        if houseType not in [0, 1, 2]:
            raise TypeError("houseTypes are 0 == rows, 1 == columns, 2 == squares")

        cells = []

        if houseType == 0:
            for column in range(9):
                cells.append([houseNum, column])

        if houseType == 1:
            for row in range(9):
                cells.append(row, houseNum)

        if houseType == 2:
            cells = square_to_coords(houseNum)

        return cells


    def getPossibleCellsForDigitInHouse(self, digit, houseType, houseNum):
        occurences = []

        cellsInHouse = self.getCellsInHouse(houseType, houseNum)

        for cell in cellsInHouse:
            if digit in self.possiblesByCell[cell[0]][cell[1]]:
                occurences.append(cell)




#given a cell's coordinates, find the square it is in.
def coords_to_square(i, j):
    return (i // 3) + j % 3

# return a list 9 coord pairs for a given square
def square_to_coords(square_index):
    coords_list = []

    i = 3 * (square_index // 3)
    j = 3 * (square_index % 3)

    for row in range(i, i + 3):
        for column in range(j, j + 3):
            coords_list.append([row, column])

    return coords_list

def sRemove(l, element): #TODO
    if not isinstance(l, list):
        raise TypeError("Trying to remove from something that isn't a list")

    if element in l:
        l.remove(element)



