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
	return f'{prefix}_revestimento {side_name} - base @{timestamp_str}.svg'

def cm_to_mm(number):
	return number * 10

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
	side: CoverSide,
	returning=False
):
	W = cm_to_mm(box.width)
	D = cm_to_mm(box.depth)
	H = cm_to_mm(box.height)
	T = box.thickness

	file_name = generate_file_name(box.client_name, side)

	full_path = os.path.join(
		os.path.expanduser("~"),
		"Desktop",
		box.client_name.replace(" ", "_"),
		file_name
  )

	if side == CoverSide.EXTERNAL:
		paper_clearance = 15

  	# Cardboard
		x0 = D + paper_clearance
		x1 = x0 + W
		xL = x0 - D
		xR = x1 + D
		xRR = xR + paper_clearance

		y0 = D + paper_clearance
		y1 = y0 + H
		yB = y0 - D
		yT = y1 + D
		yTT = yT + paper_clearance

		total_width = xRR
		total_height = yTT

		dwg = svgwrite.Drawing(
			full_path,
			size=(f"{total_width}mm", f"{total_height}mm"),
			viewBox=f"0 0 {total_width + 1} {total_height + 1}"
		)

		path = dwg.path(
			stroke="navy",
			fill="none",
			stroke_width='0.1'
		)

		path.push("M", xR + paper_clearance, y1)
		path.push("L", xR + paper_clearance, y0)
		path.push("L", xR + 6, y0)
		path.push("L", xR + 3, y0 - 1.5)
		path.push("L", x1 + T + 0.5, y0 - 1.5)
		path.push("L", x1 + T + paper_clearance, y0 - 3.5)
		path.push("L", x1 + T + paper_clearance, yB - 1.2)
		path.push("L", x1 + 1.9, yB - 3.1)
		path.push("L", x1 + 1.9, yB - 5)
		path.push("L", x1, yB - 5)
		path.push("L", x1, yB - paper_clearance)
		path.push("L", x0, yB - paper_clearance)
		path.push("L", x0, yB - 5)
		path.push("L", x0 - 1.9, yB - 5)
		path.push("L", x0 - 1.9, yB - 3.1)
		path.push("L", x0 - T - paper_clearance, yB - 1.2)
		path.push("L", x0 - T - paper_clearance, y0 - 3.5)
		path.push("L", x0 - T - 0.5, y0 - 1.5)
		path.push("L", xL - 3, y0 - 1.5)
		path.push("L", xL - 6, y0)
		path.push("L", xL - paper_clearance, y0)
		path.push("L", xL - paper_clearance, y1)

		path.push("L", xL - 6, y1)
		path.push("L", xL - 3, y1 + 1.5)
		path.push("L", x0 - T - 0.5, y1 + 1.5)
		path.push("L", x0 - T - paper_clearance, y1 + 3.5)
		path.push("L", x0 - T - paper_clearance, yT + 1.2)
		path.push("L", x0 - 1.9, yT + 3.1)
		path.push("L", x0 - 1.9, yT + 5)
		path.push("L", x0, yT + 5)
		path.push("L", x0, yT + paper_clearance)
		path.push("L", x1, yT + paper_clearance)
		path.push("L", x1, yT + 5)
		path.push("L", x1 + 1.9, yT + 5)
		path.push("L", x1 + 1.9, yT + 3.1)
		path.push("L", x1 + T + paper_clearance, yT + 1.2)
		path.push("L", x1 + T + paper_clearance, y1 + 3.5)
		path.push("L", x1 + T + 0.5, y1 + 1.5)
		path.push("L", xR + 3, y1 + 1.5)
		path.push("L", xR + 6, y1)
		path.push("L", xR + 15, y1)

		dwg.add(path)

	else:
		x0 = D
		x1 = x0 + W
		xL = x0 - D
		xR = x1 + D

		y0 = D
		y1 = y0 + H
		yB = y0 - D
		yT = y1 + D
	
		total_width = xR
		total_height = yT

		dwg = svgwrite.Drawing(
			full_path,
			profile='full',
			size=(f"{total_width}mm", f"{total_height}mm"),
			viewBox=f"0 0 {total_width} {total_height}"
		)

		path = dwg.path(
			stroke="navy",
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