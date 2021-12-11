from Field import Field
from FieldTypes import FieldType


class Player:
    def __init__(self, type, row, column, board):
        self.type = type
        self.row = row
        self.column = column
        self.board = board
        self.zidovi = 0

    # NAPOMENA: POLJA NA TABLI POCINJU OD 1,1 dok u matrici indeksi pocinju od 0,0
    def setPlayerOnTable(self):
        field = self.board.getFieldByRowAndColumn(self.row, self.column);
        field.changeType(self.type)

    def removePlayerFromCurrentPosition(self):
        field = self.board.getFieldByRowAndColumn(self.row, self.column);
        field.changeType(FieldType.EMPTY)

    # NAPOMENA - ZA DOBRIJA: Ovde sam ostavio x i y jer si mozda radio po koordinatama a ne po vrstama i kolonama
    def updatePlayerCoordinates(self, x, y):
        self.removePlayerFromCurrentPosition() # brisanje igraca sa stare pozicije
        self.row = x
        self.column = y
        self.setPlayerOnTable()

    def movePlayer(self, x, y):
        if self.validateMoveForBoardDimensions(x, y) and self.validateMoveForWalls(x, y):
            self.updatePlayerCoordinates(x, y)
        else:
            pass

    def validateMoveForBoardDimensions(self, x, y):
        if x < 0 or x > self.board.n or y < 0 or y > self.board.m:
            return False
        return True

    def validateMoveDirection(self, x, y):
        pass

    def validateMoveForWalls(self, x, y):
        # Da li su zidovi na putanji ka kojoj zelimo da idemo,
        # Ne mozemo da preskocimo zid
        return True
        pass

    # TO-DO provera da li je igrac pobednik (Kraj je kada je pešak na protivničkom početnom polju)
    def isWinner(self):
        return False;