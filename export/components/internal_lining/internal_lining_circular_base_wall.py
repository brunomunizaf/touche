import math

class InternalLiningCircularBaseWallComponent:
    def __init__(self, box_diameter_cm, box_depth_cm):
        self.diametro = box_diameter_cm * 10
        self.profundidade = box_depth_cm * 10
        self._compute_size()

    def _compute_size(self):
        self.sobra = 12
        self.raio = self.diametro / 2
        self.altura = self.profundidade
        self.largura = 2 * math.pi * self.raio + self.sobra

        self.total_width = self.largura
        self.total_height = self.altura

    def draw(self, dwg, x_offset, y_offset):
        dwg.add(
            dwg.rect(
                insert=(x_offset, y_offset), 
                size=(self.largura, self.altura), 
                stroke="navy", 
                fill="none", 
                stroke_width=0.1
            )
        )
