import shiftagoPython.evaluateBoard as me
import copy

class minimaxAlgo():
    def __init__(self, mode, evalfunc, ratios):
        if mode == 'simple':
            if evalfunc == 'lazy':
                self.evalFunc = me.SimpleLazyEval(ratios) # Good ones include (1,5) and (1,9)
        elif mode == 'extreme':
            if evalfunc == 'lazy':
                self.evalFunc = me.ExtremeLazyEval(ratios) # Don't know yet

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

    def getBestMove(self, board, depth):
        bestMove = self.minimaxRoot(board, depth, True)
        return bestMove