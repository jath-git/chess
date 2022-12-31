from globals import *

class Piece:
    def __init__(self, colour, piece, id):
        self.colour = colour
        self.piece = piece
        self.id = id
        self.movedTime = 0

class Board:
    def __init__(self):
        self.arr = [[None for j in range(COLS)] for i in range(ROWS)]
        self.copy = [[None for j in range(COLS)] for i in range(ROWS)]
        self.piecesMoved = 0
        self.reset()
        self.toMove = WHITE

    def isPiece(self, positions, colour, piece):
        for r, c in positions:
            if r >= 0 and c >= 0 and r < ROWS and c < COLS and self.arr[r][c] and self.arr[r][c].colour != colour and self.arr[r][c].piece == piece:
                return True
        return False

    def place(self, r, c, colour, piece, id):
        self.arr[r][c] = Piece(colour, piece, id)
        pieceSquareMap[colour + piece + str(id)] = [r, c]

    def promote(self, newR, newC, newPiece):
        pieceSquareMap[self.arr[newR][newC].colour + newPiece + str(self.arr[newR][newC].id)] = pieceSquareMap[self.arr[newR][newC].colour + POND + str(self.arr[newR][newC].id)]
        del pieceSquareMap[self.arr[newR][newC].colour + POND + str(self.arr[newR][newC].id)]
        self.arr[newR][newC].piece = newPiece

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
            if self.arr[r][c].movedTime == 0 and not self.arr[r + movement * 2][c]:
                possible.append([r + movement * 2, c])
        if c + 1 < COLS and self.arr[r + movement][c + 1]:
            possible.append([r + movement, c + 1])

        if c - 1 >= 0 and self.arr[r + movement][c - 1]:
            possible.append([r + movement, c - 1])

        #check if buggy
        if c + 1 < COLS and self.arr[r][c + 1] and self.arr[r][c + 1].piece == POND and self.arr[r][c + 1].movedTime == self.piecesMoved:
            possible.append([r + movement, c + 1])
        if c - 1 >= 0 and self.arr[r][c - 1] and self.arr[r][c - 1].piece == POND and self.arr[r][c - 1].movedTime == self.piecesMoved:
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

    def print(self):
        printType = ''
        if printType == 'id':
            for i in range(ROWS):
                for j in range(COLS):
                    self.copy[i][j] = self.arr[i][j].id if self.arr[i][j] else 0
        elif printType == 'colour':
            for i in range(ROWS):
                for j in range(COLS):
                    self.copy[i][j] = self.arr[i][j].colour if self.arr[i][j] else ' '
        else:
            for i in range(ROWS):
                for j in range(COLS):
                    self.copy[i][j] = self.arr[i][j].piece if self.arr[i][j] else ' '

        for i in range(ROWS):
            print(self.copy[i])

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

    def move(self, r, c, newR, newC):
        if not self.arr[r][c] or self.arr[r][c].colour != self.toMove or [newR, newC] not in self.possibleMove(r, c):
            return
        self.piecesMoved += 1

        if self.arr[newR][newC]:
            del pieceSquareMap[self.arr[newR][newC].colour + self.arr[newR][newC].piece + str(self.arr[newR][newC].id)]
            self.arr[newR][newC] = None
        elif self.arr[r][c].piece == POND and c != newC:
            del pieceSquareMap[self.arr[r][newC].colour + self.arr[r][newC].piece + str(self.arr[r][newC].id)]
            self.arr[r][newC] = None

        self.place(newR, newC, self.arr[r][c].colour, self.arr[r][c].piece, self.arr[r][c].id)
        
        if self.arr[newR][newC].piece == POND:
            if newR == 0:
                self.promote(newR, newC, QUEEN)

        if self.arr[newR][newC].piece == KING:
            if newC + 2 == c:
                self.place(newR, 3, self.arr[newR][0].colour, self.arr[newR][0].piece, self.arr[newR][0].id)
                self.arr[newR][0] = None
            elif c + 2 == newC:
                self.place(newR, 5, self.arr[newR][7].colour, self.arr[newR][7].piece, self.arr[newR][7].id)
                self.arr[newR][7] = None


        if (self.arr[newR][newC].piece == POND and abs(r - newR) == 2) or self.arr[newR][newC].piece == KING or self.arr[newR][newC].piece == ROOK:
            self.arr[newR][newC].movedTime = self.piecesMoved
        
        self.arr[r][c] = None
        self.toMove = WHITE if self.toMove == BLACK else BLACK

    def possibleMove(self, r, c):
        if not self.arr[r][c]:
            return
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
        fromColour = self.arr[r][c].colour
        fromPiece = self.arr[r][c].piece
        fromId = self.arr[r][c].id
        for newR, newC in possible:
            taken = self.arr[newR][newC]
            self.place(newR, newC, fromColour, fromPiece, fromId)
            self.arr[r][c] = None
            if taken:
                del pieceSquareMap[taken.colour + taken.piece + str(taken.id)]

            if not self.inCheck(colour):
                final.append([newR, newC])

            self.place(r, c, fromColour, fromPiece, fromId)
            if taken:
                self.place(newR, newC, taken.colour, taken.piece, taken.id)
            else:
                self.arr[newR][newC] = None
        
        return final

    def inCheck(self, colour):
        kingRow, kingCol = pieceSquareMap.get(colour + KING + str(0))
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
        for key in pieceSquareMap:
            if key[0] == colour:
                r, c = pieceSquareMap[key]
                if self.possibleMove(r, c) != []:
                    return False
        return True

    def inCheckMate(self, colour):
        return self.inCheck(colour) and self.inStaleMate(colour)
