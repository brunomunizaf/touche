import math

class ExternalLiningCircularTopWallComponent:
    def __init__(self, box_diameter_cm):
        self.diametro = (box_diameter_cm * 10) + 5
        self.profundidade = 20
        self._compute_size()

    def _compute_size(self):
        self.sobra = 12
        self.raio = self.diametro / 2
        self.espaco_entre_papelao_e_palitos = 1.9
        self.altura_palito = 6
        self.altura = self.profundidade + self.espaco_entre_papelao_e_palitos + self.altura_palito
        self.largura = 2 * math.pi * self.raio + self.sobra

        self.total_width = self.largura
        self.total_height = self.altura

    def draw(self, dwg, x_offset, y_offset):
        dwg.add(dwg.rect(
            insert=(x_offset, y_offset), 
            size=(self.largura, self.altura), 
            stroke="navy", 
            fill="none", 
            stroke_width=0.1
        ))