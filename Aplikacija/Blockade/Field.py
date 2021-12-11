from FieldTypes import FieldType

class Field:
	def __init__(self, i, j, type):
		self.type = type
		self.i = i
		self.j = j

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

	def setWall(self, pravac):
		if pravac == 'V': # Vertikalno
			self.type = FieldType.VERTICAL_WALL_FULL;
		else: # pravac == 'H'  # Horizontalno 
			self.type = FieldType.HORIZONTAL_WALL_FULL;
		pass
		

	def isFieldForPlayer(self):
		if self.i % 2 == 0 and self.j % 2 == 0:
			return True
		else:
			return False

	def changeType(self, type):
		self.type = type
	