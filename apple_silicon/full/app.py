from svg.top import TopType
from svg.top import export as export_top
from svg.base import export as export_base

export_base('teste', 15, 15, 10, 1.9, True)
export_top('teste', 15, 15, 1, 1.9, TopType.BOOK)
export_top('teste', 10, 10, 10, 1.9, TopType.MAGNET)

def calculate_cost(
	width, 
	height, 
	depth, 
	thickness, 
	cost_per_cm2=0.09
):
	def cm_to_mm(number):
		return number * 10

	W = cm_to_mm(width)
	H = cm_to_mm(height)
	D = cm_to_mm(depth)
	T = thickness

	# Áreas em mm²
	area_base = W * H
	area_top_bottom = 2 * (W + T) * D
	area_left_right = 2 * (H + T) * D

	# Área total usada na base da caixa
	area_total_mm2 = area_base + area_top_bottom + area_left_right
	area_total_cm2 = area_total_mm2 / 100  # 1 cm² = 100 mm²

	custo_total = area_total_cm2 * custo_por_cm2
	return round(custo_total, 4)  # em reais
