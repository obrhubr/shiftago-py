class bcolors:
    OKBLUE = '\033[91m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

def printChar(num):
    if num == 0:
        print(0, end='')
    elif num == 1:
        print(f"{bcolors.OKBLUE}{str(num)}{bcolors.ENDC}", end='')
    elif num == 2:
        print(f"{bcolors.OKGREEN}{str(num)}{bcolors.ENDC}", end='')

def printBoard(board):
    for i in range(7):
        printChar(board[i,0])
        print(' - ', end='')
        printChar(board[i,1])
        print(' - ', end='')
        printChar(board[i,2])
        print(' - ', end='')
        printChar(board[i,3])
        print(' - ', end='')
        printChar(board[i,4])
        print(' - ', end='')
        printChar(board[i,5])
        print(' - ', end='')
        printChar(board[i,6])
        print('')
