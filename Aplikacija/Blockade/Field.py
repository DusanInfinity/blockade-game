from Enums import FieldType
from Pawn import Pawn

class Field:
	def __init__(self, i, j, type, board):
		self.type = type
		self.i = i
		self.j = j
		self.board = board

	def getSymbol(self):
		type = self.type
		return "X" if type == FieldType.X else "O" if type == FieldType.O else " | " if type == FieldType.VERTICAL_WALL_EMPTY else "---" if type == FieldType.HORIZONTAL_WALL_EMPTY else " ǁ " if type == FieldType.VERTICAL_WALL_FULL else "===" if type == FieldType.HORIZONTAL_WALL_FULL else " ";

	def isEmptyWallField(self):
		if self.type == FieldType.HORIZONTAL_WALL_EMPTY or self.type == FieldType.VERTICAL_WALL_EMPTY:
			return True
		return False

	def isWall(self):
		if self.type == FieldType.HORIZONTAL_WALL_FULL or self.type == FieldType.VERTICAL_WALL_FULL:
			return True
		return False

	def setWall(self, boja):
		#treba provera da se uradi da li se prolazi kroz zid

		if self.isWall():
			print("[GRESKA] Već posotoji zid na ovoj poziciji")
		else:
			if boja == 'p': # Plavo - horizonalno
				self.type = FieldType.HORIZONTAL_WALL_FULL
			else: # pravac == 'Z'  # Zeleno - vertikalno
				self.type = FieldType.VERTICAL_WALL_FULL
	
	def areWallsCrossing(self, color):
		if color == 'p':
			if (self.board.matrix[self.i - 1][self.j + 1].isWall() 
			and self.board.matrix[self.i + 1][self.j + 1].isWall()):
				return True
			else:
				return False
		else:
			if (self.board.matrix[self.i + 1][self.j - 1].isWall() 
			and self.board.matrix[self.i + 1][self.j + 1].isWall()):
				return True
			else:
				return False

	def isFieldForPlayer(self):
		if self.i % 2 == 0 and self.j % 2 == 0:
			return True
		else:
			return False

	def changeType(self, type):
		self.type = type
	

	def possibleMoves(self):
		if not self.isFieldForPlayer():
			return []
		row = int(self.i / 2) + 1
		column = int(self.j / 2) + 1

		pawn = Pawn(None, 1, row, column, self.board)
		moguci_potezi = []
		# W A S D
		niz_HV = [(-1, 0), (-2, 0), (1, 0), (2, 0), (0, -1), (0, -2), (0, 1), (0, 2)]
		# WA WD SA SD
		niz_dijagonalno = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

		kombinacija_poteza = niz_HV + niz_dijagonalno
		for potez in kombinacija_poteza:
			if pawn.validateMove(row + potez[0], column + potez[1]):
				moguci_potezi.append(self.board.getFieldByRowAndColumn(row + potez[0], column + potez[1]))
		return moguci_potezi