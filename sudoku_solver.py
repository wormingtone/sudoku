import numpy as np

class SudokuSolver:
    """doc string goes here"""


    def __init__(self):

        self.given_digits = [] #list of triples (i, j, digit)

        self.grid = np.array((9, 9), dtype=int)

        #given current information, the digits that the cell could take
        self.possiblesByCell = np.array((9, 9), dtype=list)

        #the remaining digits needed to complete a house
        self.possiblesByHouse = np.array((3, 9), dtype=list)

        for row in range(9):
            for column in range(9):
                self.possiblesByCell[row, column] = list(range(1,10))

        for houseType in range (3):
            for houseNum in range (9):
                self.possiblesByHouse[houseType, houseNum] = list(range(1,10))

        #house types as lists of lists: each type lists its 9 houses,
        #and each house lists the possible values of each cell
        self.rows = []
        self.columns = []
        self.squares = []

        #list of lists of lists
        self.houses = [self.rows, self.columns, self.squares]

        #feed in initial given values with a series of updates

        for row in range(9):
            self.rows.append(self.possiblesByCell[row])

        for column in range(9):
            column_list = []
            for row in range(9):
                column_list.append(self.possiblesByCell[row, column])

        for square in range(9):
            self.squares[square] = square_to_coords(square)


    def update_grid(self, i, j, digit):
        self.grid[i, j] = digit
        self.possiblesByCell[i, j] = []

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
        if self.possiblesByCell[i, j].len() == 0:
            self.grid[i, j] = self.possiblesByCell[i, j][0]
            #update

    def find_hidden_single(self, list):
        for houseType in range(3):
            for houseNum in range(9):
                remainingDigits = self.possiblesByHouse[houseType, houseNum]

                # if it occurs only once in house
                digitCount = 0
                for digit in remainingDigits:
                    for cell in self.houses[houseType,houseNum]:
                        if digit == cell:
                            digitCount += 1
                if digitCount == 1:
                    sRemove(self.houses[houseType,houseNum], digit)

    #TODO naked pair
    #

    #TODO hidden pair
    #if there is a pair of digits that can only exist in 2 cells in a house, those two cells cannot contain any other
    #values

    def hiddenPairUpdate(self):

        #find one or more pairs in a given house
        def findPairs(houseType, houseNum):
            digitCounts = {}
            remainingDigits = self.possiblesByHouse[houseType, houseNum]
            for remainingDigit in remainingDigits
                digitCounts.update(remainingDigit, 0)

            #count occurences of digits in houses
            for cellPossibles in self.houses[houseType, houseNum]:
                for possible in cellPossibles:
                    digitCounts.update(possible, digitCounts[possible]+1)

            #identify which digits are pairs
            pairedNumbers = []
            for key in remainingDigits:
                if digitCounts[key] == 2:
                    pairedNumbers.add(key)

            #find which cells are paired
            cellsWithPairs = {}
            for number in pairedNumbers:
                cellsWithPairs.update(number, [])

            for cell in self.houses[houseType, houseNum]:
                if




                #find hidden pair
        for houseType in range(3):
            for houseNum in range(9):
                digitCounts = {}
                for remainingDigit in self.possiblesByHouse[houseType, houseNum]
                    digitCounts.update(remainingDigit, 0)

                for digit in remainingDigits:
                    for cell in self.houses[houseType,houseNum]:
                        if digit == cell:
                            digitCount += 1

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









#given a cell's coordinates, find the square it is in.
def coords_to_square(i, j):
    return (i // 3) + j % 3

# return a list 9 coord pairs for a given square
def square_to_coords(square_index):
    coords_list = []

    i = square_index // 3
    j = square_index % 3

    for row in range(i + 3):
        for column in range(j + 3):
            coords_list.append((row, column))

    return coords_list

def sRemove(l, element): #TODO
    if not isinstance(l, list):
        pass
       # throw new IllegalArgumentException
    if l.contains(element):
       l.remove(element)



