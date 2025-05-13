import os
import io
import svgwrite

from enums import CoverSide
from datetime import datetime
from models import Box, ExportBundle

def generate_file_name(prefix, side):
	if side == CoverSide.EXTERNAL:
		side_name = 'externo'
	else:
		side_name = 'interno'

	timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
	return f'{prefix}_revestimento {side_name} - tampa solta @{timestamp_str}.svg'

def cm_to_mm(number):
	return number * 10

def get_in_between_spacing(thickness):
	if thickness >= 1.5 and thickness <= 2:
		return 6
	else:
		return 8

def export(
	box: Box, 
	side: CoverSide,
	returning=False
):
	raise NotImplementedError("Exportação de revestimento interno/externo da tampa solta ainda não foi implementada.")
