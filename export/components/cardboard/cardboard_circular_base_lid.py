class CardboardCircularBaseLidComponent:
    def __init__(self, box_diameter_cm):
        self.diametro = box_diameter_cm * 10
        self._compute_size()

    def _compute_size(self):
        self.raio = self.diametro / 2
        self.total_width = self.raio * 2
        self.total_height = self.raio * 2

    def draw(self, dwg, x_offset, y_offset):
        centro = (x_offset + self.raio, y_offset + self.raio)
        dwg.add(
            dwg.circle(
                center=centro, 
                r=self.raio, 
                stroke="black", 
                fill="none", 
                stroke_width=0.1
            )
        )
