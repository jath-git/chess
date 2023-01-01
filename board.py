from globals import *


class Piece:
    def __init__(self, colour, piece, id):
        self.colour = colour
        self.piece = piece
        self.id = id
        self.movedTime = 0
        self.moved = False

class Board:
    def __init__(self):
        self.arr = [[None for j in range(COLS)] for i in range(ROWS)]
        self.possible = [[0 for j in range(COLS)] for i in range(ROWS)]
        self.piecesMoved = 0
        self.toMove = WHITE
        self.reset()

    def isPiece(self, positions, colour, piece):
        for r, c in positions:
            if r >= 0 and c >= 0 and r < ROWS and c < COLS and self.arr[r][c] and self.arr[r][c].colour != colour and self.arr[r][c].piece == piece:
                return True
        return False

    def place(self, r, c, colour, piece, id):
        self.arr[r][c] = Piece(colour, piece, id)
        pieceSquareMap[colour + piece + str(id)] = [r, c]

    def promote(self, newR, newC, newPiece):
        self.arr[newR][newC].piece = newPiece
        pieceSquareMap[self.arr[newR][newC].colour +
                       newPiece + str(self.arr[newR][newC].id)] = [newR, newC]
        del pieceSquareMap[self.arr[newR][newC].colour +
                           POND + str(self.arr[newR][newC].id)]

    def moveDirection(self, r, c, movementR, movementC, isLast):
        possible = []
        s = r + movementR
        t = c + movementC
        while s >= 0 and t >= 0 and s < ROWS and t < COLS:
            if self.arr[s][t]:
                if self.arr[s][t].colour != self.arr[r][c].colour:
                    possible.append([s, t])
                break
            if not isLast:
                possible.append([s, t])
            s += movementR
            t += movementC
        return possible

    def moveBishop(self, r, c, isLast):
        possible = self.moveDirection(r, c, 1, -1, isLast) + self.moveDirection(
            r, c, -1, 1, isLast) + self.moveDirection(r, c, 1, 1, isLast) + self.moveDirection(r, c, -1, -1, isLast)
        return possible

    def movePond(self, r, c):
        possible = []
        movement = 1 if self.arr[r][c].colour == BLACK else -1
        if not self.arr[r + movement][c]:
            possible.append([r + movement, c])
            if not self.arr[r][c].moved and not self.arr[r + movement * 2][c]:
                possible.append([r + movement * 2, c])
        if c + 1 < COLS and self.arr[r + movement][c + 1] and self.arr[r + movement][c + 1].colour != self.arr[r][c].colour:
            possible.append([r + movement, c + 1])

        if c - 1 >= 0 and self.arr[r + movement][c - 1] and self.arr[r + movement][c - 1].colour != self.arr[r][c].colour:
            possible.append([r + movement, c - 1])

        # todo: check if buggy
        if c + 1 < COLS and self.arr[r][c + 1] and self.arr[r][c + 1].piece == POND and self.arr[r][c + 1].colour != self.arr[r][c].colour and self.arr[r][c + 1].movedTime == self.piecesMoved:
            possible.append([r + movement, c + 1])
        if c - 1 >= 0 and self.arr[r][c - 1] and self.arr[r][c - 1].piece == POND and self.arr[r][c - 1].colour != self.arr[r][c].colour and self.arr[r][c - 1].movedTime == self.piecesMoved:
            possible.append([r + movement, c - 1])
        return possible

    def permutations(self, arr):
        if len(arr) == 1:
            return [[arr[0]], [- arr[0]]]
        perms = []
        for i in range(len(arr)):
            rest = self.permutations(arr[:i] + arr[i + 1:])
            for j in rest:
                perms.append([arr[i]] + j)
                perms.append([- arr[i]] + j)
        return perms

    def moveKnight(self, r, c):
        possible = self.permutations([1, 2])
        for i in range(len(possible)):
            possible[i][0] += r
            possible[i][1] += c

        final = []
        for p in possible:
            if p[0] >= 0 and p[1] >= 0 and p[0] < ROWS and p[1] < COLS:
                if (not self.arr[p[0]][p[1]] or self.arr[p[0]][p[1]].colour != self.arr[r][c].colour):
                    final.append(p)
        return final

    def moveKing(self, r, c):
        possible = []
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if i == r and j == c:
                    continue
                possible.append([i, j])

        final = []
        for p in possible:
            if p[0] >= 0 and p[1] >= 0 and p[0] < ROWS and p[1] < COLS:
                if (not self.arr[p[0]][p[1]] or self.arr[p[0]][p[1]].colour != self.arr[r][c].colour):
                    final.append(p)

        if self.arr[r][c].movedTime == 0 and not self.inCheck(self.arr[r][c].colour):
            if self.arr[r][0] and self.arr[r][0].piece == ROOK and self.arr[r][0].movedTime == 0 and not self.arr[r][3] and not self.arr[r][2] and not self.arr[r][1]:
                final.append([r, 2])
            if self.arr[r][COLS - 1] and self.arr[r][COLS - 1].piece == ROOK and self.arr[r][COLS - 1].movedTime == 0 and not self.arr[r][6] and not self.arr[r][5]:
                final.append([r, 6])
        return final

    def moveRook(self, r, c, isLast):
        possible = self.moveDirection(r, c, 1, 0, isLast) + self.moveDirection(
            r, c, -1, 0, isLast) + self.moveDirection(r, c, 0, 1, isLast) + self.moveDirection(r, c, 0, -1, isLast)
        return possible

    def moveQueen(self, r, c):
        possible = self.moveRook(r, c, False) + self.moveBishop(r, c, False)
        return possible

    def changeColour(self, colour):
        print(f'{bcolors[colour]}', end='')

    def resetColour(self):
        self.changeColour('WHITE')

    def print(self):
        print('------------------BOARD------------------')
        letterLabel = ' '
        for i in range(COLS):
            letterLabel += '   '
            letterLabel += chr(ord('A') + i)

        self.changeColour('BLUE')
        print(letterLabel)
        print()

        for i in range(ROWS):
            self.changeColour('BLUE')
            print(i + 1, end='')

            for j in range(COLS):
                self.resetColour()
                print(end='   ')
                if self.possible[i][j] != 0:
                    # print(i, j, self.possible[i][j])
                    self.changeColour('GREEN' if self.possible[i][j] == 1 else 'YELLOW')
                    self.possible[i][j] = 0

                if not self.arr[i][j]:
                    print(' ', end='')
                    self.changeColour('DEFAULT')
                    continue
                
                if self.arr[i][j].colour == BLACK:
                    self.changeColour('PURPLE')
                print(self.arr[i][j].piece, end='')
                self.changeColour('DEFAULT')
                self.resetColour()
            print()
            print()

        self.changeColour('BLUE')
        print(letterLabel)
        self.resetColour()
        self.changeColour('DEFAULT')

    def reset(self):
        for i in range(COLS):
            self.place(1, i, BLACK, POND, i + 1)
            self.place(6, i, WHITE, POND, i + 1)

        self.place(0, 0, BLACK, ROOK, 0)
        self.place(0, 7, BLACK, ROOK, 9)
        self.place(COLS - 1, 0, WHITE, ROOK, 0)
        self.place(COLS - 1, COLS - 1, WHITE, ROOK, 9)

        self.place(0, 1, BLACK, KNIGHT, 0)
        self.place(0, 6, BLACK, KNIGHT, 9)
        self.place(COLS - 1, 1, WHITE, KNIGHT, 0)
        self.place(COLS - 1, 6, WHITE, KNIGHT, 9)

        self.place(0, 2, BLACK, BISHOP, 0)
        self.place(0, 5, BLACK, BISHOP, 9)
        self.place(COLS - 1, 2, WHITE, BISHOP, 0)
        self.place(COLS - 1, 5, WHITE, BISHOP, 9)

        self.place(0, 3, BLACK, QUEEN, 0)
        self.place(COLS - 1, 3, WHITE, QUEEN, 0)

        self.place(0, 4, BLACK, KING, 0)
        self.place(COLS - 1, 4, WHITE, KING, 0)

    def whichSpecialCase(self, r, c, newR, newC, current, taken):
        if current.piece == POND and (newR == 0 or newR == 7):
            return POND_PROMOTION
        if current.piece == POND and c != newC and not taken:
            return POND_PASSING
        if current.piece == KING and abs(c - newC) == 2:
            return CASTLE
        return NOT_SPECIAL

    def specialMove(self, r, c, newR, newC, current):
        # print(current.piece, POND, c, newC, self.arr[newR][newC] == None)
        if current.piece == POND and (newR == 0 or newR == 7):
            self.promote(newR, newC, QUEEN)
        elif current.piece == POND and c != newC:
            del pieceSquareMap[self.arr[r][newC].colour + self.arr[r][newC].piece + str(self.arr[r][newC].id)]
            self.arr[r][newC] = None

        if current.piece == KING:
            if newC + 2 == c:
                self.arr[newR][3] = self.arr[newR][0]
                pieceSquareMap[self.arr[newR][0].colour + self.arr[newR]
                               [0].piece + str(self.arr[newR][0].id)] = [newR, 3]
                self.arr[newR][0] = None
            elif c + 2 == newC:
                self.arr[newR][5] = self.arr[newR][7]
                pieceSquareMap[self.arr[newR][7].colour + self.arr[newR]
                               [7].piece + str(self.arr[newR][7].id)] = [newR, 5]
                self.arr[newR][7] = None

    def move(self, r, c, newR, newC):
        if not self.arr[r][c] or self.arr[r][c].colour != self.toMove or [newR, newC] not in self.possibleMove(r, c):
            return ERROR

        self.piecesMoved += 1

        current = self.arr[r][c]
        taken = self.arr[newR][newC]

        if (current.piece == POND and abs(r - newR) == 2) or current.piece == KING or current.piece == ROOK:
            current.movedTime = self.piecesMoved
        current.moved = True
        self.toMove = WHITE if self.toMove == BLACK else BLACK

        self.arr[newR][newC] = current
        pieceSquareMap[current.colour + current.piece +
                       str(current.id)] = [newR, newC]
        self.arr[r][c] = None

        if taken:
            del pieceSquareMap[taken.colour + taken.piece + str(taken.id)]
        if self.whichSpecialCase(r, c, newR, newC, current, taken) != NOT_SPECIAL:
            print(True)
            self.specialMove(r, c, newR, newC, current)
        return SUCCESS

    def possibleMove(self, r, c):
        if not self.arr[r][c]:
            return []

        colour = self.arr[r][c].colour

        possible = []
        if self.arr[r][c].piece == KNIGHT:
            possible = self.moveKnight(r, c)
        elif self.arr[r][c].piece == ROOK:
            possible = self.moveRook(r, c, False)
        elif self.arr[r][c].piece == BISHOP:
            possible = self.moveBishop(r, c, False)
        elif self.arr[r][c].piece == QUEEN:
            possible = self.moveQueen(r, c)
        elif self.arr[r][c].piece == KING:
            possible = self.moveKing(r, c)
        elif self.arr[r][c].piece == POND:
            possible = self.movePond(r, c)

        final = []
        current = self.arr[r][c]
        oldCurrentMoved = current.moved
        oldMovedTime = current.movedTime
        self.piecesMoved += 1
        self.toMove = WHITE if self.toMove == BLACK else BLACK

        for newR, newC in possible:
            if (current.piece == POND and abs(r - newR) == 2) or current.piece == KING or current.piece == ROOK:
                current.movedTime = self.piecesMoved

            taken = self.arr[newR][newC]
            self.arr[newR][newC] = current
            pieceSquareMap[current.colour + current.piece +
                           str(current.id)] = [newR, newC]
            self.arr[r][c] = None
            if taken:
                del pieceSquareMap[taken.colour + taken.piece + str(taken.id)]
            specialCase = self.whichSpecialCase(r, c, newR, newC, current, taken)
            
            specialPond = None
            if specialCase != NOT_SPECIAL:
                specialPond = self.arr[r][newC]
                self.specialMove(r, c, newR, newC, current)

            if not self.inCheck(colour):
                final.append([newR, newC])

            self.arr[newR][newC] = taken
            self.arr[r][c] = current
            pieceSquareMap[current.colour +
                           current.piece + str(current.id)] = [r, c]
            if taken:
                pieceSquareMap[taken.colour + taken.piece +
                               str(taken.id)] = [newR, newC]

            if specialCase == POND_PROMOTION:
                current.piece = POND
            if specialCase == CASTLE:
                if not self.arr[newR][newC - 1]:
                    self.arr[newR][0] = self.arr[newR][newC + 1]
                    self.arr[newR][newC + 1] = None
                    pieceSquareMap[self.arr[newR][0].colour + self.arr[newR]
                                   [0].piece + str(self.arr[newR][0].id)] = [newR, 0]
                else:
                    self.arr[newR][COLS - 1] = self.arr[newR][newC - 1]
                    self.arr[newR][newC - 1] = None
                    pieceSquareMap[self.arr[newR][COLS - 1].colour + self.arr[newR]
                                   [COLS - 1].piece + str(self.arr[newR][COLS - 1].id)] = [newR, COLS - 1]
            if specialCase == POND_PASSING:
                self.arr[r][newC] = specialPond
                pieceSquareMap[specialPond.colour + POND + str(specialPond.id)] = [r, newC]

            current.movedTime = oldMovedTime

        current.moved = oldCurrentMoved
        self.piecesMoved -= 1
        self.toMove = WHITE if self.toMove == BLACK else BLACK
        return final

    def inCheck(self, colour):
        kingRow, kingCol = pieceSquareMap[colour + KING + str(0)]
        pondDirection = 1 if colour == BLACK else -1
        if self.isPiece([[kingRow + pondDirection, kingCol + 1], [kingRow + pondDirection, kingCol - 1]], colour, POND):
            return True

        possible = self.moveKnight(kingRow, kingCol)
        if self.isPiece(possible, colour, KNIGHT):
            return True
        possible = self.moveRook(kingRow, kingCol, True)
        if self.isPiece(possible, colour, ROOK):
            return True
        if self.isPiece(possible, colour, QUEEN):
            return True
        possible = self.moveBishop(kingRow, kingCol, True)
        if self.isPiece(possible, colour, BISHOP):
            return True
        if self.isPiece(possible, colour, QUEEN):
            return True
        return False

    def inStaleMate(self, colour):
        for key in list(pieceSquareMap.keys()):
            if key[0] == colour:
                r, c = pieceSquareMap[key]
                if self.possibleMove(r, c) != []:
                    return False
        return True

    def inCheckMate(self, colour):
        return self.inCheck(colour) and self.inStaleMate(colour)
