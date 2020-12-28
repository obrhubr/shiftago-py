class lazyEval():
    def __init__(self, ratio1, ratio2):
        self.ratio1 = ratio1
        self.ratio2 = ratio2
    
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