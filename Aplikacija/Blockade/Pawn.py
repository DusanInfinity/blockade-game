from typing import Collection
from Enums import FieldType
import copy


class Pawn:
    def __init__(self, player, figureNumber, row, column, board):
        self.player = player
        self.figureNum = figureNumber
        self.startingRow = row
        self.startingColumn = column
        self.row = row
        self.column = column
        self.board = board

    # NAPOMENA: POLJA NA TABLI POCINJU OD 1,1 dok u matrici indeksi pocinju od 0,0
    def setPawnOnTable(self):
        field = self.board.getFieldByRowAndColumn(self.row, self.column)
        field.changeType(self.player.type)

    def removePawnFromCurrentPosition(self):
        field = self.board.getFieldByRowAndColumn(self.row, self.column)
        field.changeType(FieldType.EMPTY)

    # NAPOMENA - ZA DOBRIJA: Ovde sam ostavio x i y jer si mozda radio po koordinatama a ne po vrstama i kolonama
    def updatePawnCoordinates(self, x, y):
        self.removePawnFromCurrentPosition()  # brisanje igraca sa stare pozicije
        self.row = x
        self.column = y
        self.setPawnOnTable()


    # TO-DO ovo je losa praksa, dve funkcije rade istu stvar, mozemo da zaboravimo neku proveru u nekoj
    def validateMove(self, x, y): # bez printa
        if x < 1 or x > self.board.n: #[GRESKA] Minimalna pozicija za vrstu je 1, maksimalna {self.board.n}. Vi ste uneli: ' + str(i))
            return False
        if y < 1 or y > self.board.m: #[GRESKA] Minimalna pozicija za kolonu je 1, maksimalna {self.board.m}. Vi ste uneli: ' + str(j))
            return False
        if (not self.validateMoveForWalls(x, y) or
            not self.validateMoveDirection(x, y) or
            not self.validateMoveForBoardDimensions(x, y) or
            not self.validateMoveForOtherPawns(x, y)):
            return False
        return True

    def movePawn(self, x, y):
        if x < 1 or x > self.board.n:
            print(f'[GRESKA] Minimalna pozicija za vrstu je 1, maksimalna {self.board.n}!')
            return False
        if y < 1 or y > self.board.m:
            print(f'[GRESKA] Minimalna pozicija za kolonu je 1, maksimalna {self.board.m}!')
            return False
        if not self.validateMoveForBoardDimensions(x, y):
            print("[GRESKA] Uneta pozicija nije u granicama table!")
            return False
        if not self.validateMoveDirection(x, y):
            print("[GRESKA] Ne možete pomeriti pijuna na zadatu poziciju!")
            return False
        if not self.validateMoveForOtherPawns(x, y):
            print("[GRESKA] Na unetoj poziciji se već nalazi pijun!")
            return False
        if not self.validateMoveForWalls(x, y):
            print("[GRESKA] Ne možete pomeriti pijuna na zadatu poziciju zbog zida!")
            return False
        self.updatePawnCoordinates(x, y)
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
        matrixI = (self.row - 1) * 2
        matrixJ = (self.column - 1) * 2
        if self.row == x or self.column == y: # AKO IDE GORE DOLE LEVO DESNO
            if abs(self.row - x) > 0: # razlika izmedju ta dva argumenta mora da bude 2 ili 0
                if self.row < x: # treba da ide dole
                    if (self.board.matrix[matrixI + 1][matrixJ].isWall()
                        or ((abs(self.row - x) == 2) and self.board.matrix[self.row * 2 + 1][matrixJ].isWall())
                    ):
                        return False
                    else:
                        return True
                elif self.row > x: # treba da ide gore
                    if (self.board.matrix[matrixI - 1][matrixJ].isWall()
                        or ((abs(self.row - x) == 2) and self.board.matrix[(self.row - 2) * 2 - 1][matrixJ].isWall())
                    ):
                        return False
                    else:
                        return True
            elif abs(self.column - y) > 0:
                if self.column < y: # treba da ide desno
                    if (self.board.matrix[matrixI][matrixJ + 1].isWall()
                        or ((abs(self.column - y) == 2) and self.board.matrix[matrixI][self.column * 2 + 1].isWall())
                    ):
                        return False
                    else:
                        return True
                elif self.column > y: # treba da ide levo
                    if (self.board.matrix[matrixI][matrixJ - 1].isWall() 
                        or ((abs(self.column - y) == 2) and self.board.matrix[matrixI][(self.column - 2) * 2 - 1].isWall())
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
        matrixI = (x - 1) * 2
        matrixJ = (y - 1) * 2
        if self.board.matrix[matrixI - 1][matrixJ].isWall() and self.board.matrix[matrixI][matrixJ - 1].isWall(): # gore i levo
            return True
        if self.board.matrix[matrixI - 1][matrixJ - 2].isWall() and self.board.matrix[matrixI - 2][matrixJ - 1].isWall(): # gore-levo i gore-gore
            return True
        if self.board.matrix[matrixI][matrixJ - 1].isWall() and self.board.matrix[matrixI - 2][matrixJ - 1].isWall(): # levo i gore-gore
            return True
        if self.board.matrix[matrixI - 1][matrixJ].isWall() and self.board.matrix[matrixI - 1][matrixJ - 2].isWall(): # gore i gore-levo
            return True

        return False


    def diagonalMoveUpRight(self, x, y):
        matrixI = (x - 1) * 2
        matrixJ = (y - 1) * 2
        if self.board.matrix[matrixI - 1][matrixJ].isWall() and self.board.matrix[matrixI][matrixJ + 1].isWall(): # gore i desno
            return True
        if self.board.matrix[matrixI - 1][matrixJ + 2].isWall() and self.board.matrix[matrixI - 2][matrixJ + 1].isWall(): # gore-desno i gore-gore
            return True
        if self.board.matrix[matrixI - 1][matrixJ].isWall() and self.board.matrix[matrixI - 1][matrixJ + 2].isWall(): # gore i gore-desno
            return True
        if self.board.matrix[matrixI - 2][matrixJ + 1].isWall() and self.board.matrix[matrixI][matrixJ + 1].isWall(): # gore-gore i desno
            return True

        return False

    def diagonalMoveDownLeft(self, x, y):
        matrixI = (x - 1) * 2
        matrixJ = (y - 1) * 2
        if self.board.matrix[matrixI][matrixJ - 1].isWall() and self.board.matrix[matrixI + 1][matrixJ].isWall(): # levo i dole
            return True
        if self.board.matrix[matrixI + 1][matrixJ - 2].isWall() and self.board.matrix[matrixI + 2][matrixJ - 1].isWall(): # dole-levo i dole-dole
            return True
        if self.board.matrix[matrixI + 1][matrixJ - 2].isWall() and self.board.matrix[matrixI + 1][matrixJ].isWall(): #dole-levo i dole
            return True
        if self.board.matrix[matrixI][matrixJ - 1].isWall() and self.board.matrix[matrixI + 2][matrixJ - 1].isWall(): # levo i dole-dole
            return True

        return False
    
    def diagonalMoveDownRight(self, x, y):
        matrixI = (x - 1) * 2
        matrixJ = (y - 1) * 2
        if self.board.matrix[matrixI + 1][matrixJ].isWall() and self.board.matrix[matrixI][matrixJ + 1].isWall(): # dole i desno
            return True
        if self.board.matrix[matrixI + 2][matrixJ + 1].isWall() and self.board.matrix[matrixI + 1][matrixJ + 2].isWall(): # dole-dole i dole-desno
            return True
        if self.board.matrix[matrixI + 1][matrixJ].isWall() and self.board.matrix[matrixI + 1][matrixJ + 2].isWall(): # dole i dole-desno 
            return True
        if self.board.matrix[matrixI][matrixJ + 1].isWall() and self.board.matrix[matrixI + 2][matrixJ + 1].isWall(): # desno i dole-dole
            return True

        return False
    

    def validateMoveForOtherPawns(self, x, y):
        enemy = self.board.playerO if self.player == self.board.playerX else self.board.playerX
        for p in enemy.pawns:
            if x == p.startingRow and y == p.startingColumn: 
                # moze da ode na to polje zato sto je to zavrsno polje i ignorisace tog igraca
                return True
            if x == p.row and y == p.column:
                return False
        
        return True
 
    def getPossibleMoves(self):
        possible_moves = []

        hv = [(-1, 0), (-2, 0), (1, 0), (2, 0), (0, -1), (0, -2), (0, 1), (0, 2)]
        diagonal = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves = hv + diagonal

        for move in moves:
            if self.validateMove(self.row + move[0], self.column + move[1]):
                possible_moves.append(move)
        return possible_moves

    def getAllPossibleNextStates(self):
        possible_moves = self.getPossibleMoves()
        states = []
        for move in possible_moves:
            x = self.row + move[0]
            y = self.column + move[1]
            states.append(self.board.playMove(self.player.type, self.figureNum, x, y))
        return states
