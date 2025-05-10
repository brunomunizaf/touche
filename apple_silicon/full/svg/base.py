import svgwrite
from datetime import datetime

def generate_file_name(prefix):
	timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
	return f'{prefix}_base@{timestamp_str}.svg'

def cm_to_mm(number):
	return number * 10

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
		stroke=stroke,
		stroke_width=0.1
	))

def export(
	file_name, 
	width, 
	height, 
	depth, 
	thickness, 
	with_magnets=False
):
	W = cm_to_mm(width)
	H = cm_to_mm(height)
	D = cm_to_mm(depth)
	T = thickness
	magnet_radius = 7

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
		generate_file_name(file_name),
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

	if with_magnets:
		xM = x0 + (x1 - x0) / 2
		yM = y1 + (D / 2)

		left_center = x0 + (x1 - x0) / 4
		right_center = x1 - (x1 - x0) / 4

		if W + 15 > 100:
			draw_magnet(left_center, yM, magnet_radius, dwg, 'red')
			draw_magnet(right_center, yM, magnet_radius, dwg, 'red')
		else:
			draw_magnet(xM, yM, magnet_radius, dwg, 'red')

	dwg.add(path)
	dwg.save()