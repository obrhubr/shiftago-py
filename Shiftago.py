import shiftagoPython.toFile as toF
import shiftagoPython.consoleOutput as coO

import numpy as np

class SimpleShiftagoGame():
    def __init__(self):
        self.board = np.zeros((7,7), int)
        self.turn = True
        self.gameEnd = False
        self.winner = 0

    def move(self, num):
        if self.gameEnd == True:
            return None
        if num >= 28:
            return False
        else:
            if num//7 == 0:
                if self.checkCol(num%7) == False:
                    return False
                else:
                    self.shiftColRight(num%7)
                    self.board[0,num%7] = 1 if self.turn == True else 2
            elif num//7 == 1:
                if self.checkRow(num%7) == False:
                    return False
                else:
                    self.shiftRowLeft(6-num%7)
                    self.board[num%7,6] = 1 if self.turn == True else 2
            elif num//7 == 2:
                if self.checkCol(6-num%7) == False:
                    return False
                else:
                    self.shiftColLeft(num%7)
                    self.board[6,6-num%7] = 1 if self.turn == True else 2
            elif num//7 == 3:
                if self.checkRow(6-num%7) == False:
                    return False
                else:
                    self.shiftRowRight(6-num%7)
                    self.board[6-num%7,0] = 1 if self.turn == True else 2

            self.turn = not self.turn

        res = self.checkEnd()
        if res != 0:
            self.winner = res
            self.gameEnd = True
            return None
        return True

    def checkEnd(self):
        adjacent1 = 0
        adjacent2 = 0
        adjacent11 = 0
        adjacent22 = 0

        #Check Columns
        for i in range(7):
            for j in range(7):
                if self.board[i,j] == 1:
                    adjacent1 += 1
                    adjacent2 = 0
                if self.board[i,j] == 2:
                    adjacent2 += 1
                    adjacent1 = 0
                if self.board[i,j] == 0:
                    adjacent1 = 0
                    adjacent2 = 0
                if adjacent1 == 4:
                    return 1
                if adjacent2 == 4:
                    return 2

                #Check rows
                if self.board[j,i] == 1:
                    adjacent11 += 1
                    adjacent22 = 0
                if self.board[j,i] == 2:
                    adjacent22 += 1
                    adjacent11 = 0
                if self.board[j,i] == 0:
                    adjacent11 = 0
                    adjacent22 = 0
                if adjacent11 == 4:
                    return 1
                if adjacent22 == 4:
                    return 2


            adjacent11 = 0
            adjacent22 = 0
            adjacent1 = 0
            adjacent2 = 0
        
        #Check top-left to bottom-right diagonal
        res = self.checkDiagonal()
        if res != 0:
            return res
        #Check top-right to bottom-left diagonal
        self.rotate(1)
        res = self.checkDiagonal()
        self.rotate(3)
        if res != 0:
            return res
        #Return 0 because no one won
        return 0

    def printBoard(self):
        coO.printBoard(self.board)
        return

    #Utility functions
    def checkCol(self, num):
        placed = 0
        for i in range(7):
            if self.board[i, num] != 0:
                placed += 1
            if self.board[i, num] == 0:
                return True
        if placed == 7:
            return False
        else:
            return True

    def checkRow(self, num):
        placed = 0
        for i in range(7):
            if self.board[num, i] != 0:
                placed += 1
            if self.board[num, i] == 0:
                return True
        if placed == 7:
            return False
        else:
            return True

    def shiftRowRight(self, num):
        temp = []
        for i in range(7):
            if self.board[num, i] == 0 and i == 0:
                return
            elif self.board[num, i] == 1 or self.board[num, i] == 2:
                temp.append(self.board[num, i])
                self.board[num, i] = 0
            elif self.board[num, i] == 0 and i != 0:
                temp.reverse()
                for j in range(len(temp)):
                    self.board[num, i-j] = temp[j]
                return
        return

    def shiftColRight(self, num):
        temp = []
        for i in range(7):
            if self.board[i, num] == 0 and i == 0:
                return
            elif self.board[i, num] == 1 or self.board[i, num] == 2:
                temp.append(self.board[i, num])
                self.board[i, num] = 0
            elif self.board[i, num] == 0 and i != 0:
                temp.reverse()
                for j in range(len(temp)):
                    self.board[i-j, num] = temp[j]
                return
        return

    def shiftRowLeft(self, num):
        self.rotate(2)
        temp = []
        for i in range(7):
            if self.board[num, i] == 0 and i == 0:
                self.rotate(2)
                return
            elif self.board[num, i] == 1 or self.board[num, i] == 2:
                temp.append(self.board[num, i])
                self.board[num, i] = 0
            elif self.board[num, i] == 0 and i != 0:
                temp.reverse()
                for j in range(len(temp)):
                    self.board[num, i-j] = temp[j]
                self.rotate(2)
                return
        self.rotate(2)
        return

    def shiftColLeft(self, num):
        temp = []
        self.rotate(2)
        for i in range(7):
            if self.board[i, num] == 0 and i == 0:
                self.rotate(2)
                return
            elif self.board[i, num] == 1 or self.board[i, num] == 2:
                temp.append(self.board[i, num])
                self.board[i, num] = 0
            elif self.board[i, num] == 0 and i != 0:
                temp.reverse()
                for j in range(len(temp)):
                    self.board[i-j, num] = temp[j]
                self.rotate(2)
                return
        self.rotate(2)
        return

    def exportBoard(self, filename):
        toF.exportfile(self.board, filename)
        return

    def importBoard(self, board):
        self.board = board
        return
    
    def rotate(self, num):
        self.board = np.rot90(self.board, num)
        return

    def checkDiagonal(self):
        adjacent1 = 0
        adjacent2 = 0
        adjacent11 = 0
        adjacent22 = 0
        for i in range(4):
            for j in range(7-i):
                if self.board[i+j, j] == 1:
                    adjacent1 += 1
                    adjacent2 = 0
                if self.board[i+j, j] == 2:
                    adjacent2 += 1
                    adjacent1 = 0
                if self.board[i+j, j] == 0:
                    adjacent1 = 0
                    adjacent2 = 0
                if adjacent1 == 4:
                    return 1
                if adjacent2 == 4:
                    return 2

                if self.board[j, j+i] == 1:
                    adjacent11 += 1
                    adjacent22 = 0
                if self.board[j, j+i] == 2:
                    adjacent22 += 1
                    adjacent11 = 0
                if self.board[j, j+i] == 0:
                    adjacent11 = 0
                    adjacent22 = 0
                if adjacent11 == 4:
                    return 1
                if adjacent22 == 4:
                    return 2

            adjacent11 = 0
            adjacent22 = 0
            adjacent1 = 0
            adjacent2 = 0
        return 0

