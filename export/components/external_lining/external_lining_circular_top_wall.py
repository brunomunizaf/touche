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
        
        # Calcular quantos palitinhos cabem ao longo da largura da parede
        self.perimetro_lado = self.largura
        self.espaco_entre_palitos = 10  # 10mm entre cada palito
        self.largura_palito = 0.1
        self.numero_palitos_por_lado = int(self.perimetro_lado / (self.espaco_entre_palitos + self.largura_palito))

    def _desenhar_palitos_lado_superior(self, dwg, x_offset, y_offset):
        """Desenha palitinhos apenas no lado superior"""
        # Lado superior - palitinhos apontam para baixo
        x_base = x_offset
        y_base = y_offset
        
        # Margem das bordas para evitar palitinhos muito próximos das extremidades
        margem_borda = 10  # 10mm de margem de cada lado
        
        # Calcular posições de início e fim para os palitinhos
        x_inicio_palitos = x_base + margem_borda
        x_fim_palitos = x_inicio_palitos + self.largura
        
        # Calcular quantos palitinhos cabem na área disponível
        area_disponivel = x_fim_palitos - x_inicio_palitos
        numero_palitos_ajustado = int(area_disponivel / (self.espaco_entre_palitos + self.largura_palito))
        
        # Desenhar palitinhos ao longo do lado superior (com margem das bordas)
        for i in range(numero_palitos_ajustado):
            # Calcular posição horizontal do palito
            x_pos = x_inicio_palitos + (i * (self.espaco_entre_palitos + self.largura_palito))
            
            # Ponto inicial do palito (na borda superior)
            x_inicio = x_pos
            y_inicio = y_base
            
            # Ponto final do palito (apontando para baixo)
            x_fim = x_pos
            y_fim = y_base + self.altura_palito
            
            # Desenhar o palito como um segmento de linha
            dwg.add(dwg.line(
                start=(x_inicio, y_inicio),
                end=(x_fim, y_fim),
                stroke="navy",
                stroke_width=0.1
            ))

    def draw(self, dwg, x_offset, y_offset):
        # Desenhar o retângulo principal
        dwg.add(dwg.rect(
            insert=(x_offset, y_offset), 
            size=(self.largura, self.altura), 
            stroke="navy", 
            fill="none", 
            stroke_width=0.1
        ))
        
        # Desenhar palitinhos apenas no lado superior
        self._desenhar_palitos_lado_superior(dwg, x_offset, y_offset)