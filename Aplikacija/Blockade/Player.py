from typing import Collection
from Field import Field
from FieldTypes import FieldType
from FieldTypes import PlayStatus


class Player:
    def __init__(self, type, row, column, remainingWalls, board):
        self.type = type
        self.startingRow = row
        self.startingColumn = column
        self.row = row
        self.column = column
        self.board = board
        self.remainingWalls = remainingWalls

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
        if not self.validateMoveForBoardDimensions(x, y):
            print("[GRESKA] Uneta pozicija nije u granicama table!");
            return False
        if not self.validateMoveForWalls(x, y):
            print("[GRESKA] Ne možete pomeriti pijuna na zadatu poziciju zbog zida!");
            return False
        if not self.validateMoveDirection(x, y):
            print("[GRESKA] Ne možete pomeriti pijuna na zadatu poziciju!");
            return False
        self.updatePlayerCoordinates(x, y)
        print(f'Uspešno ste pomerili pijuna na poziciju ({x}, {y}).')
        return True

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

    def play(self):
        # TO-DO biranje pesaka (1 ili 2) - kada se napravi posebna klasa
        status = PlayStatus.START
        while status != PlayStatus.MOVED:
            newPos = self.board.requestInputForPlayerPosition(self.type.name, 1)
            if self.movePlayer(newPos[0], newPos[1]):
                status = PlayStatus.MOVED
                self.board.printTable()
        if self.remainingWalls > 0:
            status = PlayStatus.PLACING_WALL
            while status != PlayStatus.WALL_PLACED:
                newWallPosAndColor = self.board.requestInputForWallPosition(self.type.name)
                color = newWallPosAndColor[0]
                i = newWallPosAndColor[1]
                j = newWallPosAndColor[2]
                if self.board.putWallOnPosition(color, i, j):
                    status = PlayStatus.WALL_PLACED
                    self.board.printTable()
        

