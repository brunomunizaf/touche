import os
import svgwrite

from models import Box
from enums import CoverSide
from datetime import datetime

def generate_file_name(prefix):
	timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
	return f'{prefix}_papel - tampa ima @{timestamp_str}.svg'

def cm_to_mm(number):
	return number * 10

def get_in_between_spacing(thickness):
	if thickness >= 1.5 and thickness <= 2:
		return 6
	else:
		return 8

def export(box: Box, side: CoverSide):
	W = cm_to_mm(box.width)
	D = cm_to_mm(box.depth)
	H = cm_to_mm(box.height)
	T = box.thickness
	
	offset_shift = 15
	in_between_spacing = get_in_between_spacing(T)

	if side == CoverSide.EXTERNAL:
		# Cardboard
		x0 = 0 + offset_shift
		y0 = 0 + offset_shift
		x1 = x0 + W + 15
		yA = y0 + D - 5
		yB = yA + in_between_spacing
		yC = yB + H
		yD = yC + in_between_spacing
		yE = yD + D
		yF = yE + in_between_spacing
		yG = yF + H + 10

		#Paper
		x0p = 0
		y0p = 0
		x1p = x1 + offset_shift
		y1p = yG + offset_shift

		total_width = x1p
		total_height = y1p

		full_path = os.path.join(
			os.path.expanduser("~"),
			"Desktop",
			box.client_name.replace(" ", "_"),
			generate_file_name(box.client_name)
  	)

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
		path.push("L", x1p, yG - 10)
		path.push("L", x1 - 10, y1p)

		# ⬆️ + ↖️
		path.push("L", x0 + 10, y1p)
		path.push("L", x0p, yG - 10)

		# ⬅️
		path.push("L", x0p, y0 + 10)

		dwg.add(path)
		dwg.save()

	else:
		# Cardboard
		x0 = 0
		y0 = 0
		x1 = x0 + W + 15
		yA = y0 + D - 5
		yB = yA + in_between_spacing
		yC = yB + H
		yD = yC + in_between_spacing
		yE = yD + D
		yF = yE + in_between_spacing
		yG = yF + H + 10

		#Paper
		x0p = x0 + 15/2
		x1p = x1 - 15/2

		total_width = x1p - x0p
		total_height = yC + 42

		full_path = os.path.join(
			os.path.expanduser("~"),
			"Desktop",
			box.client_name.replace(" ", "_"),
			generate_file_name(box.client_name)
  	)

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
		dwg.save()