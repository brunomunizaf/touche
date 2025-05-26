import os
import io
import svgwrite

from datetime import datetime
from models import Box, ExportBundle

def get_magnets_x(x0, x1, W):
	if 150 <= W <= 200:
		xL = x0 + 30
		xR = x1 - 30
	elif 200 < W <= 300:
		xL = x0 + 40
		xR = x1 - 40
	else:
		xL = x0 + 45
		xR = x1 - 45
	return xL, xR

def generate_file_name(prefix):
	timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
	return f'{prefix}_papelao - tampa ima @{timestamp_str}.svg'

def cm_to_mm(number):
	return number * 10

def get_in_between_spacing(thickness):
	if thickness >= 1.5 and thickness <= 2:
		return 6
	else:
		return 8

def draw_magnet(
	x, 
	y, 
	radius, 
	dwg,
	stroke='black'
):
 dwg.add(dwg.circle(
		center=(x, y), 
		r=radius, 
		fill="none",
		stroke="black",
		stroke_width=0.1
	))

def draw_rectangle(
	x0, 
	x1, 
	y0, 
	y1, 
	dwg, 
	stroke='black'
):
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

def export(
	box: Box,
	returning=False
):
	W = cm_to_mm(box.width)
	D = cm_to_mm(box.depth)
	H = cm_to_mm(box.height)
	T = box.thickness
	
	in_between_spacing = get_in_between_spacing(T)
	magnet_radius = 7

	clearance = 15

	x0 = 0
	y0 = 0
	x1 = x0 + W + clearance
	yA = y0 + D - 5
	yB = yA + in_between_spacing
	yC = yB + H
	yD = yC + in_between_spacing
	yE = yD + D
	yF = yE + in_between_spacing
	yG = yF + H + 7

	xL = x0 + (x1 - x0) / 4
	xR = x1 - (x1 - x0) / 4

	total_width = x1 - x0
	total_height = yG

	file_name = generate_file_name(box.client_name)

	full_path = os.path.join(
		os.path.expanduser("~"),
		"Desktop",
		box.client_name.replace(" ", "_"),
		file_name
  )

	dwg = svgwrite.Drawing(
		full_path,
		size=(f"{total_width}mm", f"{total_height}mm"),
		viewBox=f"0 0 {total_width} {total_height}"
	)

	draw_rectangle(x0, x1, y0, yA, dwg)
	draw_rectangle(x0, x1, yB, yC, dwg)
	draw_rectangle(x0, x1, yD, yE, dwg)
	draw_rectangle(x0, x1, yF, yG, dwg)

	correction = 5 # Altura da língua == D - 5

	if D >= 100:
		yM = y0 + 30 - correction
	else:
		yM = y0 + (D / 2) - correction

	if W + clearance > 100:
		xLM, xRM = get_magnets_x(x0 + (clearance/2), x1 - (clearance/2), W)
		draw_magnet(xLM, yM, magnet_radius, dwg)
		draw_magnet(xRM, yM, magnet_radius, dwg)
	else:
		xM = x0 + (x1 - x0) / 2
		draw_magnet(xM, yM, magnet_radius, dwg)

	if returning:
		buffer = io.StringIO()
		dwg.write(buffer)

		return ExportBundle(buffer.getvalue(), file_name)
	else:
		dwg.save()