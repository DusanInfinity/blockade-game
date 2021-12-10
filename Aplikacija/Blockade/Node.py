
class Node:
    def __init__(self, x, y, char):
        self.char = char
        self.x = x
        self.y = y

    def isWall(self):
        if self.izgled == '=' or self.izgled == 'ǁ':
            return True

    def setWall(self, pravac):
        if pravac == 'V': # Vodoradno
            self.char = '='
        else: # pravac == 'H'  # Horizontalno 
            self.char = 'ǁ'
        pass
        

    def isPlayerNode(self):
        if self.x % 2 == 1 and self.y % 2 == 1:
            return True
        else:
            return False

    def setPlayer(self, x, y, znak):
        self.char = znak
        self.x = x
        self.y = y
    