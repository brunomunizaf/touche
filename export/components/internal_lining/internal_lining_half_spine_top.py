import svgwrite
import math

class InternalLiningHalfSpineTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.width = width_cm * 10  # convert to mm
        self.height = height_cm * 10
        self.depth = depth_cm * 10
        self.thickness = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.clearance = 15
        self.in_between_spacing = self._get_in_between_spacing(self.thickness)
        self.rect_width = self.width + self.clearance
        self.total_width = self.rect_width
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
            ], stroke="navy", fill="none", stroke_width='0.1')) 