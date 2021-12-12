from typing import Collection
from Field import Field
from Enums import FieldType
from Enums import PlayStatus


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
            print("[GRESKA] Uneta pozicija nije u granicama table!")
            return False
        if not self.validateMoveDirection(x, y):
            print("[GRESKA] Ne možete pomeriti pijuna na zadatu poziciju!")
            return False
        if not self.validateMoveForOtherPijuns(x, y):
            print("[GRESKA] Na unetoj poziciji se već nalazi pijun!")
            return False
        if not self.validateMoveForWalls(x, y):
            print("[GRESKA] Ne možete pomeriti pijuna na zadatu poziciju zbog zida!")
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
        if self.row == x or self.column == y: # AKO IDE GORE DOLE LEVO DESNO
            if abs(self.row - x) > 0: # razlika izmedju ta dva argumenta mora da bude 2 ili 0
                if self.row < x: # treba da ide dole
                    if (self.board.matrix[(self.row - 1) * 2 + 1][(self.column - 1) * 2].isWall()
                        or self.board.matrix[self.row * 2 + 1][(self.column - 1) * 2].isWall()
                    ):
                        return False
                    else:
                        return True
                elif self.row > x: # treba da ide gore
                    if (self.board.matrix[(self.row - 1) * 2 - 1][(self.column - 1) * 2].isWall()
                        or self.board.matrix[(self.row - 2) * 2 - 1][(self.column - 1) * 2].isWall()
                    ):
                        return False
                    else:
                        return True
            elif abs(self.column - y) > 0:
                if self.column < y: # treba da ide desno
                    if (self.board.matrix[(self.row - 1) * 2][(self.column - 1) * 2 + 1].isWall()
                        or self.board.matrix[(self.row - 1) * 2][self.column * 2 + 1].isWall()
                    ):
                        return False
                    else:
                        return True
                elif self.column > y: # treba da ide levo
                    if (self.board.matrix[(self.row - 1) * 2][(self.column - 1) * 2 - 1].isWall() 
                        or self.board.matrix[(self.row - 1) * 2][(self.column - 2) * 2 - 1].isWall()
                    ):
                        return False
                    else:
                        return True

        elif abs(self.row - x) == abs(self.column - y): # ide dijagonalno
            if self.row > x and self.column > y: # gore-levo
                if self.diagonalMoveUpLeft(self.row, self.column):
                    return False
            elif self.row > x and self.column < y: # gore-desno
                if self.diagonalMoveUpRight(self.row, self.column):
                    return False
            elif self.row < x and self.column > y: # dole-levo
                if self.diagonalMoveDownLeft(self.row, self.column):
                    return False
            elif self.row < x and self.column < y: # dole-desno
                if self.diagonalMoveDownRight(self.row, self.column):
                    return False

        return True

    def diagonalMoveUpLeft(self, x, y):
        if self.board.matrix[(x - 1) * 2 - 1][(y - 1) * 2].isWall() and self.board.matrix[(x - 1) * 2][(y - 1) * 2 - 1].isWall():
            return True
        if self.board.matrix[(x - 1) * 2 - 1][(y - 1) * 2 - 2].isWall() and self.board.matrix[(x - 1) * 2 - 2][(y - 1) * 2 - 1].isWall():
            return True
        if self.board.matrix[(x - 1) * 2][(y - 1) * 2 - 1].isWall() and self.board.matrix[(x - 1) * 2 - 2][(y - 1) * 2 - 1].isWall():
            return True
        if self.board.matrix[(x - 1) * 2 - 1][(y - 1) * 2].isWall() and self.board.matrix[(x - 1) * 2 - 2][(y - 1) * 2].isWall():
            return True

        return False


    def diagonalMoveUpRight(self, x, y):
        if self.board.matrix[(x - 1) * 2 - 1][(y - 1) * 2].isWall() and self.board.matrix[(x - 1) * 2][(y - 1) * 2 + 1].isWall(): # gore i desno
            return True
        if self.board.matrix[(x - 1) * 2 - 1][(y - 1) * 2 - 1 + 2].isWall() and self.board.matrix[(x - 1) * 2 - 2][(y - 1) * 2 + 1].isWall(): # gore-desno i gore-gore
            return True
        if self.board.matrix[(x - 1) * 2 - 1][(y - 1) * 2].isWall() and self.board.matrix[(x - 1) * 2 - 1][(y - 1) * 2 + 2].isWall(): # gore i gore-desno
            return True
        if self.board.matrix[(x - 1) * 2 - 2][(y - 1) * 2 + 1].isWall() and self.board.matrix[(x - 1) * 2][(y - 1) * 2 + 1].isWall(): # gore-gore i desno
            return True

        return False

    def diagonalMoveDownLeft(self, x, y):
        if self.board.matrix[(x - 1) * 2][(y - 1) * 2 - 1].isWall() and self.board.matrix[(x - 1) * 2 + 1][(y - 1) * 2].isWall(): # levo i dole
            return True
        if self.board.matrix[(x - 1) * 2 + 1][(y - 1) * 2 - 2].isWall() and self.board.matrix[(x - 1) * 2 + 2][(y - 1) * 2 - 1].isWall(): # dole-levo i dole-dole
            return True
        if self.board.matrix[(x - 1) * 2 + 1][(y - 1) * 2 - 2].isWall() and self.board.matrix[(x - 1) * 2 + 1][(y - 1) * 2].isWall(): #dole-levo i dole
            return True
        if self.board.matrix[(x - 1) * 2][(y - 1) * 2 - 1].isWall() and self.board.matrix[(x - 1) * 2 + 2][(y - 1) * 2 - 1].isWall(): # levo i dole-dole
            return True

        return False
    
    def diagonalMoveDownRight(self, x, y):
        if self.board.matrix[(x - 1) * 2 + 1][(y - 1) * 2].isWall() and self.board.matrix[(x - 1) * 2][(y - 1) * 2 + 1].isWall(): # dole i desno
            return True
        if self.board.matrix[(x - 1) * 2 + 2][(y - 1) * 2 + 1].isWall() and self.board.matrix[(x - 1) * 2 + 1][(y - 1) * 2 + 2].isWall(): # dole-dole i dole-desno
            return True
        if self.board.matrix[(x - 1) * 2 + 1][(y - 1) * 2].isWall() and self.board.matrix[(x - 1) * 2 + 1][(y - 1) * 2 + 2].isWall(): # dole i dole-desno 
            return True
        if self.board.matrix[(x - 1) * 2][(y - 1) * 2 + 1].isWall() and self.board.matrix[(x - 1) * 2 + 2][(y - 1) * 2 + 1].isWall(): # desno i dole-dole
            return True

        return False
    

    def validateMoveForOtherPijuns(self, x, y):
        for p in self.board.players:
            if self.type != p.type and x == p.startingRow and y == p.startingColumn: 
                # moze da ode na to polje zato sto je to zavrsno polje i ignorisace tog igraca
                return True
            if x == p.row and y == p.column:
                return False
        
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
                    self.remainingWalls -= 1
                    self.board.printTable()
        

