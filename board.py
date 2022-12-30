from globals import *
from complexBoard import ComplexBoard

class Board(ComplexBoard):
    def __init__(self):
        super().__init__()
        self.reset()

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

    def move(self, r, c, newR, newC):
        if [newR, newC] not in self.possibleMove(r, c):
            return

        if self.arr[newR][newC]:
            del pieceSquareMap[self.arr[newR][newC].colour + self.arr[newR][newC].piece + str(self.arr[newR][newC].id)]
            
        self.place(newR, newC, self.arr[r][c].colour, self.arr[r][c].piece, self.arr[r][c].id)
        self.arr[r][c] = None

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
        kingRow, kingCol = pieceSquareMap.get(colour + KING + str(1))
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
