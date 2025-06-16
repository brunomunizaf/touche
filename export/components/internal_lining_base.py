import svgwrite
import math

class InternalLiningBaseComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.width = width_cm * 10  # convert to mm
        self.height = height_cm * 10
        self.depth = depth_cm * 10
        self.thickness = thickness_mm
        self._compute_size()

    def _compute_size(self):
        # For lining, use the same as the old paper/base_lose.py (internal side)
        self._total_width = self.width + 2 * self.depth
        self._total_height = self.height + 2 * self.depth

    @property
    def total_width(self):
        return self._total_width

    @property
    def total_height(self):
        return self._total_height

    def draw(self, dwg, x_offset, y_offset):
        W = self.width
        D = self.depth
        H = self.height
        T = self.thickness
        
        # Main rectangle corners
        main_left_x = D + x_offset
        main_right_x = main_left_x + W
        main_bottom_y = D + y_offset
        main_top_y = main_bottom_y + H
        
        # Flap edges
        flap_left_x = main_left_x - D
        flap_right_x = main_right_x + D
        flap_bottom_y = main_bottom_y - D
        flap_top_y = main_top_y + D
        
        # Path for all flaps (notched)
        path = dwg.path(stroke="navy", fill="none", stroke_width='0.1')
        
        # Top flap (draw_top)
        top_flap_inner_left_x = main_left_x
        top_flap_inner_right_x = main_right_x
        top_flap_base_y = main_top_y
        top_flap_tip_y = flap_top_y
        top_flap_notch_left_x = top_flap_inner_left_x - T
        top_flap_notch_right_x = top_flap_inner_right_x + T
        top_flap_mid_y = top_flap_base_y + (top_flap_tip_y - top_flap_base_y) / 2
        path.push("M", top_flap_inner_left_x, top_flap_base_y)
        path.push("L", top_flap_notch_left_x, top_flap_base_y, top_flap_notch_left_x, top_flap_mid_y, top_flap_inner_left_x, top_flap_mid_y, top_flap_inner_left_x, top_flap_tip_y, top_flap_inner_right_x, top_flap_tip_y, top_flap_inner_right_x, top_flap_mid_y, top_flap_notch_right_x, top_flap_mid_y, top_flap_notch_right_x, top_flap_base_y, top_flap_inner_right_x, top_flap_base_y)
        
        # Bottom flap (draw_bottom)
        bottom_flap_inner_left_x = main_left_x
        bottom_flap_inner_right_x = main_right_x
        bottom_flap_base_y = main_bottom_y
        bottom_flap_tip_y = flap_bottom_y
        bottom_flap_notch_left_x = bottom_flap_inner_left_x - T
        bottom_flap_notch_right_x = bottom_flap_inner_right_x + T
        bottom_flap_mid_y = bottom_flap_base_y + (bottom_flap_tip_y - bottom_flap_base_y) / 2
        path.push("M", bottom_flap_inner_left_x, bottom_flap_base_y)
        path.push("L", bottom_flap_notch_left_x, bottom_flap_base_y, bottom_flap_notch_left_x, bottom_flap_mid_y, bottom_flap_inner_left_x, bottom_flap_mid_y, bottom_flap_inner_left_x, bottom_flap_tip_y, bottom_flap_inner_right_x, bottom_flap_tip_y, bottom_flap_inner_right_x, bottom_flap_mid_y, bottom_flap_notch_right_x, bottom_flap_mid_y, bottom_flap_notch_right_x, bottom_flap_base_y, bottom_flap_inner_right_x, bottom_flap_base_y)
        
        # Left flap (draw_left)
        left_flap_base_x = flap_left_x
        left_flap_inner_x = main_left_x
        left_flap_bottom_y = main_bottom_y
        left_flap_top_y = main_top_y
        left_flap_tip_y = left_flap_top_y + T
        left_flap_notch_x = left_flap_inner_x - (left_flap_inner_x - left_flap_base_x) / 2
        left_flap_notch_bottom_y = left_flap_bottom_y - T
        path.push("M", left_flap_inner_x, left_flap_bottom_y)
        path.push("L", left_flap_notch_x, left_flap_bottom_y, left_flap_notch_x, left_flap_notch_bottom_y, left_flap_base_x, left_flap_notch_bottom_y, left_flap_base_x, left_flap_tip_y, left_flap_notch_x, left_flap_tip_y, left_flap_notch_x, left_flap_top_y, left_flap_inner_x, left_flap_top_y)
        
        # Right flap (draw_right)
        right_flap_base_x = flap_right_x
        right_flap_inner_x = main_right_x
        right_flap_bottom_y = main_bottom_y
        right_flap_top_y = main_top_y
        right_flap_tip_y = right_flap_top_y + T
        right_flap_notch_x = right_flap_inner_x + (right_flap_base_x - right_flap_inner_x) / 2
        right_flap_notch_bottom_y = right_flap_bottom_y - T
        path.push("M", right_flap_inner_x, right_flap_bottom_y)
        path.push("L", right_flap_notch_x, right_flap_bottom_y, right_flap_notch_x, right_flap_notch_bottom_y, right_flap_base_x, right_flap_notch_bottom_y, right_flap_base_x, right_flap_tip_y, right_flap_notch_x, right_flap_tip_y, right_flap_notch_x, right_flap_top_y, right_flap_inner_x, right_flap_top_y)
        dwg.add(path) 