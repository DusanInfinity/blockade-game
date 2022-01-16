from Table import Table
from Enums import FieldType
import copy

def requestInputForSign():
	chosenSign = -1
	while(chosenSign != 1 and chosenSign != 2):
		print("1) X\n2) O")
		print("Unesite broj željene oznake: ", end = "")
		unos = input()
		if unos.isnumeric():
			chosenSign = int(unos)
	print("Izabrali ste " + ("X" if chosenSign == 1 else "O") + ".")
	return chosenSign

def requestInputForTableSize():
	n = -1
	m = -1
	while(n < 3 or n > 22 or m < 3 or m > 28):
		if n != -1 and (n < 3 or n > 22):
			print("[GRESKA] Minimalna veličina za n je 3, maksimalna 22. Vi ste uneli: " + str(n))
		if m != -1 and (m < 3 or m > 28): 
			print("[GRESKA] Minimalna veličina za m je 3, maksimalna 28. Vi ste uneli: " + str(m))

		print("Unesite veličinu table [Format: n, m (primer: 11 14)]: ", end = "")
		unos = input().split(" ")
		if len(unos) == 2 and unos[0].isnumeric() and unos[1].isnumeric():
			n = int(unos[0])
			m = int(unos[1])
	print(f'Broj vrsta tabele: {n}, broj kolona: {m}.')
	return (n, m)

def requestInputForWallsNumber():
	wallsNum = -1
	while(wallsNum < 1 or wallsNum > 10):
		if wallsNum != -1 and (wallsNum < 1 or wallsNum > 10):
			print("[GRESKA] Minimalni broj zidova je 1, maksimalni 10. Vi ste uneli: " + str(wallsNum))
		print("Unesite broj zidova po igraču: ", end = "")
		unos = input()
		if unos.isnumeric():
			wallsNum = int(unos)
	print(f'Izabrali ste {wallsNum} zidova po igraču.')
	return wallsNum




debugMode = True

if not debugMode:
	chosenSign = requestInputForSign() # TO-DO nakon aktiviranja igre sa racunarom, uzeti u obzir ovaj unos

	chosenTableSize = requestInputForTableSize()
	n = chosenTableSize[0]
	m = chosenTableSize[1]

	chosenWallsNum = requestInputForWallsNumber() # TO-DO uzeti ovu vrednost i dodati je kod svakog igraca

	table = Table(n, m)
	table.createPlayers(chosenWallsNum)
	players = { 'X': table.playerX, 'O': table.playerO }
	for sign in ['X', 'O']:
		for i in range(2):
			spawn = table.requestInputForPlayerPosition(sign, i+1)
			players[sign].createPawn(spawn[0], spawn[1], i+1)

	print(f'Uneli ste sve parametre, igra počinje!')

	table.printTable()

	currentPlayer = table.playerX
	humanPlayer = table.playerX if chosenSign == 1 else table.playerO
	while(table.isGameFinished() is not True):
		isComputer = True if currentPlayer != humanPlayer else False
		currentPlayer.play(isComputer)
		currentPlayer = table.playerO if currentPlayer == table.playerX else table.playerX


else:
	chosenSign = 2
	table = Table(11, 14)
	wallsNum = 9
	table.printTable()
	table.createPlayers(wallsNum)
	playerX = table.playerX
	playerO = table.playerO
	playerX.createPawn(4, 4, 1)
	playerX.createPawn(8, 4, 2)
	playerO.createPawn(4, 11, 1)
	playerO.createPawn(8, 11, 2)
	table.printTable()
	#t.players[2].movePlayer(7, 4)
	table.printTable()

	#possible_states = t.playerX.getFigureByNumber(1).getAllPossibleNextStates()
	#for i in range(0, len(possible_states)):
	#	print(f'\n\nStanje {i}:')
	#	possible_states[i].printTable()

	#next_state_minmax = table.calculateNextMoveMinMax(3, -999999, 999999, True, 1)
	#next_state_minmax[1].printTable()

	#next_state_minmax = next_state_minmax[1].calculateNextMoveMinMax(2, -999999, 999999, True, 1)
	#next_state_minmax[1].printTable()
	

	currentPlayer = table.playerX
	humanPlayer = table.playerX if chosenSign == 1 else table.playerO
	while(table.isGameFinished() is not True):
		isComputer = True if currentPlayer != humanPlayer else False
		currentPlayer.play(isComputer)
		currentPlayer = table.playerO if currentPlayer == table.playerX else table.playerX


