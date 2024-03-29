from Field import Field
from Enums import FieldType
from Player import Player
from Pawn import Pawn
import copy
import random

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
			if row == 0: #granicni gornji slucaj
				return None
			try:
				return [self.matrix[row * 2 - 1][column * 2], self.matrix[row * 2 - 1][column * 2 + 2]]
			except:
				return None
		elif color == 'z':
			if column == self.m - 1: #granicni desni slucaj
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

	def validateWallPosition(self, color, i, j, fields):
		if fields[0].isWall() or fields[1].isWall() or fields[0].areWallsCrossing(color):
			return False
		if fields[0].getNumberOfWallsTouching(color) >= 2:
			newState = self.placeWallInNewState(color, i, j)
			if newState.isWallClosingPath(): # provera da li je put zatvoren
				return False
		return True
		
	def putWallOnPosition(self, color, i, j):
		fields = self.getFieldsForWall(i, j, color)
		if fields != None and len(fields) > 0:
			if fields[0].isWall() or fields[1].isWall() or fields[0].areWallsCrossing(color):
				print("[GRESKA] Već postoji zid na toj poziciji!")
			else:
				if fields[0].getNumberOfWallsTouching(color) >= 2: 
					newState = self.placeWallInNewState(color, i, j)
					# provera da li je put zatvoren
					if newState.isWallClosingPath():
						print("[GRESKA] Zid zatvara put jednom od pijuna!")
						return False
				self.placeWallsInFields(fields, color)
				print(f'Uspešno ste postavili zid boje \'{color}\' na poziciju ({i}, {j}).')
				return True
		else:
			print("[GRESKA] Ne možete postaviti zid na tu poziciju!")
		return False




	def isWallClosingPath(self):
		# za X playera
		for p in self.playerX.pawns:
			playerField = self.getFieldByRowAndColumn(p.row, p.column)
			for ep in self.playerO.pawns:
				if self.calculateDistanceBetweenNodes(playerField, self.getFieldByRowAndColumn(ep.startingRow, ep.startingColumn)) == -1:
					return True
		
		# za O playera
		for p in self.playerO.pawns:
			playerField = self.getFieldByRowAndColumn(p.row, p.column)
			for ep in self.playerX.pawns:
				if self.calculateDistanceBetweenNodes(playerField, self.getFieldByRowAndColumn(ep.startingRow, ep.startingColumn)) == -1:
					return True
		
		return False


	def calculateDistanceBetweenNodes(self, start, end):
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
				found_end = True
				return g[end]
			for m in node.getAllPossibleMovementFields(start.type): #prenosim type zbog kasnije provere u validateMoveForOtherPawns		   
				if m not in open_set and m not in closed_set:
					open_set.add(m)
					g[m] = g[node] + 1
				else:
					if g[m] > g[node] + 1:
						g[m] = g[node] + 1
			open_set.remove(node)
			closed_set.add(node)
		return -1
	

	def calculateHeuristic(self, node, end): # Manhattan dijagonalna heuristika
		dx = abs(node.i - end.i)
		dy = abs(node.j - end.j)
		return 2 * (dx + dy) - 3 * min(dx, dy); # D = 2(gore/dole/levo/desno), D2 = 1 (dijagonala)


	def getGameWinner(self):
		if self.playerX.isWinner(self.playerO):
			return self.playerX
		elif self.playerO.isWinner(self.playerX):
			return self.playerO
		return None


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

	def calculateNextMoveMinMax(self, depth, alpha, beta, maximizingPlayer, computerPlayer):
		winner = self.getGameWinner()
		if depth == 0 or winner != None:
			heuristic = self.calculateMinMaxHeuristic(winner, depth, computerPlayer)
			return (heuristic, self) # Ovde ide funkcija heuristike
		states = [] 
		out_state = None
		if maximizingPlayer:
			# Izbor maximizing pijuna
			maximizingPawn = None
			maxEval = -999999
			for p in self.playerX.pawns:
				states = p.getAllPossibleNextStates()
				for s in states:
					eval = s.calculateNextMoveMinMax(depth - 1, alpha, beta, False, computerPlayer)
					maxEval = max(maxEval, eval[0])
					if maxEval == eval[0]:
						out_state = copy.deepcopy(s)
						maximizingPawn = p
					alpha = max(alpha, eval[0])
					if beta <= alpha:
						break
			return (maxEval, out_state, maximizingPawn)
		else:
			# Izbor minimizing pijuna
			minEval = 999999
			minimizingPawn = None
			for p in self.playerO.pawns:
				states = p.getAllPossibleNextStates()
				for s in states:
					eval = s.calculateNextMoveMinMax(depth - 1, alpha, beta, True, computerPlayer)
					minEval = min(minEval, eval[0])
					if minEval == eval[0]:
						out_state = copy.deepcopy(s)
						minimizingPawn = p
					beta = min(beta, eval[0])
					if beta <= alpha:
						break
			return (minEval, out_state, minimizingPawn)

	def calculateMinMaxHeuristic(self, winner, depth, computerPlayer):
		heuristic = 0
		if winner == self.playerX:
			heuristic = 9999
			if computerPlayer == True: # computerPlayer = MaximizingPlayer
				heuristic *= (depth + 1)
		elif winner == self.playerO:
			heuristic = -9999
			if computerPlayer == False: # computerPlayer = MinimizingPlayer
				heuristic *= (depth + 1)

		# Maximizing player - X
		for p in self.playerX.pawns:
			playerField = self.getFieldByRowAndColumn(p.row, p.column)
			smallestDistance = 2000
			for ep in self.playerO.pawns:
				distance = self.calculateDistanceBetweenNodes(playerField, self.getFieldByRowAndColumn(ep.startingRow, ep.startingColumn))
				if distance < smallestDistance:
					smallestDistance = distance
			heuristic += 2000/(smallestDistance+2) # smallestDistance moze da bude i 0 ili -1 u slucaju greske, deljenje nulom nije moguce

		# Minimizing player - O
		for p in self.playerO.pawns:
			playerField = self.getFieldByRowAndColumn(p.row, p.column)
			smallestDistance = 2000
			for ep in self.playerX.pawns:
				distance = self.calculateDistanceBetweenNodes(playerField, self.getFieldByRowAndColumn(ep.startingRow, ep.startingColumn))
				if distance < smallestDistance:
					smallestDistance = distance
			heuristic -= 2000/(smallestDistance+2) # smallestDistance moze da bude i 0 ili -1 u slucaju greske, deljenje nulom nije moguce

		return heuristic


	def getPossibleWallPositions(self):
		possible_moves = []

		for color in ['z', 'p']:
			for i in range(1, self.n):
				for j in range(1, self.m):
					wallFields = self.getFieldsForWall(i, j, color)
					if wallFields != None and self.validateWallPosition(color, i, j, wallFields):
						possible_moves.append((color, i, j))

		return possible_moves

	def getAllPossibleWallNextStates(self):
		possible_moves = self.getPossibleWallPositions()
		statesAndMoves = []
		for move in possible_moves:
			color = move[0]
			i = move[1]
			j = move[2]
			statesAndMoves.append((self.placeWallInNewState(color, i, j), move))
		return statesAndMoves


	def chooseNextWallPosition(self, maximizingPlayer):
		statesAndMoves = self.getAllPossibleWallNextStates()
		bestMove = None
		if maximizingPlayer:
			currEval = -999999
			for moveState in statesAndMoves:
				state = moveState[0]
				move = moveState[1]
				heuristic = state.calculateMinMaxHeuristic(None, 0, None)
				if heuristic > currEval:
					currEval = heuristic
					bestMove = move
		else:
			currEval = 999999
			for moveState in statesAndMoves:
				state = moveState[0]
				move = moveState[1]
				heuristic = state.calculateMinMaxHeuristic(None, 0, None)
				if heuristic < currEval:
					currEval = heuristic
					bestMove = move
		return bestMove
