from enum import Enum

class TopType(Enum):
	BOOK = 'book'
	LOSE = 'lose'
	MAGNET = 'magnet'

class CoverSide(Enum):
	EXTERNAL = 'external'
	INTERNAL = 'internal'