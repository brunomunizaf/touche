import math

class ExternalLiningCircularBaseWallComponent:
    def __init__(self, box_diameter_cm, box_depth_cm):
        self.diametro = box_diameter_cm * 10
        self.profundidade = box_depth_cm * 10
        self._compute_size()

    def _compute_size(self):
        self.sobra = 12
        self.raio = self.diametro / 2
        self.espaco_entre_papelao_e_palitos = 1.9
        self.altura_palito = 6
        self.altura = self.profundidade + (2 * self.espaco_entre_papelao_e_palitos) + (2 * self.altura_palito)
        self.largura = 2 * math.pi * self.raio + self.sobra

        self.total_width = self.largura
        self.total_height = self.altura
        
        # Calcular quantos palitinhos cabem ao longo da largura da parede
        self.perimetro_lado = self.largura
        self.espaco_entre_palitos = 10  # 10mm entre cada palito
        self.largura_palito = 0.1
        self.numero_palitos_por_lado = int(self.perimetro_lado / (self.espaco_entre_palitos + self.largura_palito))

    def _desenhar_palitos_lado(self, dwg, x_offset, y_offset, lado):
        """Desenha palitinhos em um lado específico"""
        if lado == "superior":
            # Lado superior - palitinhos apontam para baixo
            x_base = x_offset + self.espaco_entre_papelao_e_palitos
            y_base = y_offset
            direcao = 1  # para baixo
        elif lado == "inferior":
            # Lado inferior - palitinhos apontam para cima
            x_base = x_offset + self.espaco_entre_papelao_e_palitos
            y_base = y_offset + self.altura
            direcao = -1  # para cima
        else:
            return
        
        # Desenhar palitinhos ao longo do lado
        for i in range(self.numero_palitos_por_lado):
            # Calcular posição horizontal do palito
            x_pos = x_base + (i * (self.espaco_entre_palitos + self.largura_palito))
            
            # Ponto inicial do palito (na borda)
            x_inicio = x_pos
            y_inicio = y_base
            
            # Ponto final do palito (apontando para o lado oposto)
            x_fim = x_pos
            y_fim = y_base + (direcao * self.altura_palito)
            
            # Desenhar o palito como um segmento de linha
            dwg.add(dwg.line(
                start=(x_inicio, y_inicio),
                end=(x_fim, y_fim),
                stroke="navy",
                stroke_width=0.1
            ))

    def draw(self, dwg, x_offset, y_offset):
        # Criar um único path que inclui o retângulo e os palitinhos
        path = dwg.path(stroke="navy", fill="none", stroke_width=0.1)
        
        # Coordenadas do retângulo
        x1, y1 = x_offset, y_offset
        x2, y2 = x_offset + self.largura, y_offset + self.altura
        
        # Desenhar o retângulo principal usando comandos de path
        path.push("M", x1, y1)  # Mover para o canto superior esquerdo
        path.push("L", x2, y1)  # Linha para o canto superior direito
        path.push("L", x2, y2)  # Linha para o canto inferior direito
        path.push("L", x1, y2)  # Linha para o canto inferior esquerdo
        path.push("Z")           # Fechar o retângulo
        
        # Adicionar os palitinhos ao mesmo path
        margem_borda = 10
        x_inicio_palitos = x_offset + margem_borda
        x_fim_palitos = x_inicio_palitos + self.largura
        area_disponivel = x_fim_palitos - x_inicio_palitos
        numero_palitos_ajustado = int(area_disponivel / (self.espaco_entre_palitos + self.largura_palito))
        
        # Desenhar palitinhos SUPERIORES como parte do mesmo path
        for i in range(numero_palitos_ajustado):
            x_pos = x_inicio_palitos + (i * (self.espaco_entre_palitos + self.largura_palito))
            
            # Ponto inicial do palito (na borda superior)
            x_inicio = x_pos
            y_inicio = y_offset
            
            # Ponto final do palito (apontando para baixo)
            x_fim = x_pos
            y_fim = y_offset + self.altura_palito
            
            # Adicionar palito ao path
            path.push("M", x_inicio, y_inicio)  # Mover para o início do palito
            path.push("L", x_fim, y_fim)        # Linha para o fim do palito
        
        # Desenhar palitinhos INFERIORES como parte do mesmo path
        for i in range(numero_palitos_ajustado):
            x_pos = x_inicio_palitos + (i * (self.espaco_entre_palitos + self.largura_palito))
            
            # Ponto inicial do palito (na borda inferior)
            x_inicio = x_pos
            y_inicio = y_offset + self.altura
            
            # Ponto final do palito (apontando para cima)
            x_fim = x_pos
            y_fim = (y_offset + self.altura) - self.altura_palito
            
            # Adicionar palito ao path
            path.push("M", x_inicio, y_inicio)  # Mover para o início do palito
            path.push("L", x_fim, y_fim)        # Linha para o fim do palito
        
        # Adicionar o path completo ao desenho
        dwg.add(path)