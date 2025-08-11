class ExternalLiningSingleMagnetTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.largura = width_cm * 10
        self.altura = height_cm * 10
        self.profundidade = depth_cm * 10
        self.espessura = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.folga = 10
        self.espaco_sacado = 15
        self.largura_do_papelao = self.largura + self.folga
        self.espacamento = self._calcular_espacamento(self.espessura)
        self.altura_do_papelao_com_espacamentos = (
            self.profundidade + self.espacamento + self.altura + self.espacamento + self.profundidade
        )
        self.largura_total = self.largura_do_papelao + self.espaco_sacado * 2
        self.altura_total = self.altura_do_papelao_com_espacamentos + self.espaco_sacado * 2

        self.total_width = self.largura_total
        self.total_height = self.altura_total

    def _calcular_espacamento(self, espessura):
        if 1.5 <= espessura <= 2:
            return 6
        else:
            return 8

    def draw(self, dwg, x_offset, y_offset):
        abcissa_extrema_esquerda = x_offset
        abcissa_esquerda = abcissa_extrema_esquerda + 2 * self.espaco_sacado
        abcissa_extrema_direita = abcissa_extrema_esquerda + self.espaco_sacado + self.largura_do_papelao + self.espaco_sacado
        abcissa_direita = abcissa_extrema_direita - 2 * self.espaco_sacado

        coordenada_extrema_inferior = y_offset
        coordenada_inferior = coordenada_extrema_inferior + self.espaco_sacado
        coordenada_extrema_superior = coordenada_inferior + self.altura_do_papelao_com_espacamentos + self.espaco_sacado
        coordenada_superior = coordenada_extrema_superior - self.espaco_sacado

        dwg.add(dwg.polyline([
            (abcissa_extrema_esquerda, coordenada_superior),
            (abcissa_esquerda, coordenada_extrema_superior),
            (abcissa_direita, coordenada_extrema_superior),
            (abcissa_extrema_direita, coordenada_superior),
            (abcissa_extrema_direita, coordenada_inferior),
            (abcissa_direita, coordenada_extrema_inferior),
            (abcissa_esquerda, coordenada_extrema_inferior),
            (abcissa_extrema_esquerda, coordenada_inferior),
            (abcissa_extrema_esquerda, coordenada_superior),
        ], stroke="navy", fill="none", stroke_width='0.1'))