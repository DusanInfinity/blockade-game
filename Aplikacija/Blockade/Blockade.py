from Table import Table
from FieldTypes import FieldType

t = Table(10, 14)

t.printTable()
t.createPlayer(FieldType.X, 3, 3);
t.createPlayer(FieldType.X, 7, 3);
t.createPlayer(FieldType.O, 3, 8);
t.createPlayer(FieldType.O, 7, 8);
t.printTable()
t.players[0].movePlayer(4, 4);
t.printTable()