class ExtremeShiftagoGame():
    def __init__(self):
        self.board = np.zeros((7,7), int)
        self.turn = True
        self.gameEnd = False
        self.winner = 0
        self.scores = [0, 0]

    def move(self, num):
        if self.gameEnd == True:
            return None
        if 0 in self.board:
            pass
        else:
            return False
        if num >= 28:
            return False
        else:
            if num//7 == 0:
                if self.checkCol(num%7) == False:
                    return False
                else:
                    self.shiftColRight(num%7)
                    self.board[0,num%7] = 1 if self.turn == True else 2
            elif num//7 == 1:
                if self.checkRow(num%7) == False:
                    return False
                else:
                    self.shiftRowLeft(6-num%7)
                    self.board[num%7,6] = 1 if self.turn == True else 2
            elif num//7 == 2:
                if self.checkCol(6-num%7) == False:
                    return False
                else:
                    self.shiftColLeft(num%7)
                    self.board[6,6-num%7] = 1 if self.turn == True else 2
            elif num//7 == 3:
                if self.checkRow(6-num%7) == False:
                    return False
                else:
                    self.shiftRowRight(6-num%7)
                    self.board[6-num%7,0] = 1 if self.turn == True else 2

            self.turn = not self.turn

        res = self.checkEnd()
        if res != 0:
            self.winner = res
            self.gameEnd = True
            return None

        return True

    def checkScores(self):
        if self.scores[0] >= 10:
            return 1
        elif self.scores[1] >= 10:
            return 2
        else:
            return 0

    def checkEnd(self):
        # Check vertical and horizontal
        res = self.checkLines()
        if res == True:
            #Flip this so it flips back later and the same player plays twice
            self.turn = not self.turn
            return self.checkScores()
        #Check top-left to bottom-right diagonal
        res = self.checkDiagonal()
        if res == True:
            #Flip this so it flips back later and the same player plays twice
            self.turn = not self.turn
            return self.checkScores()
        #Check top-right to bottom-left diagonal
        self.rotate(1)
        res = self.checkDiagonal()
        self.rotate(3)
        if res == True:
            #Flip this so it flips back later and the same player plays twice
            self.turn = not self.turn
            return self.checkScores()
        #Check total scores
        return self.checkScores()

    def printBoard(self):
        coO.printBoard(self.board)
        return

    #Utility functions
    def checkCol(self, num):
        placed = 0
        for i in range(7):
            if self.board[i, num] != 0:
                placed += 1
            if self.board[i, num] == 0:
                return True
        if placed == 7:
            return False
        else:
            return True

    def checkRow(self, num):
        placed = 0
        for i in range(7):
            if self.board[num, i] != 0:
                placed += 1
            if self.board[num, i] == 0:
                return True
        if placed == 7:
            return False
        else:
            return True

    def shiftRowRight(self, num):
        temp = []
        for i in range(7):
            if self.board[num, i] == 0 and i == 0:
                return
            elif self.board[num, i] == 1 or self.board[num, i] == 2:
                temp.append(self.board[num, i])
                self.board[num, i] = 0
            elif self.board[num, i] == 0 and i != 0:
                temp.reverse()
                for j in range(len(temp)):
                    self.board[num, i-j] = temp[j]
                return
        return

    def shiftColRight(self, num):
        temp = []
        for i in range(7):
            if self.board[i, num] == 0 and i == 0:
                return
            elif self.board[i, num] == 1 or self.board[i, num] == 2:
                temp.append(self.board[i, num])
                self.board[i, num] = 0
            elif self.board[i, num] == 0 and i != 0:
                temp.reverse()
                for j in range(len(temp)):
                    self.board[i-j, num] = temp[j]
                return
        return

    def shiftRowLeft(self, num):
        self.rotate(2)
        temp = []
        for i in range(7):
            if self.board[num, i] == 0 and i == 0:
                self.rotate(2)
                return
            elif self.board[num, i] == 1 or self.board[num, i] == 2:
                temp.append(self.board[num, i])
                self.board[num, i] = 0
            elif self.board[num, i] == 0 and i != 0:
                temp.reverse()
                for j in range(len(temp)):
                    self.board[num, i-j] = temp[j]
                self.rotate(2)
                return
        self.rotate(2)
        return

    def shiftColLeft(self, num):
        temp = []
        self.rotate(2)
        for i in range(7):
            if self.board[i, num] == 0 and i == 0:
                self.rotate(2)
                return
            elif self.board[i, num] == 1 or self.board[i, num] == 2:
                temp.append(self.board[i, num])
                self.board[i, num] = 0
            elif self.board[i, num] == 0 and i != 0:
                temp.reverse()
                for j in range(len(temp)):
                    self.board[i-j, num] = temp[j]
                self.rotate(2)
                return
        self.rotate(2)
        return

    def exportBoard(self, filename):
        toF.exportfile(self.board, filename)
        return

    def importBoard(self, board):
        self.board = board
        return
    
    def rotate(self, num):
        self.board = np.rot90(self.board, num)
        return

    def remove(self, beg, end):
        if beg[0] != end[0] and beg[1] != end[1]:
            for i in range(beg[0]+1, end[0]):
                    self.board[i, i + beg[1] - beg[0]] = 0
        elif beg[0] == end[0]:
            for j in range(beg[1]+1, end[1]):
                self.board[beg[0], j] = 0
        elif beg[1] == end[1]:
            for i in range(beg[0]+1, end[0]):
                self.board[i, beg[1]] = 0

    def checkNextLines(self, i , j, where):
        if where == 0:
            return self.board[i+1, j]
        elif where == 1:
            return self.board[i, j+1]
        elif where == 2:
            return self.board[i+1, j+1]

    def checkDiagonal(self):
        adjacent1 = 0
        adjacent2 = 0
        adjacent11 = 0
        adjacent22 = 0

        beg1 = None
        beg2 = None

        for i in range(4):
            for j in range(7-i):
                if self.board[i+j, j] == 1:
                    if adjacent1 == 0:
                        beg1 = (i+j, j)
                    adjacent1 += 1
                    adjacent2 = 0
                if self.board[i+j, j] == 2:
                    if adjacent2 == 0:
                        beg1 = (i+j, j)
                    adjacent2 += 1
                    adjacent1 = 0
                if self.board[i+j, j] == 0:
                    beg1 = None
                    adjacent1 = 0
                    adjacent2 = 0
                
                if adjacent1 == 5:
                    if j+i == 6:
                        self.remove(beg1, (i+j, j))
                        self.scores[0] += 2
                        return True
                    else:
                        if self.checkNextLines(i+j, j, 2) != 1:
                            self.remove(beg1, (i+j, j))
                            self.scores[0] += 2
                            return True
                if adjacent2 == 5:
                    if j+i == 6:
                        self.remove(beg1, (i+j, j))
                        self.scores[1] += 2
                        return True
                    else:
                        if self.checkNextLines(i+j, j, 2) != 2:
                            self.remove(beg1, (i+j, j))
                            self.scores[1] += 2
                            return True
                if adjacent1 == 6:
                    if j+i == 6:
                        self.remove(beg1, (i+j, j))
                        self.scores[0] += 5
                        return True
                    else:
                        if self.checkNextLines(i+j, j, 2) != 1:
                            self.remove(beg1, (i+j, j))
                            self.scores[0] += 5
                            return True
                if adjacent2 == 6:
                    if j+i == 6:
                        self.remove(beg1, (i+j, j))
                        self.scores[1] += 5
                        return True
                    else:
                        if self.checkNextLines(i+j, j, 2) != 2:
                            self.remove(beg1, (i+j, j))
                            self.scores[1] += 5
                            return True
                if adjacent1 == 7:
                    self.scores[0] += 10
                    return True
                if adjacent2 == 7:
                    self.scores[1] += 10
                    return True

                if self.board[j, j+i] == 1:
                    if adjacent11 == 0:
                        beg2 = (j, j+i)
                    adjacent11 += 1
                    adjacent22 = 0
                if self.board[j, j+i] == 2:
                    if adjacent22 == 0:
                        beg2 = (j, j+i)
                    adjacent22 += 1
                    adjacent11 = 0
                if self.board[j, j+i] == 0:
                    beg2 = None
                    adjacent11 = 0
                    adjacent22 = 0
                
                
                if adjacent11 == 5:
                    if j+i == 6:
                        self.remove(beg2, (j, j+i))
                        self.scores[0] += 2
                        return True
                    else:
                        if self.checkNextLines(j, j+i, 2) != 1:
                            self.remove(beg2, (j, j+i))
                            self.scores[0] += 2
                            return True
                if adjacent22 == 5:
                    if j+i == 6:
                        self.remove(beg2, (j, j+i))
                        self.scores[1] += 2
                        return True
                    else:
                        if self.checkNextLines(j, j+i, 2) != 2:
                            self.remove(beg2, (j, j+i))
                            self.scores[1] += 2
                            return True
                if adjacent11 == 6:
                    if j+i == 6:
                        self.remove(beg2, (j, j+i))
                        self.scores[0] += 5
                        return True
                    else:
                        if self.checkNextLines(j, j+i, 2) != 1:
                            self.remove(beg2, (j, j+i))
                            self.scores[0] += 5
                            return True
                if adjacent22 == 6:
                    if j+i == 6:
                        self.remove(beg2, (j, j+i))
                        self.scores[1] += 5
                        return True
                    else:
                        if self.checkNextLines(j, j+i, 2) != 2:
                            self.remove(beg2, (j, j+i))
                            self.scores[1] += 5
                            return True
                if adjacent11 == 7:
                    self.scores[0] += 10
                    return True
                if adjacent22 == 7:
                    self.scores[1] += 10
                    return True

            adjacent11 = 0
            adjacent22 = 0
            adjacent1 = 0
            adjacent2 = 0
        return False

    def checkLines(self):
        adjacent1 = 0
        adjacent2 = 0
        adjacent11 = 0
        adjacent22 = 0

        begHor = None
        begVer = None
        
        for i in range(7):
            for j in range(7):
                if self.board[i,j] == 1:
                    if adjacent1 == 0:
                        begHor = (i,j)
                    adjacent1 += 1
                    adjacent2 = 0
                if self.board[i,j] == 2:
                    if adjacent2 == 0:
                        begHor = (i,j)
                    adjacent2 += 1
                    adjacent1 = 0
                if self.board[i,j] == 0:
                    begHor = None
                    adjacent1 = 0
                    adjacent2 = 0

                if adjacent1 == 5:
                    if j == 6:
                        self.remove(begHor, (i, j))
                        self.scores[0] += 2
                        return True
                    else:
                        if self.checkNextLines(i, j, 1) != 1:
                            self.remove(begHor, (i, j))
                            self.scores[0] += 2
                            return True
                if adjacent2 == 5:
                    if j == 6:
                        self.remove(begHor, (i, j))
                        self.scores[1] += 2
                        return True
                    else:
                        if self.checkNextLines(i, j, 1) != 2:
                            self.remove(begHor, (i, j))
                            self.scores[1] += 2
                            return True
                if adjacent1 == 6:
                    if j == 6:
                        self.remove(begHor, (i, j))
                        self.scores[0] += 5
                        return True
                    else:
                        if self.checkNextLines(i, j, 1) != 1:
                            self.remove(begHor, (i, j))
                            self.scores[0] += 5
                            return True
                if adjacent2 == 6:
                    if j == 6:
                        self.remove(begHor, (i, j))
                        self.scores[1] += 5
                        return True
                    else:
                        if self.checkNextLines(i, j, 1) != 2:
                            self.remove(begHor, (i, j))
                            self.scores[1] += 5
                            return True
                if adjacent1 == 7:
                    self.remove(begHor, (i, j))
                    self.scores[0] += 10
                    return True
                if adjacent2 == 7:
                    self.remove(begHor, (i, j))
                    self.scores[1] += 10
                    return True

                #Check cols
                if self.board[j,i] == 1:
                    if adjacent11 == 0:
                        begVer = (j,i)
                    adjacent11 += 1
                    adjacent22 = 0
                if self.board[j,i] == 2:
                    if adjacent22 == 0:
                        begVer = (j,i)
                    adjacent22 += 1
                    adjacent11 = 0
                if self.board[j,i] == 0:
                    begVer = None
                    adjacent11 = 0
                    adjacent22 = 0
                
                if adjacent11 == 5:
                    if j == 6:
                        self.remove(begVer, (j, i))
                        self.scores[0] += 2
                        return True
                    else:
                        if self.checkNextLines(j, i, 0) != 1:
                            self.remove(begVer, (j, i))
                            self.scores[0] += 2
                            return True
                if adjacent22 == 5:
                    if j == 6:
                        self.remove(begVer, (j, i))
                        self.scores[1] += 2
                        return True
                    else:
                        if self.checkNextLines(j, i, 0) != 2:
                            self.remove(begVer, (j, i))
                            self.scores[1] += 2
                            return True
                if adjacent11 == 6:
                    if j == 6:
                        self.remove(begVer, (j, i))
                        self.scores[0] += 5
                        return True
                    else:
                        if self.checkNextLines(j, i, 0) != 1:
                            self.remove(begVer, (j, i))
                            self.scores[0] += 5
                            return True
                if adjacent22 == 6:
                    if j == 6:
                        self.remove(begVer, (j, i))
                        self.scores[1] += 5
                        return True
                    else:
                        if self.checkNextLines(j, i, 0) != 2:
                            self.remove(begVer, (j, i))
                            self.scores[1] += 5
                            return True
                if adjacent11 == 7:
                    self.remove(begVer, (j, i))
                    self.scores[0] += 10
                    return True
                if adjacent22 == 7:
                    self.remove(begVer, (j, i))
                    self.scores[1] += 10
                    return True

            adjacent11 = 0
            adjacent22 = 0
            adjacent1 = 0
            adjacent2 = 0

        return False