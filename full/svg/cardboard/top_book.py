import os
import svgwrite

from models import Box
from datetime import datetime

def generate_file_name(prefix):
	timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
	return f'{prefix}_papelao - tampa livro @{timestamp_str}.svg'

def cm_to_mm(number):
	return number * 10

def get_in_between_spacing(thickness):
	if thickness >= 1.5 and thickness <= 2:
		return 6
	else:
		return 8

def draw_rectangle(x0, x1, y0, y1, dwg, stroke='black'):
	dwg.add(dwg.polyline([
		(x0, y0), 
		(x1, y0), 
		(x1, y1), 
		(x0, y1), 
		(x0, y0)
	], 
		stroke=stroke,
		fill="none",
		stroke_width='0.1'
	))

def export(box: Box):
	W = cm_to_mm(box.width)
	D = cm_to_mm(box.depth)
	H = cm_to_mm(box.height)
	T = box.thickness

	in_between_spacing = get_in_between_spacing(T)

	x0 = 0
	y0 = 0
	x1 = x0 + W + 15
	yA = y0 + H + 10
	yB = yA + in_between_spacing
	yC = yB + D
	yD = yC + in_between_spacing
	yE = yD + yA

	total_width = x1 - x0
	total_height = yE

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

	draw_rectangle(x0, x1, y0, yA, dwg)
	draw_rectangle(x0, x1, yB, yC, dwg)
	draw_rectangle(x0, x1, yD, yE, dwg)

	dwg.save()