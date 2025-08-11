import math

class CardboardCircularTopComponent:
    def __init__(self, box_diameter_cm):
        self.box_diameter_cm = box_diameter_cm
        self.tampo_thickness = 1.9  # mm
        self.parede_thickness = 1.05  # mm
        self._compute_size()

    def _compute_size(self):
        # Profundidade fixa de 3cm
        self.depth = 30  # mm
        # O diâmetro da tampa é 0.5cm maior que o da caixa
        self.tampa_diameter_cm = self.box_diameter_cm + 0.5
        self.radius = (self.tampa_diameter_cm / 2) * 10  # mm
        self.circle_diameter = self.radius * 2
        self.band_length = 2 * math.pi * self.radius
        self.band_height = self.depth
        self.spacing = 20  # espaço entre as peças
        self.total_width = self.circle_diameter + self.spacing + self.band_length
        self.total_height = max(self.circle_diameter, self.band_height)

    def draw(self, dwg, x_offset, y_offset):
        # Desenhar o círculo (tampo) com espessura 1.9mm
        circle_center = (x_offset + self.radius, y_offset + self.radius)
        dwg.add(dwg.circle(center=circle_center, r=self.radius, stroke="black", fill="none", stroke_width=self.tampo_thickness))
        # Desenhar a faixa lateral (parede) com espessura 1.05mm
        band_x = x_offset + self.circle_diameter + self.spacing
        band_y = y_offset
        dwg.add(dwg.rect(insert=(band_x, band_y), size=(self.band_length, self.band_height), stroke="black", fill="none", stroke_width=self.parede_thickness)) 