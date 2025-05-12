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
	return f'{prefix}_revestimento {side_name} - tampa livro @{timestamp_str}.svg'

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
	W = cm_to_mm(box.width)
	D = cm_to_mm(box.depth)
	H = cm_to_mm(box.height)
	T = box.thickness
	
	offset_shift = 15
	in_between_spacing = get_in_between_spacing(T)

	file_name = generate_file_name(box.client_name, side)

	full_path = os.path.join(
		os.path.expanduser("~"),
		"Desktop",
		box.client_name.replace(" ", "_"),
		file_name
  )

	if side == CoverSide.EXTERNAL:
		# Cardboard
		x0 = 0 + offset_shift
		y0 = 0 + offset_shift
		x1 = x0 + W + 15
		yA = y0 + H + 10
		yB = yA + in_between_spacing
		yC = yB + D
		yD = yC + in_between_spacing
		yE = yD + H + 10

		#Paper
		x0p = 0
		y0p = 0
		x1p = x1 + offset_shift
		y1p = yE + offset_shift

		total_width = x1p
		total_height = y1p

		dwg = svgwrite.Drawing(
			full_path,
			size=(f"{total_width}mm", f"{total_height}mm"),
			viewBox=f"0 0 {total_width} {total_height}"
		)

		path = dwg.path(
			stroke="black",
			fill="none",
			stroke_width='0.1'
		)

		# ↙️
		path.push("M", x0p, y0 + 10)
		path.push("L", x0 + 10, y0p)

		# ⬇️ + ↘️
		path.push("L", x1 - 10, y0p)
		path.push("L", x1p, y0 + 10)

		# ➡️ + ↗️
		path.push("L", x1p, yE - 10)
		path.push("L", x1 - 10, y1p)

		# ⬆️ + ↖️
		path.push("L", x0 + 10, y1p)
		path.push("L", x0p, yE - 10)

		# ⬅️
		path.push("L", x0p, y0 + 10)

		dwg.add(path)

	else:
		# Cardboard
		x0 = 0 
		y0 = 0
		x1 = x0 + W + 15
		yA = y0 + H + 10
		yB = yA + in_between_spacing
		yC = yB + D
		yD = yC + in_between_spacing
		yE = yD + yA

		#Paper
		x0p = x0 + 15/2
		x1p = x1 - 15/2

		total_width = x1p - x0p
		total_height = H + 36

		dwg = svgwrite.Drawing(
			full_path,
			size=(f"{total_width}mm", f"{total_height}mm"),
			viewBox=f"0 0 {total_width} {total_height}"
		)

		dwg.add(dwg.polyline([
			(0, 0), 
			(total_width, 0), 
			(total_width, total_height), 
			(0, total_height), 
			(0, 0)
		], 
			stroke='black',
			fill="none",
			stroke_width='0.1'
		))
		
	if returning:
		buffer = io.StringIO()
		dwg.write(buffer)

		return ExportBundle(buffer.getvalue(), file_name)
	else:
		dwg.save()