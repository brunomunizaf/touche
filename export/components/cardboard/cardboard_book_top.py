class CardboardBookTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.largura = (width_cm * 10) + 15
        self.altura = (height_cm * 10) + 10
        self.profundidade = depth_cm * 10
        self.espessura = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.espacamento = self._calcular_espacamento(self.espessura)
        self.total_width = self.largura
        self.total_height = (
            self.altura + self.espacamento + self.profundidade + self.espacamento + self.altura
        )

    def _calcular_espacamento(self, espessura):
        if 1.5 <= espessura <= 2:
            return 6
        else:
            return 8

    def draw(self, dwg, x_offset, y_offset):
        abcissa_esquerda = x_offset
        abcissa_direita = abcissa_esquerda + self.largura

        # Tampo superior
        coordenada_inferior_tampo_inferior = y_offset
        coordenada_superior_tampo_inferior = coordenada_inferior_tampo_inferior + self.altura

        # Lombada
        coordenada_inferior_lombada = coordenada_superior_tampo_inferior + self.espacamento
        coordenada_superior_lombada = coordenada_inferior_lombada + self.profundidade

        # Tampo inferior
        coordenada_inferior_tampo_superior = coordenada_superior_lombada + self.espacamento
        coordenada_superior_tampo_superior = coordenada_inferior_tampo_superior + self.altura

        # Três retangulos empilhados verticalmente
        for coordenada_superior, coordenada_inferior in [
            (coordenada_superior_tampo_superior, coordenada_inferior_tampo_superior),
            (coordenada_superior_lombada, coordenada_inferior_lombada),
            (coordenada_superior_tampo_inferior, coordenada_inferior_tampo_inferior)
        ]:
            dwg.add(dwg.polyline(
            [
                (abcissa_esquerda, coordenada_superior),
                (abcissa_direita, coordenada_superior),
                (abcissa_direita, coordenada_inferior),
                (abcissa_esquerda, coordenada_inferior),
                (abcissa_esquerda, coordenada_superior)
            ], 
                stroke="navy", 
                fill="none", 
                stroke_width='0.1'
            ))