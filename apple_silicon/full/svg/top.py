import svgwrite
from enum import Enum
from datetime import datetime

#from svg.types.lose import export as export_lose
from svg.types.book import export as export_book
from svg.types.magnet import export as export_magnet

class TopType(Enum):
	BOOK = 'book'
	LOSE = 'lose'
	MAGNET = 'magnet'

def generate_file_name(prefix, type):
	if type == TopType.MAGNET:
		name = 'ima'
	elif type == TopType.BOOK:
		name = 'livro'
	else:
		name = 'solta'

	timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
	return f'{prefix}_tampa_{name}@{timestamp_str}.svg'

def export(
	file_name, 
	width, 
	height, 
	depth, 
	thickness,
	type: TopType
):
	name = generate_file_name(file_name, type)

	if type == TopType.BOOK:
		export_book(
			name, 
			width,
			height,
			depth
		)
	else:
		export_magnet(
            name,
            width,
            height,
            depth
        )
