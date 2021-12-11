from Node import Node


class Player:
    def __init__(self, znak, x, y, board):
        self.znak = znak
        self.x = x
        self.y = y
        self.board = board
        self.zidovi = 0

    def postaviIgracaNaTabli(self, x, y, z = None):
        self.board.board[x * 2][y * 2].setPlayer(x * 2, y * 2, self.znak if z == None else " ")

    def setPlayerCordinates(self, x, y):
        self.postaviIgracaNaTabli(self.x, self.y, '')
        self.x = x
        self.y = y
        self.postaviIgracaNaTabli(self.x, self.y)

    def movePlayer(self, x, y):
        if self.validateMoveForBoardDimensions(x, y) and self.validateMoveForWalls(x, y):
            self.setPlayerCordinates(x, y)
        else:
            pass

    def validateMoveForBoardDimensions(self, x, y):
        if x < 0 or x > self.board.width or y < 0 or y > self.board.length:
            return False
        return True

    def validateMoveDirection(self, x, y):
        pass

    def validateMoveForWalls(self, x, y):
        # Da li su zidovi na putanji ka kojoj zelimo da idemo,
        # Ne mozemo da preskocimo zid
        return True
        pass




class Board:
    def __init__(self, length, width) -> None:
        self.length = length
        self.width = width
        self.board = []
        self.players = []

    def postaviTablu(self):
        for i in range(self.length * 2 - 1):
            self.board.append([])
            for j in range(self.width * 2 - 1):
                if i % 2 == 0:
                    if j % 2 == 1:
                        self.board[i].append(Node(i, j, "|"))
                    else:
                        self.board[i].append(Node(i, j, " "))
                else:
                    if j % 2 == 0:
                        self.board[i].append(Node(i, j, "-"))
                    else:
                        self.board[i].append(Node(i, j, " "))

    def iscrtajTablu(self):
        for i in range(self.length * 2 - 1):
            for j in range(self.width * 2 - 1):
                print(self.board[i][j].char, end="")
            print("")
        print("")

    def postaviIgrace(self):
        self.players.append(Player("X", 3, 3, self))
        self.players.append(Player("X", 7, 3, self))
        self.players.append(Player("O", 3, 10, self))
        self.players.append(Player("O", 7, 10, self))
        for p in self.players:
            p.postaviIgracaNaTabli(p.x, p.y)


board = Board(11, 14)
board.postaviTablu()
board.postaviIgrace()
board.iscrtajTablu()
board.players[1].movePlayer(5, 5)
board.iscrtajTablu()
