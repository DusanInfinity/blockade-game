from Table import Table
from Enums import FieldType

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
			spawn = table.requestInputForPlayerPosition(sign, i)
			players[sign].createPawn(spawn[0], spawn[1])

	print(f'Uneli ste sve parametre, igra počinje!')

	table.printTable()

	currentPlayer = table.playerX
	while(table.isGameFinished() is not True):
		currentPlayer.play()
		currentPlayer = table.playerO if currentPlayer == table.playerX else table.playerX


else:
	t = Table(10, 14)
	wallsNum = 0
	t.printTable()
	t.createPlayers(wallsNum)
	playerX = t.playerX
	playerO = t.playerO
	playerX.createPawn(4, 4)
	playerX.createPawn(7, 4)
	playerO.createPawn(4, 10)
	playerO.createPawn(7, 10)
	t.printTable()
	#t.players[2].movePlayer(7, 4)
	t.printTable()

	currentPlayer = t.playerX
	while(t.isGameFinished() is not True):
		currentPlayer.play()
		currentPlayer = t.playerO if currentPlayer == t.playerX else t.playerX



