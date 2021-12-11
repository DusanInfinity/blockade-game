from Field import Field
from FieldTypes import FieldType
from Player import Player

class Table:
	fieldMarks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

	def __init__(self, n, m):
		self.n = n;
		self.m = m;
		self.matrixRows = 2*n - 1;
		self.matrixColumns = 2*m - 1;
		self.matrix = [];
		self.initFields();
		self.players = [];

	def initFields(self):
		for i in range(self.matrixRows):
			self.matrix.append([])
			for j in range(self.matrixColumns):
				if i % 2 == 0:
					if j % 2 == 0:
						self.matrix[i].append(Field(i, j, FieldType.EMPTY))
					else:
						self.matrix[i].append(Field(i, j, FieldType.VERTICAL_WALL_EMPTY))
				else:
					if j % 2 == 0:
						self.matrix[i].append(Field(i, j, FieldType.HORIZONTAL_WALL_EMPTY))
					else:
						self.matrix[i].append(Field(i, j, FieldType.EMPTY))

	def printTable(self):
		n = self.n;
		m = self.m;

		print(*["==" for i in range(self.matrixColumns+4)], sep = "", end = "\n\n");

		print("    ", end = "");
		print(*self.fieldMarks[:m], sep = "   ");

		print("   ", end = "");
		print(*["===" for i in range(m)], sep = " ");

		for row in range(n):
			toPrint = f'{self.fieldMarks[row]} ǁ '

			i = row * 2
			for j in range(self.matrixColumns):
				toPrint += self.matrix[i][j].getSymbol();

			toPrint += f' ǁ {self.fieldMarks[row]}';

			i += 1;
			if i < self.matrixRows:
				toPrint += "\n   ";
				for j in range(self.matrixColumns):
					toPrint += self.matrix[i][j].getSymbol();
			
			print(toPrint);
			
		print("   ", end = "");
		print(*["===" for i in range(m)], sep = " ");
		print("    ", end = "");
		print(*self.fieldMarks[:m], sep = "   ");
		print(f'\nN = {n}, M = {m}', end = "\n\n");

	def createPlayer(self, type, row, column):
		newPlayer = Player(type, row, column, self);
		self.players.append(newPlayer)
		newPlayer.setPlayerOnTable()

	def getFieldByRowAndColumn(self, row, column):
		i = (row - 1) * 2;
		j = (column - 1) * 2;
		return self.matrix[i][j];


