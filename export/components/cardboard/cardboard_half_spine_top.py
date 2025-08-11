class CardboardHalfSpineTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.largura = width_cm * 10 
        self.altura = height_cm * 10
        self.profundidade = depth_cm * 10
        self.espessura = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.folga = 10
        self.espacamento = self._calcular_espacamento(self.espessura)
        self.raio_do_ima = 7
        self.largura_do_papelao = self.largura + self.folga
        self.largura_total = self.largura_do_papelao
        self.altura_total = (
            self.profundidade + self.espacamento + self.altura + self.espacamento + self.profundidade
        )

        self.total_width = self.largura_total
        self.total_height = self.altura_total

    def _calcular_espacamento(self, espessura):
        if 1.5 <= espessura <= 2:
            return 6
        else:
            return 8
        
    def _calcular_abcissa_ima(self, abcissa_esquerda, abcissa_direita, largura):
        if 150 <= largura <= 200:
            xL = abcissa_esquerda + 30
            xR = abcissa_direita - 30
        elif 200 < largura <= 300:
            xL = abcissa_esquerda + 40
            xR = abcissa_direita - 40
        else:
            xL = abcissa_esquerda + 45
            xR = abcissa_direita - 45
        return xL, xR
    
    def draw(self, dwg, x_offset, y_offset):
        abcissa_extrema_esquerda = x_offset
        abcissa_extrema_direita = abcissa_extrema_esquerda + self.largura_do_papelao

        # Coordenadas dos retângulos
        coordenada_inferior_primeiro_retangulo = y_offset
        coordenada_superior_primeiro_retangulo = coordenada_inferior_primeiro_retangulo + self.profundidade

        coordenada_inferior_segundo_retangulo = coordenada_superior_primeiro_retangulo + self.espacamento
        coordenada_superior_segundo_retangulo = coordenada_inferior_segundo_retangulo + self.altura

        coordenada_inferior_terceiro_retangulo = coordenada_superior_segundo_retangulo + self.espacamento
        coordenada_superior_terceiro_retangulo = coordenada_inferior_terceiro_retangulo + self.profundidade

        # Desenha três retângulos empilhados verticalmente
        for coordenada_superior, coordenada_inferior in [
            (coordenada_inferior_primeiro_retangulo, coordenada_superior_primeiro_retangulo),
            (coordenada_inferior_segundo_retangulo, coordenada_superior_segundo_retangulo),
            (coordenada_inferior_terceiro_retangulo, coordenada_superior_terceiro_retangulo)
        ]:
            dwg.add(dwg.polyline([
                (abcissa_extrema_esquerda, coordenada_superior),
                (abcissa_extrema_direita, coordenada_superior),
                (abcissa_extrema_direita, coordenada_inferior),
                (abcissa_extrema_esquerda, coordenada_inferior),
                (abcissa_extrema_esquerda, coordenada_superior)
            ], stroke="black", fill="none", stroke_width='0.1'))

        # Desenha imas no último retângulo
        largura = self.largura
        if largura + self.folga > 100:
            xLM, xRM = self._calcular_abcissa_ima(abcissa_extrema_esquerda + (self.folga/2), abcissa_extrema_direita - (self.folga/2), largura)
            yM = coordenada_superior_terceiro_retangulo - 30 if self.profundidade >= 100 else coordenada_superior_terceiro_retangulo - (self.profundidade - 5) / 2
            dwg.add(dwg.circle(center=(xLM, yM), r=self.raio_do_ima, fill="none", stroke="black", stroke_width=0.1))
            dwg.add(dwg.circle(center=(xRM, yM), r=self.raio_do_ima, fill="none", stroke="black", stroke_width=0.1))
        else:
            xM = abcissa_extrema_esquerda + (abcissa_extrema_direita - abcissa_extrema_esquerda) / 2
            yM = coordenada_superior_terceiro_retangulo - (self.profundidade - 5) / 2
            dwg.add(dwg.circle(center=(xM, yM), r=self.raio_do_ima, fill="none", stroke="black", stroke_width=0.1))