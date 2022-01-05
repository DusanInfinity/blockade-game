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



    def movePawn(self, x, y):
        if x == self.row and y == self.column:
            print(f'[GRESKA] Pijun se već nalazi na unetoj poziciji!')
            return False
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
            if self.validateMoveForOneFieldMove(x, y): # slucaj za potez za jedno polje, pritom da je to ciljno polje
                self.updatePawnCoordinates(x, y)
                return True
            print("[GRESKA] Nevalidne kordinate nove pozicije. Možete ići 2 polja horizontalno ili vertikalno i 1 polje dijagonalno!")
            return False
        if self.validateMoveDirection(x, y):
            if self.validateMoveForOneFieldMove(self.row + (x - self.row) // 2, self.column + (y - self.column) // 2): # slucaj za potez za dva polja, pritom da je ciljno polje izmedju sadasnjeg i poteza koji odaberemo
                self.updatePawnCoordinates(self.row + (x - self.row) // 2, self.column + (y - self.column) // 2)
                return True
        if not self.validateMoveForWalls(x, y):
            print("[GRESKA] Ne možete pomeriti pijuna na zadatu poziciju zbog zida!")
            return False
        if not self.validateMoveForOtherPawns(x, y):
            print("[GRESKA] Na unetoj poziciji se već nalazi pijun!")
            if self.row == x or self.column == y: # samo ako ide W A S D, treba da se radi provera
                if not self.validateMoveIfPawnOnNeighborField(x, y): #proverava susedno polje daa li moze da stavi pijuna
                    self.updatePawnCoordinates(self.row + (x - self.row) // 2, self.column + (y - self.column) // 2)
                    print(f'Uspešno ste pomerili pijuna na poziciju ({self.row}, {self.column}).')
                    return True
                print("[GRESKA] Pijun se ne može pomeriti za jedno polje jer se tu nalazi pijun!")
            return False
        self.updatePawnCoordinates(x, y)
        print(f'Uspešno ste pomerili pijuna na poziciju ({x}, {y}).')
        return True

  

    def validateMoveForBoardDimensions(self, x, y):
        if x < 1 or x > self.board.n or y < 1 or y > self.board.m:
            return False
        return True


    def validateMoveForOneFieldMove(self, x, y):
        if self.row == x or self.column == y:
            if abs(self.row - x) + abs(self.column - y) == 1:
                all_pawns = self.board.playerO.pawns + self.board.playerX.pawns
                for p in all_pawns:
                    if p.player.type != self.player.type and x == p.startingRow and y == p.startingColumn: # ako je krajnje polje
                        if self.validateMoveForWalls(x, y):
                            return True
            else:
                return False

    def validateMoveDirection(self, x, y):
        # za W A S D
        if self.row == x or self.column == y:
            if abs(self.row - x) + abs(self.column - y) == 2:
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
        all_pawns = self.board.playerO.pawns + self.board.playerX.pawns
        for p in all_pawns:
            if p.player.type != self.player.type and x == p.startingRow and y == p.startingColumn: 
                # moze da ode na to polje zato sto je to zavrsno polje i ignorisace tog igraca
                return True
            if x == p.row and y == p.column:
                # kad je drugi igrac na tom polju, treba da se pawn prebaci na polje izmedju sadasnjeg i odredisnog
                return False
        return True

    def validateMoveIfPawnOnNeighborField(self, x, y):
        all_pawns = self.board.playerO.pawns + self.board.playerX.pawns
        for p in all_pawns:
            if self.row + (x - self.row) // 2 == p.row and self.column + (y - self.column) // 2 == p.column:
                return True
        return False
 


    
    def validateMove(self, x, y): # bez printa
        if x == self.row and y == self.column:
            return False
        if x < 1 or x > self.board.n: #[GRESKA] Minimalna pozicija za vrstu je 1, maksimalna {self.board.n}. Vi ste uneli: ' + str(i))
            return False
        if y < 1 or y > self.board.m: #[GRESKA] Minimalna pozicija za kolonu je 1, maksimalna {self.board.m}. Vi ste uneli: ' + str(j))
            return False
        if not self.validateMoveForBoardDimensions(x, y):
            return False
        if not self.validateMoveDirection(x, y):
            if self.validateMoveForOneFieldMove(x, y):
                return True
            return False
        if self.validateMoveDirection(x, y):
            if self.validateMoveForOneFieldMove(self.row + (x - self.row) // 2, self.column + (y - self.column) // 2): # slucaj za potez za dva polja, pritom da je ciljno polje izmedju sadasnjeg i poteza koji odaberemo
                return True
        if not self.validateMoveForWalls(x, y):
            return False
        if not self.validateMoveForOtherPawns(x, y):
            return False
        return True

    def getPossibleMoves(self):
        possible_moves = []

        hv = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        diagonal = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        hv_1 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        moves = hv + diagonal + hv_1


        for move in moves:
            x = move[0] + self.row
            y = move[1] + self.column            
            if self.validateMove(x, y):
                possible_moves.append((x, y))
        return possible_moves

    def getAllPossibleNextStates(self):
        possible_moves = self.getPossibleMoves()
        states = []
        for move in possible_moves:
            x = move[0]
            y = move[1]
            states.append(self.board.playMoveInNewState(self.player.type, self.figureNum, x, y))
        return states
