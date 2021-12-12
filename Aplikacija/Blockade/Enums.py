from enum import Enum
class FieldType(Enum):
    EMPTY = 0
    X = 1
    O = 2
    VERTICAL_WALL_EMPTY = 3
    HORIZONTAL_WALL_EMPTY = 4
    VERTICAL_WALL_FULL = 5
    HORIZONTAL_WALL_FULL = 6


class PlayStatus(Enum):
    START = 0
    MOVED = 1
    PLACING_WALL = 2
    WALL_PLACED = 3
    

