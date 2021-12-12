from typing import Collection
from Field import Field
from FieldTypes import FieldType


class Player:
    def __init__(self, type, row, column, board):
        self.type = type
        self.startingRow = row
        self.startingColumn = column
        self.row = row
        self.column = column
        self.board = board
        self.zidovi = 0

    # NAPOMENA: POLJA NA TABLI POCINJU OD 1,1 dok u matrici indeksi pocinju od 0,0
    def setPlayerOnTable(self):
        field = self.board.getFieldByRowAndColumn(self.row, self.column)
        field.changeType(self.type)

    def removePlayerFromCurrentPosition(self):
        field = self.board.getFieldByRowAndColumn(self.row, self.column)
        field.changeType(FieldType.EMPTY)

    # NAPOMENA - ZA DOBRIJA: Ovde sam ostavio x i y jer si mozda radio po koordinatama a ne po vrstama i kolonama
    def updatePlayerCoordinates(self, x, y):
        self.removePlayerFromCurrentPosition()  # brisanje igraca sa stare pozicije
        self.row = x
        self.column = y
        self.setPlayerOnTable()

    def movePlayer(self, x, y):
        if self.validateMoveForBoardDimensions(x, y) and self.validateMoveForWalls(x, y) and self.validateMoveDirection(x, y):
            self.updatePlayerCoordinates(x, y)
        else:
            print("\nPomeranje pijuna nije moguce!\n")

    def validateMoveForBoardDimensions(self, x, y):
        if x < 0 or x > self.board.n or y < 0 or y > self.board.m:
            return False
        return True


    def validateMoveDirection(self, x, y):
        # za W A S D
        if self.row == x or self.column == y:
            if abs(self.row - x) + abs(self.column - y) <= 2:
                return True
            else:
                return False
        
        # WA WD SA SD
        else:
            if abs(self.row - x) == abs(self.column - y) and abs(self.row - x) == 1:
                return True
            else:
                return False
                
    def validateMoveForWalls(self, x, y):
        # Da li su zidovi na putanji ka kojoj zelimo da idemo,
        # Ne mozemo da preskocimo zid
        return True


    def isWinner(self):
        for p in self.board.players:
            if self.type != p.type:
                if self.row == p.startingRow and self.column == p.startingColumn:
                    return True
        return False
