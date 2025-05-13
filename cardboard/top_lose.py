import os
import io
import svgwrite

from datetime import datetime
from models import Box, ExportBundle

def generate_file_name(prefix):
	timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
	return f'{prefix}_papelao - tampa solta @{timestamp_str}.svg'

def cm_to_mm(number):
	return number * 10

def calculate_top_depth(depth_mm):
	if depth_mm <= 50:
		return 15
	elif depth_mm <= 100:
		return 20
	else:
		return 20 + 10 * math.ceil((depth_mm - 100) / 50)

def get_clearance(thickness):
	if thickness in (1.90, 2.00):
		clearance = 7.0
	elif thickness == 2.50:
		clearance = 8.0
	else:
		clearance = thickness * 3
	return clearance

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

def move_to(
	x, 
	y, 
	path
):
	path.push("M", x, y)

def draw_top(
	x0, 
	x1, 
	y1, 
	yT, 
	T, 
	path
):
	move_to(x0, y1, path)	

	xL = x0-T
	yM = y1+(yT-y1)/2
	xR = x1+T

	path.push("L",
		xL, y1,
		xL, yM,
		x0, yM,
		x0, yT,
		x1, yT,
		x1, yM,
		xR, yM,
		xR, y1,
		x1, y1
	)

def draw_bottom(
	x0, 
	x1, 
	yB, 
	y0, 
	T, 
	path
):
	move_to(x0, y0, path)

	xL = x0-T
	yM = (y0-yB)/2
	xR = x1+T

	path.push("L",
  	xL, y0,
  	xL, yM,
  	x0, yM,
  	x0, yB,
  	x1, yB,
  	x1, yM,
  	xR, yM,
  	xR, y0,
  	x1, y0
	)

def draw_left(
	xL, 
	x0, 
	y0, 
	y1, 
	T, 
	path
):
	move_to(x0, y0, path)

	yT = y1+T
	xM = (x0-xL)/2
	yB = y0-T

	path.push("L",
		xM, y0,
		xM, yB,
		xL, yB,
		xL, yT,
		xM, yT,
		xM, y1,
		x0, y1
	)

def draw_right(
	x1, 
	xR, 
	y0, 
	y1, 
	T, 
	path
):
	move_to(x1, y0, path)

	yT = y1+T
	xM = x1+(xR-x1)/2
	yB = y0-T

	path.push("L",
		xM, y0,
		xM, yB,
		xR, yB,
		xR, yT,
		xM, yT,
		xM, y1,
		x1, y1
	)

def export(
	box: Box,
	returning=False
):
	W = cm_to_mm(box.width) + get_clearance(box.thickness)
	H = cm_to_mm(box.height) + get_clearance(box.thickness)
	D = calculate_top_depth(cm_to_mm(box.depth))
	T = box.thickness

	x0 = D
	xL = 0
	x1 = x0 + W
	xR = x1 + D

	y0 = D
	yB = 0
	y1 = y0 + H
	yT = y1 + D

	total_width = xR
	total_height = yT

	file_name = generate_file_name(box.client_name)

	full_path = os.path.join(
		os.path.expanduser("~"),
		"Desktop",
		box.client_name.replace(" ", "_"),
		file_name
  )

	dwg = svgwrite.Drawing(
		full_path,
		profile='full',
		size=(f"{total_width}mm", f"{total_height}mm"),
		viewBox=f"0 0 {total_width} {total_height}"
	)

	draw_rectangle(x0, x1, y0, y1, dwg, 'red')

	path = dwg.path(
		stroke="black",
		fill="none",
		stroke_width='0.1'
	)

	draw_top(x0, x1, y1, yT, T, path)
	draw_bottom(x0, x1, yB, y0, T, path)
	draw_left(xL, x0, y0, y1, T, path)
	draw_right(x1, xR, y0, y1, T, path)

	dwg.add(path)
	
	if returning:
		buffer = io.StringIO()
		dwg.write(buffer)

		return ExportBundle(buffer.getvalue(), file_name)
	else:
		dwg.save()