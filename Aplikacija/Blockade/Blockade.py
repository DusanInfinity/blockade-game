from Table import Table
from FieldTypes import FieldType

def requestInputForSign():
	chosenSign = -1
	while(chosenSign is not 1 and chosenSign is not 2):
		print("1) X\n2) O");
		print("Unesite broj željene oznake: ", end = "");
		unos = input()
		if unos.isnumeric():
			chosenSign = int(unos)
	print("Izabrali ste " + ("X" if chosenSign == 1 else "O") + ".");
	return chosenSign;

def requestInputForTableSize():
	n = -1;
	m = -1;
	while(n < 3 or n > 15 or m < 3 or m > 15):
		if n != -1 and (n < 3 or n > 15):
			print("[GRESKA] Minimalna veličina za n je 3, maksimalna 15. Vi ste uneli: " + str(n));
		if m != -1 and (m < 3 or m > 15): 
			print("[GRESKA] Minimalna veličina za m je 3, maksimalna 15. Vi ste uneli: " + str(m));

		print("Unesite veličinu table [Format: n, m (primer: 11 14)]: ", end = "");
		unos = input().split(" ")
		if len(unos) == 2 and unos[0].isnumeric() and unos[1].isnumeric():
			n = int(unos[0])
			m = int(unos[1])
	print(f'Broj vrsta tabele: {n}, broj kolona: {m}.');
	return (n, m)

def requestInputForWallsNumber():
	wallsNum = -1
	while(wallsNum < 1 or wallsNum > 10):
		if wallsNum != -1 and (wallsNum < 1 or wallsNum > 10):
			print("[GRESKA] Minimalni broj zidova je 3, maksimalni 10. Vi ste uneli: " + str(wallsNum));
		print("Unesite broj zidova po igraču: ", end = "");
		unos = input()
		if unos.isnumeric():
			wallsNum = int(unos)
	print(f'Izabrali ste {wallsNum} zidova po igraču.');
	return wallsNum;




debugMode = True;

if not debugMode:
	chosenSign = requestInputForSign(); # TO-DO nakon aktiviranja igre sa racunarom, uzeti u obzir ovaj unos

	chosenTableSize = requestInputForTableSize();
	n = chosenTableSize[0];
	m = chosenTableSize[1];

	chosenWallsNum = requestInputForWallsNumber(); # TO-DO uzeti ovu vrednost i dodati je kod svakog igraca

	table = Table(n, m);
	for sign in ['X', 'O']:
		type = FieldType.X if sign is 'X' else FieldType.O;
		for i in range(2):
			spawn = table.requestInputForPosition(sign, i);
			table.createPlayer(type, spawn[0], spawn[1]);

	print(f'Uneli ste sve parametre, igra počinje!');

	table.printTable();

	while(table.isGameFinished() is not True):
		newPosX1 = table.requestInputForPosition('X', 1);
		table.players[0].movePlayer(newPosX1[0], newPosX1[1]);
		table.printTable();


else:
	t = Table(10, 14)

	t.printTable()
	t.createPlayer(FieldType.X, 3, 3);
	t.createPlayer(FieldType.X, 7, 3);
	t.createPlayer(FieldType.O, 3, 8);
	t.createPlayer(FieldType.O, 7, 8);
	t.printTable()
	t.players[0].movePlayer(4, 4);
	t.printTable()

	while(t.isGameFinished() is not True):
		newPosX1 = t.requestInputForPosition('X', 1);
		t.players[0].movePlayer(newPosX1[0], newPosX1[1]);
		t.printTable();



