import svgwrite

def cm_to_mm(number):
	return number * 10

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
	file_name,
	width,
	height,
	depth
):
	W = cm_to_mm(width)
	D = cm_to_mm(depth)
	H = cm_to_mm(height)
	margin = 2
	magnet_radius = 7

	x0 = 0
	y0 = 0
	x1 = W + 15
	yA = D - 5
	yB = yA + margin
	yC = yB + H
	yD = yC + margin
	yE = yD + D
	yF = yE + margin
	yG = yF + H + 10

	xM = x0 + (x1 - x0) / 2
	yM = yA / 2

	xL = x0 + (x1 - x0) / 4
	xR = x1 - (x1 - x0) / 4

	total_width = x1 - x0
	total_height = yG

	dwg = svgwrite.Drawing(
		file_name,
		size=(f"{total_width}mm", f"{total_height}mm"),
		viewBox=f"0 0 {total_width} {total_height}"
	)

	draw_rectangle(x0, x1, y0, yA, dwg)
	draw_rectangle(x0, x1, yB, yC, dwg)
	draw_rectangle(x0, x1, yD, yE, dwg)
	draw_rectangle(x0, x1, yF, yG, dwg)

	if W + 15 > 100:
		draw_magnet(xL, yM, magnet_radius, dwg)
		draw_magnet(xR, yM, magnet_radius, dwg)
	else:
		draw_magnet(xM, yM, magnet_radius, dwg)

	dwg.save()