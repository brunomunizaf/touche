import svgwrite
import math

class CardboardHalfSpineTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.width = width_cm * 10  # convert to mm
        self.height = height_cm * 10
        self.depth = depth_cm * 10
        self.thickness = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.clearance = 10
        self.in_between_spacing = self._get_in_between_spacing(self.thickness)
        self.rect_width = self.width + self.clearance
        self.total_width = self.rect_width
        # Altura total: aba (meia profundidade - 5), painel (altura), lombada (meia profundidade)
        self.flap_height = (self.depth / 2) - 5
        self.panel_height = self.height
        self.spine_height = self.depth / 2
        self.total_height = (
            self.flap_height + self.in_between_spacing + self.panel_height + self.in_between_spacing + self.spine_height
        )

    def _get_in_between_spacing(self, thickness):
        if 1.5 <= thickness <= 2:
            return 6
        else:
            return 8

    def _get_magnets_x(self, left_x, right_x, width):
        if 150 <= width <= 200:
            xL = left_x + 30
            xR = right_x - 30
        elif 200 < width <= 300:
            xL = left_x + 40
            xR = right_x - 40
        else:
            xL = left_x + 45
            xR = right_x - 45
        return xL, xR

    def draw(self, dwg, x_offset, y_offset):
        left_x = x_offset
        right_x = left_x + self.rect_width

        # Flap (meia profundidade - 5)
        flap_top_y = y_offset
        flap_bottom_y = flap_top_y + self.flap_height

        # Painel (altura)
        panel_top_y = flap_bottom_y + self.in_between_spacing
        panel_bottom_y = panel_top_y + self.panel_height

        # Spine (meia profundidade)
        spine_top_y = panel_bottom_y + self.in_between_spacing
        spine_bottom_y = spine_top_y + self.spine_height

        # Desenhar as três partes
        for top_y, bottom_y in [
            (flap_top_y, flap_bottom_y),
            (panel_top_y, panel_bottom_y),
            (spine_top_y, spine_bottom_y)
        ]:
            dwg.add(dwg.polyline([
                (left_x, top_y),
                (right_x, top_y),
                (right_x, bottom_y),
                (left_x, bottom_y),
                (left_x, top_y)
            ], stroke="black", fill="none", stroke_width='0.1'))

        # Adicionar ímãs na aba
        width = self.width
        magnet_radius = 7
        if width + self.clearance > 100:
            xLM, xRM = self._get_magnets_x(left_x + (self.clearance/2), right_x - (self.clearance/2), width)
            yM = flap_top_y + 30 if self.flap_height >= 100 else flap_top_y + self.flap_height / 2
            dwg.add(dwg.circle(center=(xLM, yM), r=magnet_radius, fill="none", stroke="black", stroke_width=0.1))
            dwg.add(dwg.circle(center=(xRM, yM), r=magnet_radius, fill="none", stroke="black", stroke_width=0.1))
        else:
            xM = left_x + (right_x - left_x) / 2
            yM = flap_top_y + self.flap_height / 2
            dwg.add(dwg.circle(center=(xM, yM), r=magnet_radius, fill="none", stroke="black", stroke_width=0.1)) 