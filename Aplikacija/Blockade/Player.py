from Node import Node
from FieldTypes import FieldType


class Player:
    def __init__(self, type, row, column, board):
        self.type = type
        self.row = row
        self.column = column
        self.board = board
        self.zidovi = 0

    # NAPOMENA: POLJA NA TABLI POCINJU OD 1,1 dok u matrici indeksi pocinju od 0,0
    def postaviIgracaNaTabli(self):
        row = (self.row - 1) * 2;
        column = (self.column - 1) * 2;
        self.board.matrix[row][column].changeType(self.type)

    def removePlayerFromCurrentPosition(self):
        row = (self.row - 1) * 2;
        column = (self.column - 1) * 2;
        self.board.matrix[row][column].changeType(FieldType.EMPTY)

    # NAPOMENA - ZA DOBRIJA: Ovde sam ostavio x i y jer si mozda radio po koordinatama a ne po vrstama i kolonama
    def setPlayerCordinates(self, x, y):
        self.removePlayerFromCurrentPosition() # brisanje igraca sa stare pozicije
        self.row = y
        self.column = x
        self.postaviIgracaNaTabli()

    def movePlayer(self, x, y):
        if self.validateMoveForBoardDimensions(x, y) and self.validateMoveForWalls(x, y):
            self.setPlayerCordinates(x, y)
        else:
            pass

    def validateMoveForBoardDimensions(self, x, y):
        if x < 0 or x > self.board.m or y < 0 or y > self.board.n:
            return False
        return True

    def validateMoveDirection(self, x, y):
        pass

    def validateMoveForWalls(self, x, y):
        # Da li su zidovi na putanji ka kojoj zelimo da idemo,
        # Ne mozemo da preskocimo zid
        return True
        pass