from globals import *

class Piece:
    def __init__(self, colour, piece, id):
        self.colour = colour
        self.piece = piece
        self.id = id
        self.moved = False

class Board:
    def __init__(self):
        self.arr = [[None for j in range(COLS)] for i in range(ROWS)]
        self.copy = [[None for j in range(COLS)] for i in range(ROWS)]
        self.reset()

    def place(self, r, c, colour, piece, id):
        self.arr[r][c] = Piece(colour, piece, id)
        pieceSquareMap[colour + piece + str(id)] = [r, c]

    def reset(self):
        for i in range(COLS):
            self.place(1, i, BLACK, POND, i + 1)
            self.place(6, i, WHITE, POND, i + 1)

        self.place(0, 0, BLACK, ROOK, 1)
        self.place(0, 7, BLACK, ROOK, 2)
        self.place(7, 0, WHITE, ROOK, 1)
        self.place(7, 7, WHITE, ROOK, 2)

        self.place(0, 1, BLACK, KNIGHT, 1)
        self.place(0, 6, BLACK, KNIGHT, 2)
        self.place(7, 1, WHITE, KNIGHT, 1)
        self.place(7, 6, WHITE, KNIGHT, 2)

        self.place(0, 2, BLACK, BISHOP, 1)
        self.place(0, 5, BLACK, BISHOP, 2)
        self.place(7, 2, WHITE, BISHOP, 1)
        self.place(7, 5, WHITE, BISHOP, 2)

        self.place(0, 3, BLACK, QUEEN, 1)
        self.place(7, 3, WHITE, QUEEN, 1)

        self.place(0, 4, BLACK, KING, 1)
        self.place(7, 4, WHITE, KING, 1)

    def move(self, r, c):
        if not self.arr[r][c]:
            return
        
        if self.arr[r][c].piece == KNIGHT:
            self.moveKnight(r, c)
        elif self.arr[r][c].piece == ROOK:
            self.moveRook(r, c)
        elif self.arr[r][c].piece == BISHOP:
            self.moveBishop(r, c)
        elif self.arr[r][c].piece == QUEEN:
            self.moveQueen(r, c)
        elif self.arr[r][c].piece == KING:
            self.moveKing(r, c)
        elif self.arr[r][c].piece == POND:
            #todo: make moved = true
            self.movePond(r, c)

    def moveBishopDirection(self, r, c, movementR, movementC):
        possible = []
        s = r + movementR
        t = c + movementC
        while s >= 0 and t >= 0 and s < ROWS and t < COLS:
            if self.arr[s][t]:
                if self.arr[s][t].colour != self.arr[r][c].colour:
                    possible.append([s, t])
                break
            possible.append([s, t])
            s += movementR
            t += movementC
        return possible

    def moveBishop(self, r, c):
        possible = self.moveBishopDirection(r, c, 1, -1) + self.moveBishopDirection(r, c, -1, 1) + self.moveBishopDirection(r, c, 1, 1) + self.moveBishopDirection(r, c, -1, -1)
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

    def moveKnight(self, r, c):
        possible = []
        possible.append([r - 1, c - 2])
        possible.append([r - 1, c + 2])
        possible.append([r + 1, c - 2])
        possible.append([r + 1, c + 2])
        possible.append([r - 2, c - 1])
        possible.append([r - 2, c + 1])
        possible.append([r + 2, c - 1])
        possible.append([r + 2, c + 1])
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


    def moveRook(self, r, c):
        possible = []
        for s in range(c + 1, COLS, 1):
            if self.arr[r][s]:
                if self.arr[r][s].colour != self.arr[r][c].colour:
                    possible.append([r, s])
                break
            possible.append([r, s])
        for s in range(c - 1, -1, -1):
            if self.arr[r][s]:
                if self.arr[r][s].colour != self.arr[r][c].colour:
                    possible.append([r, s])
                break
            possible.append([r, s])
        for s in range(r + 1, ROWS, 1):
            if self.arr[s][c]:
                if self.arr[s][c].colour != self.arr[r][c].colour:
                    possible.append([s, c])
                break
            possible.append([s, c])
        for s in range(r - 1, -1, -1):
            if self.arr[s][c]:
                if self.arr[s][c].colour != self.arr[r][c].colour:
                    possible.append([s, c])
                break
            possible.append([s, c])
        
        return possible

    def moveQueen(self, r, c):
        possible = self.moveRook(r, c) + self.moveBishop(r, c)
        print(possible)
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