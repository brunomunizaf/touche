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
	path,
	extra_above=0
):
	move_to(x0, y1, path)	

	xL = x0-T
	yM = y1+(yT-y1)/2
	xR = x1+T

	path.push("L",
		xL, y1,
		xL, yM,
		x0, yM,
		x0, yT + extra_above,
		x1, yT + extra_above,
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

	paper_clearance = 15
	little_square_side = 2

	if side == CoverSide.EXTERNAL:
		total_width = (2 * (paper_clearance + 0.2 + H + (2.5 * T))) + W
		total_height = 200

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


		# y lateral, de baixo pra cima
		y_lateral_0 = 0
		y_lateral_1 = paper_clearance
		y_lateral_2 = paper_clearance
		y_lateral_3 = paper_clearance + little_square_side
		y_lateral_4 = paper_clearance + little_square_side + (2.5 * T)
		y_lateral_5 = paper_clearance + little_square_side + (2.5 * T) + D
		y_lateral_6 = paper_clearance + little_square_side + (2.5 * T) + D + (2.5 * T)
		y_lateral_7 = paper_clearance + little_square_side + (2.5 * T) + D + (2.5 * T) + little_square_side
		y_lateral_8 = paper_clearance + little_square_side + (2.5 * T) + D + (2.5 * T) + little_square_side
		y_lateral_9 = paper_clearance + little_square_side + (2.5 * T) + D + (2.5 * T) + little_square_side + paper_clearance

		# --------

		path.push(
			"M", 
			paper_clearance + little_square_side, 
			y_lateral_0
		)

		path.push(
			"L", 
			paper_clearance + little_square_side, 
			y_lateral_1
		)
		path.push(
			"L", 
			paper_clearance, 
			y_lateral_2
		)
		path.push(
			"L", 
			paper_clearance, 
			y_lateral_3
		)
		path.push(
			"L", 
			0, 
			y_lateral_4
		)
		path.push(
			"L", 
			0, 
			y_lateral_5
		)
		path.push(
			"L", 
			paper_clearance, 
			y_lateral_6
		)
		path.push(
			"L", 
			paper_clearance, 
			y_lateral_7
		)
		path.push(
			"L", 
			paper_clearance + little_square_side, 
			y_lateral_8
		)
		path.push(
			"L", 
			paper_clearance + little_square_side, 
			y_lateral_9
		)
		# path.push(
		# 	"L", 
		# 	paper_clearance + little_square_side + H, 
		# 	D + paper_clearance
		# )
		# path.push(
		# 	"L", 
		# 	paper_clearance + little_square_side + H + (0.5 * T), 
		# 	D + (2 * T)
		# )
		# path.push(
		# 	"L", 
		# 	paper_clearance + little_square_side + H + (1.5 * T), 
		# 	D
		# )
		# path.push(
		# 	"L", 
		# 	paper_clearance + little_square_side + H + (2.5 * T), 
		# 	D + (2 * T)
		# )
		# path.push(
		# 	"L", 
		# 	paper_clearance + little_square_side + H + (3 * T), 
		# 	D + paper_clearance
		# )
		# path.push(
		# 	"L", 
		# 	paper_clearance + little_square_side + H + (3 * T), 
		# 	D + paper_clearance
		# )
		# path.push(
		# 	"L", 
		# 	paper_clearance + little_square_side + H + (3 * T) + W - (0.5 * T), 
		# 	D + paper_clearance
		# )
		# path.push( # <------
		# 	"L", 
		# 	paper_clearance + little_square_side + H + (3 * T) + W, 
		# 	D + (2 * T)
		# )
		# path.push(
		# 	"L", 
		# 	paper_clearance + little_square_side + H + (3 * T) + W + (1.5 * T), 
		# 	D
		# )
		# path.push(
		# 	"L", 
		# 	paper_clearance + little_square_side + H + (3 * T) + W + (2.5 * T), 
		# 	D + (2 * T)
		# )
		# path.push(
		# 	"L", 
		# 	paper_clearance + little_square_side + H + (3 * T) + W + (3 * T), 
		# 	D + paper_clearance
		# )

		#path.push("L", paper_clearance + little_square_side + H - (2.5 * T), D + paper_clearance)
		#path.push("L", paper_clearance + little_square_side + H - (2 * T), D + (2 * T))
		#path.push("L", paper_clearance + little_square_side + H - T, D)
		#path.push("L", paper_clearance + little_square_side + H, D + (2 * T))
		#path.push("L", paper_clearance + little_square_side + H + 0.5 * T, D + paper_clearance)
		#path.push("L", paper_clearance + little_square_side + H + W - 0.5 * T, D + paper_clearance)
		#path.push("L", paper_clearance + little_square_side + H + W, D + (2 * T))
		#path.push("L", paper_clearance + little_square_side + H + W + T, D)
		#path.push("L", paper_clearance + little_square_side + H + W + (2 * T), D + (2 * T))
		#path.push("L", paper_clearance + little_square_side + H + W + (2.5 * T), D + paper_clearance)
		#path.push("L", paper_clearance + little_square_side + (2 * H) + W + (2.5 * T), D + paper_clearance)

		#path.push("L", )


  	# Cardboard
		# x0 = D + paper_clearance
		# x1 = x0 + W
		# xL = x0 - D
		# xR = x1 + D
		# xRR = xR + paper_clearance

		# y0 = D + paper_clearance
		# y1 = y0 + H
		# yB = y0 - D
		# yT = y1 + D
		# yTT = yT + paper_clearance
	
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
		total_height = yT + paper_clearance

		dwg = svgwrite.Drawing(
			full_path,
			profile='full',
			size=(f"{total_width}mm", f"{total_height}mm"),
			viewBox=f"0 0 {total_width} {total_height} "
		)

		path = dwg.path(
			stroke="navy",
			fill="none",
			stroke_width='0.1'
		)

		draw_top(x0, x1, y1, yT, T, path, paper_clearance)
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