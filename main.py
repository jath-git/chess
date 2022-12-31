from board import *
from globals import *

def getRowCol():
    read = input()
    if len(read) != 2:
        print('TRY AGAIN: Coordinate must have length of 2')
        return None
    col = read[0]
    row = read[1]

    if ord(col) - ord('A') < 0 or ord(col) - ord('A') > 7:
        print('TRY AGAIN: column must be A - H')
        return None

    if ord(row) - ord('1') < 0 or ord(row) - ord('1') > 7:
        print('TRY AGAIN: column must be 1 - 8')
        return None
    return [ord(read[0]) - ord('A'), ord(read[1]) - ord('1')]

def main():
    board = Board()
    board.move(6, 4, 4, 4)
    board.move(1, 0, 2, 0)
    board.move(7, 3, 5, 5)
    board.move(2, 0, 3, 0)
    board.move(7, 5, 4, 2)
    board.move(3, 0, 4, 0)
    board.move(5, 5, 1, 5)
    print(board.inCheckMate(BLACK))
    board.print()
    return 1
    while True:
        print('------------------BOARD------------------')
        board.print()
        player = 1 if board.toMove == WHITE else 2
        otherPlayer = 1 if player == 2 else 2
        if board.inCheckMate(board.toMove):
            print(f'CHECKMATE: player {otherPlayer} has won')
            break
        if board.inStaleMate(board.toMove):
            print(f'STALEMATE: it is a draw')
            break
        if board.inCheck(board.toMove):
            print(f'CHECK: player {player} move carefully')
        print(f'PLAYER {player}: select piece')
        rowCol = getRowCol()
        if not rowCol:
            continue
        col, row = rowCol
        if not board.arr[row][col]:
            print('TRY AGAIN: no piece in coordinate')
        if board.arr[row][col].colour != board.toMove:
            print(f'TRY AGAIN: not player {player} piece')
        print(f'PLAYER {player}: select destination')
        rowCol = getRowCol()
        if not rowCol:
            continue
        newCol, newRow = rowCol
        if board.move(row, col, newRow, newCol) == ERROR:
            print('TRY AGAIN: not a valid move')
            continue
    return 0

if __name__ == '__main__':
    main()