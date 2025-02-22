import copy

class Minimax():
    def __init__(self, ratios, depth = 3):
        self.evalFunc = SimpleLazyEval(ratios) # Good ones include (1,5) and (1,9)
        self.depth = depth
        return

    def minimax(self, game, depth, alpha, beta, playerToMax):
        if depth == 0:
            return -1 * self.evalFunc.evaluateBoard(game.board)
        
        if playerToMax == True:
            bestMoveValue = -9999
            for i in range(28):
                curGame = copy.deepcopy(game)

                move = curGame.move(i)
                if move == False:
                    continue
                elif move == None:
                    bestMoveValue = 9999
                else:
                    bestMoveValue = max(bestMoveValue, self.minimax(curGame, depth-1, alpha, beta, not playerToMax))

                del curGame
                alpha = max(alpha, bestMoveValue)
                if beta <= alpha:
                    return bestMoveValue
            return bestMoveValue
        else:
            bestMoveValue = 9999
            for i in range(28):
                curGame = copy.deepcopy(game)

                move = curGame.move(i)
                if move == False:
                    continue
                elif move == None:
                    bestMoveValue = -9999
                else:
                    bestMoveValue = min(bestMoveValue, self.minimax(curGame, depth-1, alpha, beta, not playerToMax))

                del curGame
                alpha = min(alpha, bestMoveValue)
                if beta <= alpha:
                    return bestMoveValue
                    
            return bestMoveValue

    def minimaxRoot(self, game, depth, playerToMax):
        bestMoveValue = -9999
        bestMoveIndex = None

        for i in range(28):
            curGame = copy.deepcopy(game)

            move = curGame.move(i)
            if move == False:
                continue
            elif move == None:
                return i
            else:
                value = self.minimax(curGame, depth-1, -10000, 10000, not playerToMax)

            del curGame
            if value >= bestMoveValue:
                bestMoveValue = value
                bestMoveIndex = i

        return bestMoveIndex

    def move(self, game):
        bestMove = self.minimaxRoot(game, self.depth, True)
        return bestMove
    
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