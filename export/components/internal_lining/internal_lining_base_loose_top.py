class InternalLiningBaseForLooseTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.largura = width_cm * 10  # convert to mm
        self.altura = height_cm * 10
        self.profundidade = depth_cm * 10
        self.espessura = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.total_width = self.largura + 2 * self.profundidade
        self.total_height = self.altura + 2 * self.profundidade
    
    def draw(self, dwg, x_offset, y_offset):
        main_left_x = self.profundidade + x_offset
        main_right_x = main_left_x + self.largura
        main_bottom_y = self.profundidade + y_offset
        main_top_y = main_bottom_y + self.altura
        flap_left_x = (main_left_x - self.profundidade) + 0.5
        flap_right_x = (main_right_x + self.profundidade) - 0.5
        flap_bottom_y = (main_bottom_y - self.profundidade) + 0.5
        flap_top_y = (main_top_y + self.profundidade) - 0.5

        path = dwg.path(stroke="navy", fill="none", stroke_width='0.1')

        path.push("M", main_left_x, main_top_y)

        path.push("L", 
            main_left_x - self.espessura, main_top_y, 
            main_left_x - self.espessura, main_top_y + self.profundidade / 2, 
            main_left_x, main_top_y + self.profundidade / 2, 
            main_left_x, flap_top_y,
            main_right_x, flap_top_y, 
            main_right_x, main_top_y + self.profundidade / 2, 
            main_right_x + self.espessura, main_top_y + self.profundidade / 2, 
            main_right_x + self.espessura, main_top_y, 
            main_right_x, main_top_y
        )

        path.push("M", main_left_x, main_bottom_y)

        path.push("L", 
            main_left_x - self.espessura, main_bottom_y, 
            main_left_x - self.espessura, main_bottom_y - self.profundidade / 2, 
            main_left_x, main_bottom_y - self.profundidade / 2, 
            main_left_x, flap_bottom_y,
            main_right_x, flap_bottom_y, 
            main_right_x, main_bottom_y - self.profundidade / 2, 
            main_right_x + self.espessura, main_bottom_y - self.profundidade / 2, 
            main_right_x + self.espessura, main_bottom_y, 
            main_right_x, main_bottom_y
        )

        path.push("M", main_left_x, main_bottom_y)

        path.push("L", 
            main_left_x - self.profundidade / 2, main_bottom_y, 
            main_left_x - self.profundidade / 2, main_bottom_y - self.espessura, 
            flap_left_x, main_bottom_y - self.espessura,
            flap_left_x, main_top_y + self.espessura, 
            main_left_x - self.profundidade / 2, main_top_y + self.espessura, 
            main_left_x - self.profundidade / 2, main_top_y, 
            main_left_x, main_top_y
        )

        path.push("M", main_right_x, main_bottom_y)

        path.push("L",
            main_right_x + self.profundidade / 2, main_bottom_y,
            main_right_x + self.profundidade / 2, main_bottom_y - self.espessura,
            flap_right_x, main_bottom_y - self.espessura,
            flap_right_x, main_top_y + self.espessura,
            main_right_x + self.profundidade / 2, main_top_y + self.espessura,
            main_right_x + self.profundidade / 2, main_top_y,
            main_right_x, main_top_y
        )

        dwg.add(path) 