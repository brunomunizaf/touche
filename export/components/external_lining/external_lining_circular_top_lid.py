import math

class ExternalLiningCircularTopLidComponent:
    def __init__(self, box_diameter_cm):
        self.box_diameter_cm = box_diameter_cm
        self.tampo_thickness = 1.9  # mm (espessura do tampo)
        self._compute_size()

    def _compute_size(self):
        # O diâmetro da tampa é 0.5cm maior que o da caixa
        self.tampa_diameter_cm = self.box_diameter_cm + 0.5
        self.radius = (self.tampa_diameter_cm / 2) * 10  # mm

        # Cálculo das dimensões do círculo (tampo)
        self.circle_diameter = self.radius * 2  # diâmetro do círculo

        # Tamanho total do SVG
        self.total_width = self.circle_diameter
        self.total_height = self.circle_diameter

    def draw(self, dwg, x_offset, y_offset):
        # Desenhar o círculo (tampo) com espessura 1.9mm
        circle_center = (x_offset + self.radius, y_offset + self.radius)
        dwg.add(dwg.circle(
            center=circle_center, 
            r=self.radius, 
            stroke="navy", 
            fill="none", 
            stroke_width=self.tampo_thickness
        ))
