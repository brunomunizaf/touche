import math

class CardboardLooseTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.largura = (width_cm * 10) + self._calcular_folga(thickness_mm)
        self.altura = (height_cm * 10) + self._calcular_folga(thickness_mm)
        self.profundidade = self._calcular_profundidade_da_tampa(depth_cm * 10)
        self.espessura = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.total_width = self.largura + (2 * self.profundidade)
        self.total_height = self.altura + (2 * self.profundidade)

    def _calcular_folga(self, espessura):
        if espessura in (1.90, 2.00):
            return 7.0
        elif espessura == 2.50:
            return 8.0
        else:
            return espessura * 3

    def _calcular_profundidade_da_tampa(self, profundidade):
        if profundidade <= 50:
            return 15
        elif profundidade <= 100:
            return 20
        else:
            return 20 + 10 * math.ceil((profundidade - 100) / 50)

    def draw(self, dwg, x_offset, y_offset):
        abcissa_extrema_esquerda = x_offset
        abcissa_esquerda = abcissa_extrema_esquerda + self.profundidade
        abcissa_direita = abcissa_esquerda + self.largura
        abcissa_extrema_direita = abcissa_direita + self.profundidade

        coordenada_extrema_inferior = y_offset
        coordenada_inferior = coordenada_extrema_inferior + self.profundidade
        coordenada_superior = coordenada_inferior + self.altura        
        coordenada_extrema_superior = coordenada_superior + self.profundidade

        meia_profundidade = self.profundidade / 2

        # Desenha o retângulo do meio (vinco)
        dwg.add(dwg.polyline([
            (abcissa_esquerda, coordenada_inferior),
            (abcissa_direita, coordenada_inferior),
            (abcissa_direita, coordenada_superior),
            (abcissa_esquerda, coordenada_superior),
            (abcissa_esquerda, coordenada_inferior),
        ], stroke="red", fill="none", stroke_width='0.1'))

        path = dwg.path(
            stroke="black",
            fill="none",
            stroke_width='0.1'
        )

        # Move para canto inferior esquerdo do retângulo do vinco
        path.push("M", 
            abcissa_esquerda, coordenada_inferior
        )

        # Desenha a aba inferior
        path.push("L",
            abcissa_esquerda - self.espessura, coordenada_inferior, 
            abcissa_esquerda - self.espessura, coordenada_inferior - meia_profundidade, 
            abcissa_esquerda, coordenada_inferior - meia_profundidade, 
            abcissa_esquerda, coordenada_extrema_inferior,
            abcissa_direita, coordenada_extrema_inferior, 
            abcissa_direita, coordenada_inferior - meia_profundidade, 
            abcissa_direita + self.espessura, coordenada_inferior - meia_profundidade, 
            abcissa_direita + self.espessura, coordenada_inferior,
            abcissa_direita, coordenada_inferior
        )

        # Move para canto superior esquerdo do retângulo do vinco
        path.push("M", abcissa_esquerda, coordenada_superior)

        # Desenha a aba superior
        path.push("L",
            abcissa_esquerda - self.espessura, coordenada_superior, 
            abcissa_esquerda - self.espessura, coordenada_superior + meia_profundidade, 
            abcissa_esquerda, coordenada_superior + meia_profundidade, 
            abcissa_esquerda, coordenada_extrema_superior,
            abcissa_direita, coordenada_extrema_superior, 
            abcissa_direita, coordenada_superior + meia_profundidade, 
            abcissa_direita + self.espessura, coordenada_superior + meia_profundidade, 
            abcissa_direita + self.espessura, coordenada_superior,
            abcissa_direita, coordenada_superior
        )

        # Move para canto inferior esquerdo do retângulo do vinco
        path.push("M", abcissa_esquerda, coordenada_inferior)

        # Desenha a aba esquerda
        path.push("L", 
            abcissa_esquerda - meia_profundidade, coordenada_inferior, 
            abcissa_esquerda - meia_profundidade, coordenada_inferior - self.espessura, 
            abcissa_extrema_esquerda, coordenada_inferior - self.espessura,
            abcissa_extrema_esquerda, coordenada_superior + self.espessura, 
            abcissa_esquerda - meia_profundidade, coordenada_superior + self.espessura, 
            abcissa_esquerda - meia_profundidade, coordenada_superior, 
            abcissa_esquerda, coordenada_superior
        )

        # Move para canto inferior direito do retângulo do vinco
        path.push("M", abcissa_direita, coordenada_inferior)

        # Desenha a aba direita
        path.push("L", 
            abcissa_extrema_direita - meia_profundidade, coordenada_inferior, 
            abcissa_extrema_direita - meia_profundidade, coordenada_inferior - self.espessura, 
            abcissa_extrema_direita, coordenada_inferior - self.espessura,
            abcissa_extrema_direita, coordenada_superior + self.espessura, 
            abcissa_extrema_direita - meia_profundidade, coordenada_superior + self.espessura, 
            abcissa_extrema_direita - meia_profundidade, coordenada_superior, 
            abcissa_direita, coordenada_superior
        )

        dwg.add(path)