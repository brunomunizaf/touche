class ExternalLiningBaseSingleMagnetComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.largura = width_cm * 10
        self.altura = height_cm * 10
        self.profundidade = depth_cm * 10
        self.espessura = thickness_mm
        self._compute_geometry()

    def _compute_geometry(self):
        self.sobra = 15
        self.total_width = self.profundidade + self.sobra + self.largura + self.profundidade + self.sobra
        self.total_height = self.profundidade + self.sobra + self.altura + self.profundidade + self.sobra

    def draw(self, dwg, x_offset, y_offset):
        x0 = self.profundidade + self.sobra + x_offset
        x1 = x0 + self.largura
        xL = x0 - self.profundidade
        xR = x1 + self.profundidade

        y0 = self.profundidade + self.sobra + y_offset
        y1 = y0 + self.altura
        yB = y0 - self.profundidade
        yT = y1 + self.profundidade

        path = dwg.path(
            stroke="navy",
            fill="none",
            stroke_width='0.1'
        )

        # Lado direito

        path.push("M", xR + self.sobra, y1)
        path.push("L", xR + self.sobra, y0)
        path.push("L", xR + 6, y0)
        path.push("L", xR + 3, y0 - 1.5)
        path.push("L", x1 + self.espessura + 0.5, y0 - 1.5)

        # Lado superior

        path.push("L", x1 + self.espessura + self.sobra, y0 - 3.5)
        path.push("L", x1 + self.espessura + self.sobra, yB - 1.2)
        path.push("L", x1 + 1.9, yB - 3.1)
        path.push("L", x1 + 1.9, yB - 5)
        path.push("L", x1, yB - 5)
        path.push("L", x1, yB - self.sobra)
        path.push("L", x0, yB - self.sobra)
        path.push("L", x0, yB - 5)
        path.push("L", x0 - 1.9, yB - 5)
        path.push("L", x0 - 1.9, yB - 3.1)
        path.push("L", x0 - self.espessura - self.sobra, yB - 1.2)
        path.push("L", x0 - self.espessura - self.sobra, y0 - 3.5)
        path.push("L", x0 - self.espessura - 0.5, y0 - 1.5)

        # Lado esquerdo

        path.push("L", xL - 3, y0 - 1.5)
        path.push("L", xL - 6, y0)
        path.push("L", xL - self.sobra, y0)
        path.push("L", xL - self.sobra, y1)

        # Lado inferior

        path.push("L", xL - self.sobra, y1)
        path.push("L", xL - 5, y1)
        path.push("L", xL - 5, y1 + 1.9)
        path.push("L", xL - 3.1, y1 + 1.9)
        path.push("L", xL - 1.2, y1 + self.sobra + 1.9)
        path.push("L", x0 - self.espessura - 1.2, y1 + self.sobra + 1.9)
        path.push("L", x0 - self.espessura, y1 + 1.9)
        # path.push("L", x1 + 1.9, yB - 3.1)
        # path.push("L", x1 + 1.9, yB - 5)
        # path.push("L", x1, yB - 5)
        # path.push("L", x1, yB - self.sobra)
        # path.push("L", x0, yB - self.sobra)
        # path.push("L", x0, yB - 5)
        # path.push("L", x0 - 1.9, yB - 5)
        # path.push("L", x0 - 1.9, yB - 3.1)

        dwg.add(path)