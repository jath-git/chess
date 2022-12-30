from globals import *

class Piece:
    def __init__(self, colour, piece, id):
        self.colour = colour
        self.piece = piece
        self.id = id
        self.moved = False

class ComplexBoard:
    def __init__(self):
        self.arr = [[None for j in range(COLS)] for i in range(ROWS)]
        self.copy = [[None for j in range(COLS)] for i in range(ROWS)]

    def isPiece(self, positions, colour, piece):
        for r, c in positions:
            if r >= 0 and c >= 0 and r < ROWS and c < COLS and self.arr[r][c] and self.arr[r][c].colour != colour and self.arr[r][c].piece == piece:
                return True
        return False

    def place(self, r, c, colour, piece, id):
        self.arr[r][c] = Piece(colour, piece, id)
        pieceSquareMap[colour + piece + str(id)] = [r, c]


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
        if c + 1 < COLS and self.arr[r + movement][c + 1]:
            possible.append([r + movement, c + 1])
        if c - 1 >= 0 and self.arr[r + movement][c - 1]:
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

        return final

    def moveRook(self, r, c, isLast):
        possible = self.moveDirection(r, c, 1, 0, isLast) + self.moveDirection(
            r, c, -1, 0, isLast) + self.moveDirection(r, c, 0, 1, isLast) + self.moveDirection(r, c, 0, -1, isLast)
        return possible

    def moveQueen(self, r, c):
        possible = self.moveRook(r, c, False) + self.moveBishop(r, c, False)
        return possible

    def print(self):
        printType = 'piece'
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