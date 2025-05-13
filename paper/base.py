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

	external_clearance = 15

  # Cardboard
	x0 = D + external_clearance
	x1 = x0 + W
	xL = x0 - D
	xR = x1 + D
	xRR = xR + external_clearance

	y0 = D + external_clearance
	y1 = y0 + H
	yB = y0 - D
	yT = y1 + D
	yTT = yT + external_clearance

	if side == CoverSide.EXTERNAL:
		clearance = external_clearance
		total_width = xRR
		total_height = yTT

		dwg = svgwrite.Drawing(
			full_path,
			size=(f"{total_width}mm", f"{total_height}mm"),
			viewBox=f"0 0 {total_width + 1} {total_height + 1}"
		)

		path = dwg.path(
			stroke="blue",
			fill="none",
			stroke_width='0.1'
		)

		path.push("M", xR + clearance, y1)
		path.push("L", xR + clearance, y0)
		path.push("L", xR + 6, y0)
		path.push("L", xR + 3, y0 - 1.5)
		path.push("L", x1 + T + 0.5, y0 - 1.5)
		path.push("L", x1 + T + clearance, y0 - 3.5)
		path.push("L", x1 + T + clearance, yB - 1.2)
		path.push("L", x1 + 1.9, yB - 3.1)
		path.push("L", x1 + 1.9, yB - 5)
		path.push("L", x1, yB - 5)
		path.push("L", x1, yB - clearance)
		path.push("L", x0, yB - clearance)
		path.push("L", x0, yB - 5)
		path.push("L", x0 - 1.9, yB - 5)
		path.push("L", x0 - 1.9, yB - 3.1)
		path.push("L", x0 - T - clearance, yB - 1.2)
		path.push("L", x0 - T - clearance, y0 - 3.5)
		path.push("L", x0 - T - 0.5, y0 - 1.5)
		path.push("L", xL - 3, y0 - 1.5)
		path.push("L", xL - 6, y0)
		path.push("L", xL - clearance, y0)
		path.push("L", xL - clearance, y1)

		path.push("L", xL - 6, y1)
		path.push("L", xL - 3, y1 + 1.5)
		path.push("L", x0 - T - 0.5, y1 + 1.5)
		path.push("L", x0 - T - clearance, y1 + 3.5)
		path.push("L", x0 - T - clearance, yT + 1.2)
		path.push("L", x0 - 1.9, yT + 3.1)
		path.push("L", x0 - 1.9, yT + 5)
		path.push("L", x0, yT + 5)
		path.push("L", x0, yT + clearance)
		path.push("L", x1, yT + clearance)
		path.push("L", x1, yT + 5)
		path.push("L", x1 + 1.9, yT + 5)
		path.push("L", x1 + 1.9, yT + 3.1)
		path.push("L", x1 + T + clearance, yT + 1.2)
		path.push("L", x1 + T + clearance, y1 + 3.5)
		path.push("L", x1 + T + 0.5, y1 + 1.5)
		path.push("L", xR + 3, y1 + 1.5)
		path.push("L", xR + 6, y1)
		path.push("L", xR + 15, y1)

		dwg.add(path)

	else:
		raise NotImplementedError("Exportação de revestimento interno da base ainda não foi implementada.")
		
	if returning:
		buffer = io.StringIO()
		dwg.write(buffer)

		return ExportBundle(buffer.getvalue(), file_name)
	else:
		dwg.save()