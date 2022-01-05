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
	

	def getAllPossibleMovementFields(self, type):
		if not self.isFieldForPlayer():
			return []

		row = int(self.i / 2) + 1
		column = int(self.j / 2) + 1

		pawn = Pawn(self.board.getPlayerByType(type), 1, row, column, self.board) # virtuelni pijun - nema ga na tabli, pruza pristup funkcijama klase Pawn
		possible_moves = pawn.getPossibleMoves()

		possible_fields = []
		for potez in possible_moves:
			possible_fields.append(self.board.getFieldByRowAndColumn(potez[0], potez[1]))		
		return possible_fields

	def getNumberOfWallsTouching(self, color):
		touchingNum = 0
		if color == 'p': # horizontalni
			if (self.j < 2 #granica za levu stranu
			or self.board.matrix[self.i - 1][self.j - 1].isWall() # levi gornji
			or self.board.matrix[self.i][self.j - 2].isWall() # levi srednji
			or self.board.matrix[self.i + 1][self.j - 1].isWall()): # levi donji
				touchingNum += 1

			if (self.board.matrix[self.i - 1][self.j + 1].isWall() # srednji gornji
			or self.board.matrix[self.i + 1][self.j + 1].isWall()): # srednji donji
				touchingNum += 1

			if (self.j + 4 >= self.board.matrixColumns #granica za desnu stranu
			or self.board.matrix[self.i - 1][self.j + 3].isWall() # desni gornji
			or self.board.matrix[self.i][self.j + 4].isWall() # desni srednji
			or self.board.matrix[self.i + 1][self.j + 3].isWall()): # desni donji
				touchingNum += 1
	
		elif color == 'z': # vertikalni
			if (self.i < 2 #granica za gornju stranu
			or self.board.matrix[self.i - 1][self.j - 1].isWall() # gornji levi
			or self.board.matrix[self.i - 2][self.j].isWall() # gornji srednji1
			or self.board.matrix[self.i - 1][self.j + 1].isWall()): # gornji desni
				touchingNum += 1

			if (self.board.matrix[self.i + 1][self.j - 1].isWall() # srednji levi
			or self.board.matrix[self.i + 1][self.j + 1].isWall()): # srednji desni
				touchingNum += 1

			if (self.i + 4 >= self.board.matrixRows #granica za donju stranu
			or self.board.matrix[self.i + 3][self.j - 1].isWall() # donji levi
			or self.board.matrix[self.i + 4][self.j].isWall() # donji srednji
			or self.board.matrix[self.i + 3][self.j + 1].isWall()): # donji desni
				touchingNum += 1

		return touchingNum
