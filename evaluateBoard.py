class SimpleLazyEval():
    def __init__(self, ratios):
        self.ratio1 = ratios[0]
        self.ratio2 = ratios[1]
    
    def evaluateStraight(self, board):
        value = 0

        adjacent1 = 0
        adjacent2 = 0
        adjacent11 = 0
        adjacent22 = 0

        #Check Columns
        for i in range(7):
            for j in range(7):
                if board[i,j] == 1:
                    adjacent1 += 1
                    adjacent2 = 0
                if board[i,j] == 2:
                    adjacent2 += 1
                    adjacent1 = 0
                if board[i,j] == 0:
                    adjacent1 = 0
                    adjacent2 = 0
                if adjacent1 == 2:
                    value += self.ratio1
                if adjacent2 == 2:
                    value += -1 * self.ratio1
                if adjacent1 == 3:
                    value += self.ratio2
                if adjacent2 == 3:
                    value += -1 * self.ratio2

                #Check rows
                if board[j,i] == 1:
                    adjacent11 += 1
                    adjacent22 = 0
                if board[j,i] == 2:
                    adjacent22 += 1
                    adjacent11 = 0
                if board[j,i] == 0:
                    adjacent11 = 0
                    adjacent22 = 0
                if adjacent11 == 2:
                    value += self.ratio1
                if adjacent22 == 2:
                    value += -1 * self.ratio1
                if adjacent11 == 3:
                    value += self.ratio2
                if adjacent22 == 3:
                    value += -1 * self.ratio2


            adjacent11 = 0
            adjacent22 = 0
            adjacent1 = 0
            adjacent2 = 0

        return value

    def evaluateDiagonals(self, board):
        value = 0

        adjacent1 = 0
        adjacent2 = 0
        adjacent11 = 0
        adjacent22 = 0
        
        for i in range(4):
            for j in range(7-i):
                if board[i+j, j] == 1:
                    adjacent1 += 1
                    adjacent2 = 0
                if board[i+j, j] == 2:
                    adjacent2 += 1
                    adjacent1 = 0
                if board[i+j, j] == 0:
                    adjacent1 = 0
                    adjacent2 = 0
                if adjacent1 == 2:
                    value += self.ratio1
                if adjacent2 == 2:
                    value += -1 * self.ratio1
                if adjacent1 == 3:
                    value += self.ratio2
                if adjacent2 == 3:
                    value += -1 * self.ratio2

                if board[j, j+i] == 1:
                    adjacent11 += 1
                    adjacent22 = 0
                if board[j, j+i] == 2:
                    adjacent22 += 1
                    adjacent11 = 0
                if board[j, j+i] == 0:
                    adjacent11 = 0
                    adjacent22 = 0
                if adjacent11 == 2:
                    value += self.ratio1
                if adjacent22 == 2:
                    value += -1 * self.ratio1
                if adjacent11 == 3:
                    value += self.ratio2
                if adjacent22 == 3:
                    value += -1 * self.ratio2

            adjacent11 = 0
            adjacent22 = 0
            adjacent1 = 0
            adjacent2 = 0

        return value

    def evaluateBoard(self, board):
        value = 0
        
        value += self.evaluateStraight(board)
        value += self.evaluateDiagonals(board)

        return value

