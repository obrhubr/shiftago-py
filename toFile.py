import os

def exportfile(board, fileName):
    f = open(fileName, "a")

    for i in range(7):
        strToWrite = str(board[i, 0]) + ',' +  str(board[i, 1]) + ',' + str(board[i, 2]) + ',' +  str(board[i, 3]) + ',' +  str(board[i, 4]) + ',' +  str(board[i, 5]) + ',' +  str(board[i, 6]) + ','
        if i == 6:
            f.write(strToWrite[:-1])
        else:
            f.write(strToWrite)

    f.write('\n')
    
    f.close()
    return