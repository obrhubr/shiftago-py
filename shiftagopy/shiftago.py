import numpy as np

class Shiftago():
    def __init__(self):
        self.board = np.zeros((7,7))
        self.game_end = False
        self.turn = 1
        self.winner = 0

    def move(self, num):
        if self.game_end == True:
            return
        
        # Invalid move
        if num < 0 and num > 27:
            return False
        
        if num//7 == 0:
            if self.checkCol(num%7) == False:
                return False
            else:
                self.shiftColRight(num%7)
                self.board[0,num%7] = self.turn
        elif num//7 == 1:
            if self.checkRow(num%7) == False:
                return False
            else:
                self.shiftRowLeft(6-num%7)
                self.board[num%7,6] = self.turn
        elif num//7 == 2:
            if self.checkCol(6-num%7) == False:
                return False
            else:
                self.shiftColLeft(num%7)
                self.board[6,6-num%7] = self.turn
        elif num//7 == 3:
            if self.checkRow(6-num%7) == False:
                return False
            else:
                self.shiftRowRight(6-num%7)
                self.board[6-num%7,0] = self.turn

        # Switch turns
        self.turn = 1 if self.turn == 2 else 2

        # Check for end states
        result = self.check_end()
        if result != 0:
            self.winner = result
            self.game_end = True
        
        return True

    def check_end(self):
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

    def board_to_string(self):
        def player_to_string(num):
            if num == 1:
                return "🟥"
            elif num == 2:
                return "🟦"
            return "⬛"
        
        output = "\n".join(["".join(map(player_to_string, line)) for line in self.board])
        return f"Player {player_to_string(self.turn)}'s turn: \n{output}\n"

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