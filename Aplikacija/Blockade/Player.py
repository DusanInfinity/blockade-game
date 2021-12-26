from Enums import PlayStatus
from Pawn import Pawn

class Player:
	def __init__(self, type, remainingWalls, board):
		self.type = type
		self.board = board
		self.remainingWalls = remainingWalls
		self.pawns = []

	def createPawn(self, row, column, figureNum):
		newPawn = Pawn(self, figureNum, row, column, self.board)
		self.pawns.append(newPawn)
		newPawn.setPawnOnTable()

	def choosePawn(self):
		chosenPawn = -1
		sign = self.type.name
		while(chosenPawn != 1 and chosenPawn != 2):
			print(f'1) {sign}1\n2) {sign}2')
			print("Unesite broj željenog pijuna: ", end = "")
			unos = input()
			if unos.isnumeric():
				chosenPawn = int(unos)
		print(f'Izabrali ste pijuna {sign}' + ("1" if chosenPawn == 1 else "2") + ".")
		return chosenPawn

	def isWinner(self, enemy):
		for p in self.pawns:
			for ep in enemy.pawns:
				if p.row == ep.startingRow and p.column == ep.startingColumn:
					return True
		return False

	def play(self):
		chosenPawn = self.choosePawn()
		pawn = self.pawns[chosenPawn-1]
		status = PlayStatus.START
		while status != PlayStatus.MOVED:
			newPos = self.board.requestInputForPlayerPosition(self.type.name, chosenPawn)
			if pawn.movePawn(newPos[0], newPos[1]):
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

	def getFigureByNumber(self, num):
		if num == 1:
			return self.pawns[0]
		else:
			return self.pawns[1]