class ExtremeLazyEval():
    def __init__(self, ratios):
        self.ratio1 = ratios[0]
        self.ratio2 = ratios[1]
        self.ratio3 = ratios[2]
        self.ratio4 = ratios[3]
        self.ratio5 = ratios[4]

    def checkNextLines(self, board, i , j, where):
        if where == 0:
            return board[i+1, j]
        elif where == 1:
            return board[i, j+1]
        elif where == 2:
            return board[i+1, j+1]
    
    def evaluateStraight(self, board):
        value = 0

        adjacent1 = 0
        adjacent2 = 0
        adjacent11 = 0
        adjacent22 = 0
        
        for i in range(7):
            for j in range(7):
                if board[i,j] == 1:
                    adjacent1 += 1
                    adjacent2 = 0
                if board[i,j] == 2:
                    adjacent2 += 1
                    adjacent1 = 0
                if board[i,j] == 0:
                    adjacent1 = 0
                    adjacent2 = 0

                if adjacent1 == 3:
                    value += 1 * self.ratio1
                if adjacent2 == 3:
                    value += -1 * self.ratio1
                if adjacent1 == 4:
                    value += 1 * self.ratio2
                if adjacent2 == 4:
                    value += -1 * self.ratio2
                if adjacent1 == 5:
                    if j == 6:
                        value += 1 * self.ratio3
                    else:
                        if self.checkNextLines(board, i, j, 1) == 0:
                            value += 1 * self.ratio3
                if adjacent2 == 5:
                    if j == 6:
                        value += -1 * self.ratio3
                    else:
                        if self.checkNextLines(board, i, j, 1) == 0:
                            value += -1 * self.ratio3
                if adjacent1 == 6:
                    if j == 6:
                        value += 1 * self.ratio4
                    else:
                        if self.checkNextLines(board, i, j, 1) == 0:
                            value += 1 * self.ratio4
                if adjacent2 == 6:
                    if j == 6:
                        value += -1 * self.ratio4
                    else:
                        if self.checkNextLines(board, i, j, 1) == 0:
                            value += -1 * self.ratio4
                if adjacent1 == 7:
                    value += 1 * self.ratio5
                if adjacent2 == 7:
                    value += -1 * self.ratio5

                #Check rows
                if board[j,i] == 1:
                    adjacent11 += 1
                    adjacent22 = 0
                if board[j,i] == 2:
                    adjacent22 += 1
                    adjacent11 = 0
                if board[j,i] == 0:
                    adjacent11 = 0
                    adjacent22 = 0

                if adjacent11 == 3:
                    value += 1 * self.ratio1
                if adjacent22 == 3:
                    value += -1 * self.ratio1
                if adjacent11 == 4:
                    value += 1 * self.ratio2
                if adjacent22 == 4:
                    value += -1 * self.ratio2
                if adjacent11 == 5:
                    if j == 6:
                        value += 1 * self.ratio3
                    else:
                        if self.checkNextLines(board, j, i, 0) == 0:
                            value += 1 * self.ratio3
                if adjacent22 == 5:
                    if j == 6:
                        value += -1 * self.ratio3
                    else:
                        if self.checkNextLines(board, j, i, 0) == 0:
                            value += -1 * self.ratio3
                if adjacent11 == 6:
                    if j == 6:
                        value += 1 * self.ratio4
                    else:
                        if self.checkNextLines(board, j, i, 0) == 0:
                            value += 1 * self.ratio4
                if adjacent22 == 6:
                    if j == 6:
                        value += -1 * self.ratio4
                    else:
                        if self.checkNextLines(board, j, i, 0) == 0:
                            value += -1 * self.ratio4
                if adjacent11 == 7:
                    value += 1 * self.ratio5
                if adjacent22 == 7:
                    value += -1 * self.ratio5

            adjacent11 = 0
            adjacent22 = 0
            adjacent1 = 0
            adjacent2 = 0

        return value

    def evaluateDiagonals(self, board):
        value = 0

        adjacent1 = 0
        adjacent2 = 0
        adjacent11 = 0
        adjacent22 = 0

        for i in range(4):
            for j in range(7-i):
                if board[i+j, j] == 1:
                    adjacent1 += 1
                    adjacent2 = 0
                if board[i+j, j] == 2:
                    adjacent2 += 1
                    adjacent1 = 0
                if board[i+j, j] == 0:
                    adjacent1 = 0
                    adjacent2 = 0
                
                if adjacent1 == 3:
                    value += 1 * self.ratio1
                if adjacent2 == 3:
                    value += -1 * self.ratio1
                if adjacent1 == 4:
                    value += 1 * self.ratio2
                if adjacent2 == 4:
                    value += -1 * self.ratio2
                if adjacent1 == 5:
                    if j+i == 6:
                        value += 1 * self.ratio3
                    else:
                        if self.checkNextLines(board, i+j, j, 2) == 0:
                            value += 1 * self.ratio3
                if adjacent2 == 5:
                    if j+i == 6:
                        value += -1 * self.ratio3
                    else:
                        if self.checkNextLines(board, i+j, j, 2) == 0:
                            value += -1 * self.ratio3
                if adjacent1 == 6:
                    if j+i == 6:
                        value += 1 * self.ratio4
                    else:
                        if self.checkNextLines(board, i+j, j, 2) == 0:
                            value += 1 * self.ratio4
                if adjacent2 == 6:
                    if j+i == 6:
                        value += -1 * self.ratio4
                    else:
                        if self.checkNextLines(board, i+j, j, 2) == 0:
                            value += -1 * self.ratio4
                if adjacent1 == 7:
                    value += 1 * self.ratio5
                if adjacent2 == 7:
                    value += -1 * self.ratio5

                if board[j, j+i] == 1:
                    adjacent11 += 1
                    adjacent22 = 0
                if board[j, j+i] == 2:
                    adjacent22 += 1
                    adjacent11 = 0
                if board[j, j+i] == 0:
                    adjacent11 = 0
                    adjacent22 = 0
                
                if adjacent11 == 3:
                    value += 1 * self.ratio1
                if adjacent22 == 3:
                    value += -1 * self.ratio1
                if adjacent11 == 4:
                    value += 1 * self.ratio2
                if adjacent22 == 4:
                    value += -1 * self.ratio2
                if adjacent11 == 5:
                    if j+i == 6:
                        value += 1 * self.ratio4
                    else:
                        if self.checkNextLines(board, j, j+i, 2) == 0:
                            value += 1 * self.ratio3
                if adjacent22 == 5:
                    if j+i == 6:
                        value += 1 * self.ratio4
                    else:
                        if self.checkNextLines(board, j, j+i, 2) == 0:
                            value += -1 * self.ratio3
                if adjacent11 == 6:
                    if j+i == 6:
                        value += 1 * self.ratio4
                    else:
                        if self.checkNextLines(board, j, j+i, 2) == 0:
                            value += 1 * self.ratio4
                if adjacent22 == 6:
                    if j+i == 6:
                        value += -1 * self.ratio4
                    else:
                        if self.checkNextLines(board, j, j+i, 2) == 0:
                            value += -1 * self.ratio4
                if adjacent11 == 7:
                    value += 1 * self.ratio5
                if adjacent22 == 7:
                    value += -1 * self.ratio5

            adjacent11 = 0
            adjacent22 = 0
            adjacent1 = 0
            adjacent2 = 0
        
        return value

    def evaluateBoard(self, board):
        value = 0
        
        value += self.evaluateStraight(board)
        value += self.evaluateDiagonals(board)

        return value