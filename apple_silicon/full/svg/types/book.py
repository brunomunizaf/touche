import svgwrite

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

	x0 = 0
	y0 = 0
	x1 = W + 15
	yA = H + 10
	yB = yA + margin
	yC = yB + D
	yD = yC + margin
	yE = yD + yA

	total_width = x1 - x0
	total_height = yE

	dwg = svgwrite.Drawing(
		file_name,
		size=(f"{total_width}mm", f"{total_height}mm"),
		viewBox=f"0 0 {total_width} {total_height}"
	)

	draw_rectangle(x0, x1, y0, yA, dwg)
	draw_rectangle(x0, x1, yB, yC, dwg)
	draw_rectangle(x0, x1, yD, yE, dwg)

	dwg.save()