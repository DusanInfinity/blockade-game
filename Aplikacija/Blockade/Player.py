
class Player:
    def __init__(self, znak, x, y, board):
        self.znak = znak
        self.x = x
        self.y = y
        self.board = board
        self.zidovi = 0

    def setPlayer(self, x, y):
        self.x = x
        self.y = y

    def movePlayer(self, x, y):
        if self.validateMoveForDimensions(x, y) and self.validateMoveForWalls(x, y):
            self.setPlayer(x, y)
        else:
            pass

    def validateMoveForDimensions(self, x, y):
        if not (x < 0 or x > self.board.X or y < 0 or y > self.board.Y):
            return False
        return True

    def validateMoveForWalls(self, x, y):
        # Da li su zidovi na putanji ka kojoj zelimo da idemo,
        # Ne mozemo da preskocimo zid
        pass

    