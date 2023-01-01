KING = 'K'
QUEEN = 'Q'
ROOK = 'R'
KNIGHT = 'N'
BISHOP = 'B'
POND = 'P'
WHITE = 'W'
BLACK = 'B'
ERROR = None
SUCCESS = 1
ROWS = 8
COLS = 8
NOT_SPECIAL = 0
POND_PROMOTION = 1
POND_PASSING = 2
CASTLE = 3

bcolors = {
    'BLUE': '\033[94m',
    'PURPLE': '\033[95m',
    'WHITE': '\033[0m',
    'GREEN': '\x1b[6;30;42m',
    'YELLOW': '\x1b[6;30;43m',
    'DEFAULT': '\x1b[0m',
}

pieceSquareMap = {}
