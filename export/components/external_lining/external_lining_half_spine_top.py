import svgwrite
import math

class ExternalLiningHalfSpineTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.box_width_mm = width_cm * 10  # convert to mm
        self.box_height_mm = height_cm * 10
        self.box_depth_mm = depth_cm * 10
        self.cardboard_thickness_mm = thickness_mm
        self._compute_geometry()

    def _compute_geometry(self):
        self.outer_offset_mm = 15
        self.spacing_between_panels_mm = self._get_spacing_between_panels(self.cardboard_thickness_mm)
        self.panel_height_mm = self.box_height_mm
        self.panel_width_mm = self.box_width_mm + self.outer_offset_mm
        self.flap_height_mm = (self.box_depth_mm / 2) - 5
        self.spine_panel_height_mm = self.box_depth_mm / 2
        self.total_width = self.panel_width_mm
        self.total_height = (
            self.flap_height_mm + self.spacing_between_panels_mm + self.panel_height_mm + self.spacing_between_panels_mm + self.spine_panel_height_mm
        )

    def _get_spacing_between_panels(self, thickness):
        if 1.5 <= thickness <= 2:
            return 6
        else:
            return 8

    def draw(self, dwg, x_offset, y_offset):
        left_x = x_offset
        right_x = left_x + self.total_width

        # Flap (meia profundidade - 5)
        flap_top_y = y_offset
        flap_bottom_y = flap_top_y + self.flap_height_mm

        # Painel (altura)
        panel_top_y = flap_bottom_y + self.spacing_between_panels_mm
        panel_bottom_y = panel_top_y + self.panel_height_mm

        # Spine (meia profundidade)
        spine_top_y = panel_bottom_y + self.spacing_between_panels_mm
        spine_bottom_y = spine_top_y + self.spine_panel_height_mm

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