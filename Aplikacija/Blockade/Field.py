from Enums import FieldType

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
			print("Vec posotoji zid na ovoj poziciji")
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
	