from FieldTypes import FieldType

class Node:
    def __init__(self, row, column, type):
        self.type = type
        self.row = row
        self.column = column

    def isWall(self):
        if self.type == FieldType.HORIZONTAL_WALL_FULL or self.type == FieldType.VERTICAL_WALL_FULL:
            return True

    def setWall(self, pravac):
        if pravac == 'V': # Vertikalno
            self.type = FieldType.VERTICAL_WALL_FULL;
        else: # pravac == 'H'  # Horizontalno 
            self.type = FieldType.HORIZONTAL_WALL_FULL;
        pass
        

    def isPlayerNode(self):
        if self.row % 2 == 0 and self.column % 2 == 0:
            return True
        else:
            return False

    def changeType(self, type):
        self.type = type
    