import math

class ExternalLiningCircularTopLidComponent:
    def __init__(self, box_diameter_cm):
        self.altura_palito = 6
        self.espaco_entre_papelao_e_palitos = 2.05 # espessura do papelao mais fino + 1 mm de sobra
        self.diametro_papelao = (box_diameter_cm * 10) + 5
        self.diametro = self.diametro_papelao + (2 * self.espaco_entre_papelao_e_palitos) + (2 * self.altura_palito)
        self._compute_size()

    def _compute_size(self):
        self.raio = self.diametro / 2
        self.total_width = self.diametro
        self.total_height = self.diametro
        
        # Calcular quantos palitinhos cabem no perímetro
        self.perimetro = 2 * math.pi * self.raio
        self.espaco_entre_palitos = 10  # 10mm entre cada palito
        self.largura_palito = 0.1
        self.numero_palitos = int(self.perimetro / (self.espaco_entre_palitos + self.largura_palito))

    def _desenhar_palitos(self, dwg, centro, raio):
        """Desenha os palitinhos ao redor do perímetro circular"""
        angulo_inicial = 0
        angulo_incremento = 2 * math.pi / self.numero_palitos
        
        # Comprimento do palito (da circunferência até o ponto interno)
        comprimento_palito = self.altura_palito
        
        for i in range(self.numero_palitos):
            # Calcular posição do palito
            angulo = angulo_inicial + (i * angulo_incremento)
            
            # Ponto inicial do palito (na circunferência)
            x_inicio = centro[0] + (raio * math.cos(angulo))
            y_inicio = centro[1] + (raio * math.sin(angulo))
            
            # Ponto final do palito (interno, apontando para o centro)
            x_fim = centro[0] + ((raio - comprimento_palito) * math.cos(angulo))
            y_fim = centro[1] + ((raio - comprimento_palito) * math.sin(angulo))
            
            # Desenhar o palito como um segmento de linha simples
            dwg.add(dwg.line(
                start=(x_inicio, y_inicio),
                end=(x_fim, y_fim),
                stroke="navy",
                stroke_width=0.1
            ))

    def draw(self, dwg, x_offset, y_offset):
        centro = (x_offset + self.raio, y_offset + self.raio)
        
        # Criar um único path que inclui o círculo e os palitinhos
        path = dwg.path(stroke="navy", fill="none", stroke_width=0.1)
        
        # Desenhar o círculo principal usando comandos de path
        # Usar comando de arco para criar um círculo perfeito
        raio = self.raio
        cx, cy = centro
        
        # Mover para o ponto inicial (direita do círculo)
        path.push("M", cx + raio, cy)
        
        # Desenhar o círculo usando dois arcos de 180 graus
        # Arco superior (direita para esquerda)
        path.push("A", raio, raio, 0, 1, 0, cx - raio, cy)
        # Arco inferior (esquerda para direita)
        path.push("A", raio, raio, 0, 1, 0, cx + raio, cy)
        
        # Adicionar os palitinhos ao mesmo path
        angulo_inicial = 0
        angulo_incremento = 2 * math.pi / self.numero_palitos
        
        for i in range(self.numero_palitos):
            # Calcular posição do palito
            angulo = angulo_inicial + (i * angulo_incremento)
            
            # Ponto inicial do palito (na circunferência)
            x_inicio = centro[0] + (self.raio * math.cos(angulo))
            y_inicio = centro[1] + (self.raio * math.sin(angulo))
            
            # Ponto final do palito (interno, apontando para o centro)
            x_fim = centro[0] + ((self.raio - self.altura_palito) * math.cos(angulo))
            y_fim = centro[1] + ((self.raio - self.altura_palito) * math.sin(angulo))
            
            # Adicionar palito ao path
            path.push("M", x_inicio, y_inicio)  # Mover para o início do palito
            path.push("L", x_fim, y_fim)        # Linha para o fim do palito
        
        # Adicionar o path completo ao desenho
        dwg.add(path)
