from Field import Field
from Enums import FieldType
from Player import Player
from Pawn import Pawn
import copy

class Table:
	fieldMarks = ['1', '2', '3', '4', '5', '6', '7', '8', '9'] + list((chr(i) for i in range(65, 84))) # Brojevi(9) + 17 slova => 28 karaktera

	def __init__(self, n, m):
		self.n = n
		self.m = m
		self.matrixRows = 2*n - 1
		self.matrixColumns = 2*m - 1
		self.matrix = []
		self.initFields()
		self.playerX = None
		self.playerO = None

	def createPlayers(self, wallsNum):
		self.playerX = Player(FieldType.X, wallsNum, self)
		self.playerO = Player(FieldType.O, wallsNum, self)

	def initFields(self):
		for i in range(self.matrixRows):
			self.matrix.append([])
			for j in range(self.matrixColumns):
				if i % 2 == 0:
					if j % 2 == 0:
						self.matrix[i].append(Field(i, j, FieldType.EMPTY, self))
					else:
						self.matrix[i].append(Field(i, j, FieldType.VERTICAL_WALL_EMPTY, self))
				else:
					if j % 2 == 0:
						self.matrix[i].append(Field(i, j, FieldType.HORIZONTAL_WALL_EMPTY, self))
					else:
						self.matrix[i].append(Field(i, j, FieldType.EMPTY, self))

	def printTable(self):
		n = self.n
		m = self.m

		print(*["==" for i in range(self.matrixColumns+4)], sep = "", end = "\n\n")

		print("    ", end = "")
		print(*self.fieldMarks[:m], sep = "   ")

		print("   ", end = "")
		print(*["===" for i in range(m)], sep = " ")

		for row in range(n):
			toPrint = f'{self.fieldMarks[row]} ǁ '

			i = row * 2
			for j in range(self.matrixColumns):
				toPrint += self.matrix[i][j].getSymbol()

			toPrint += f' ǁ {self.fieldMarks[row]}'

			i += 1
			if i < self.matrixRows:
				toPrint += "\n   "
				for j in range(self.matrixColumns):
					toPrint += self.matrix[i][j].getSymbol()
			
			print(toPrint)
			
		print("   ", end = "")
		print(*["===" for i in range(m)], sep = " ")
		print("    ", end = "")
		print(*self.fieldMarks[:m], sep = "   ")
		print(f'\nN = {n}, M = {m}', end = "\n\n")

	def getFieldByRowAndColumn(self, row, column):
		i = (row - 1) * 2
		j = (column - 1) * 2
		return self.matrix[i][j]

	def getFieldsForWall(self, row, column, color):
		row = row - 1
		column = column -1
		if color == 'p':
			if row == 0:
				return None
			try:
				return [self.matrix[row * 2 - 1][column * 2], self.matrix[row * 2 - 1][column * 2 + 2]]
			except:
				return None
		elif color == 'z':
			if column == 0:
				return None
			try:
				return [self.matrix[row * 2][column * 2 + 1], self.matrix[row * 2 + 2][column * 2 + 1]]
			except:
				return None
		else:
			return None

	def placeWallsInFields(self, fields, color):
		for f in fields:
			f.setWall(color)
		
	def putWallOnPosition(self, color, i, j):
		fields = self.getFieldsForWall(i, j, color)
		if fields != None and len(fields) > 0:
			if fields[0].isWall() or fields[1].isWall() or fields[0].areWallsCrossing(color):
				print("[GRESKA] Već postoji zid na toj poziciji!")
			else:
				newState = self.placeWallInNewState(color, i, j)
				# provera da li je put zatvoren
				if newState.isWallClosingPath():
					print("[GRESKA] Zid zatvara put jednom od pijuna!")
					return False
				self.placeWallsInFields(fields, color)
				return True
		else:
			print("[GRESKA] Ne možete postaviti zid na tu poziciju!")
		return False




	def isWallClosingPath(self):
		# za X playera
		for p in self.playerX.pawns:
			playerField = self.getFieldByRowAndColumn(p.row, p.column)
			for ep in self.playerO.pawns:
				if not self.doesPathExistBetweenNodes(playerField, self.getFieldByRowAndColumn(ep.startingRow, ep.startingColumn)):
					return True
		
		# za O playera
		for p in self.playerO.pawns:
			playerField = self.getFieldByRowAndColumn(p.row, p.column)
			for ep in self.playerX.pawns:
				if not self.doesPathExistBetweenNodes(playerField, self.getFieldByRowAndColumn(ep.startingRow, ep.startingColumn)):
					return True
		
		return False


	def doesPathExistBetweenNodes(self, start, end):
		found_end = False
		open_set = set()
		open_set.add(start)
		closed_set = set()
		g = {}
		g[start] = 0
		while len(open_set) > 0 and (not found_end):
			node = None
			for next_node in open_set:
				if node is None or g[next_node] + self.calculateHeuristic(next_node, end) < g[node] + self.calculateHeuristic(node, end):
					node = next_node
			if node == end:
				return True
			for m in node.getAllPossibleMovementFields():			   
				if m not in open_set and m not in closed_set:
					open_set.add(m)
					g[m] = g[node] + 1
				else:
					if g[m] > g[node] + 1:
						g[m] = g[node] + 1
			open_set.remove(node)
			closed_set.add(node)
		return False
	

	def calculateHeuristic(self, node, end):
		return abs(node.i - end.i) + abs(node.j - end.j)



	def isGameFinished(self):
		if self.playerX.isWinner(self.playerO):
			print(f"~~~~~~~~ X is WINNER!! ~~~~~~~~")
			return True
		elif self.playerO.isWinner(self.playerX):
			print(f"~~~~~~~~ O is WINNER!! ~~~~~~~~")
			return True
		return False

	def parseEnteredValueToTableIndex(self, str):
		if str.isnumeric():
			return int(str)
		if len(str) == 1 and str >= 'A' and str <= 'Z':
			return ord(str) - 55; # A - 65, imamo brojeve od 1 do 9, sledeci broj je broj 10(A)
		return -1

	def requestInputForPlayerPosition(self, sign, seqNumber):
		i = -1
		j = -1
		while(i < 1 or i > self.n or j < 1 or j > self.m):
			if i != -1 and (i < 1 or i > self.n):
				print(f'[GRESKA] Minimalna pozicija za vrstu je 1, maksimalna {self.n}. Vi ste uneli: ' + str(i))
			if j != -1 and (j < 1 or j > self.m): 
				print(f'[GRESKA] Minimalna pozicija za kolonu je 1, maksimalna {self.m}. Vi ste uneli: ' + str(j))

			print(f'Unesite poziciju za {seqNumber}. figuru igrača {sign} [Format: vrsta kolona (primer: 3 5)]: ', end = "")
			unos = input().split(" ")
			if len(unos) == 2:
				i = self.parseEnteredValueToTableIndex(unos[0])
				j = self.parseEnteredValueToTableIndex(unos[1])
			
		print(f'[{sign}({seqNumber})] Uneli ste poziciju ({i}, {j}).')
		return (i, j)


	def requestInputForWallPosition(self, sign):
		color = ''
		i = -1
		j = -1
		while(i < 1 or i > self.n or j < 1 or j > self.m or color != 'p' and color != 'z'):
			if color != '' and color != 'p' and color != 'z':
				print(f'[GRESKA] Uneli ste nevalidnu boju za zid. Dozvoljene boje: p(plava) i z(zelena). Vi ste uneli: ' + str(color))
			if i != -1 and (i < 1 or i > self.n):
				print(f'[GRESKA] Minimalna pozicija za vrstu je 1, maksimalna {self.n}. Vi ste uneli: ' + str(i))
			if j != -1 and (j < 1 or j > self.m): 
				print(f'[GRESKA] Minimalna pozicija za kolonu je 1, maksimalna {self.m}. Vi ste uneli: ' + str(j))

			print(f'Unesite poziciju za zid igrača {sign} [Format: boja(p ili z) vrsta kolona (primer: p 6 5)]: ', end = "")
			unos = input().split(" ")
			if len(unos) == 3:
				color = unos[0]
				i = self.parseEnteredValueToTableIndex(unos[1])
				j = self.parseEnteredValueToTableIndex(unos[2])
		print(f'[{sign} - ZID] Uneli ste poziciju ({i}, {j}), boja: {color}')
		return (color, i, j)

	def getPlayerByType(self, type):
		if type == FieldType.X:
			return self.playerX
		else:
			return self.playerO

	def playMoveInNewState(self, playerType, figureNumber, newX, newY):
		newState = copy.deepcopy(self)
		player = newState.getPlayerByType(playerType)
		figure = player.getFigureByNumber(figureNumber)
		figure.updatePawnCoordinates(newX, newY)
		return newState

	def placeWallInNewState(self, color, i, j):
		newState = copy.deepcopy(self)
		fields = newState.getFieldsForWall(i, j, color)
		newState.placeWallsInFields(fields, color)
		return newState

