class InternalLiningSingleMagnetTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.largura = width_cm * 10
        self.altura = height_cm * 10
        self.profundidade = depth_cm * 10
        self.espessura = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.espacamento = self._calcular_espacamento(self.espessura)
        self.largura_do_retangulo = self.largura
        self.altura_do_retangulo = (
            42 + self.altura + self.espacamento + (self.profundidade - 5)    
        )

        self.total_width = self.largura_do_retangulo
        self.total_height = self.altura_do_retangulo

    def _calcular_espacamento(self, espessura):
        if 1.5 <= espessura <= 2:
            return 6
        else:
            return 8

    def draw(self, dwg, x_offset, y_offset):
        abcissa_extrema_esquerda = x_offset
        abcissa_extrema_direita = abcissa_extrema_esquerda + self.largura_do_retangulo

        # Coordenadas do retângulo
        coordenada_inferior = y_offset
        coordenada_superior = coordenada_inferior + self.altura_do_retangulo

        dwg.add(dwg.polyline([
            (abcissa_extrema_esquerda, coordenada_superior),
            (abcissa_extrema_direita, coordenada_superior),
            (abcissa_extrema_direita, coordenada_inferior),
            (abcissa_extrema_esquerda, coordenada_inferior),
            (abcissa_extrema_esquerda, coordenada_superior)
        ], stroke="navy", fill="none", stroke_width='0.1'))
