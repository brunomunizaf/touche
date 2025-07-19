import svgwrite
import math

class InternalLiningBaseForSleeveTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.width = width_cm * 10  # convert to mm
        self.height = height_cm * 10
        self.depth = depth_cm * 10
        self.thickness = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.clearance = self._get_clearance(self.thickness)
        self.base_width = self.width + self.clearance
        self.base_height = self.height + self.clearance
        self.base_depth = self.depth + self.clearance
        self._total_width = self.base_width + 2 * self.base_depth
        self._total_height = self.base_height + 2 * self.base_depth

    @property
    def total_width(self):
        return self._total_width

    @property
    def total_height(self):
        return self._total_height

    def _get_clearance(self, thickness):
        if thickness in (1.90, 2.00):
            return 7.0
        elif thickness == 2.50:
            return 8.0
        else:
            return thickness * 3

    def draw(self, dwg, x_offset, y_offset):
        main_left_x = self.base_depth + x_offset
        main_right_x = main_left_x + self.base_width
        main_bottom_y = self.base_depth + y_offset
        main_top_y = main_bottom_y + self.base_height
        flap_left_x = main_left_x - self.base_depth
        flap_right_x = main_right_x + self.base_depth
        flap_bottom_y = main_bottom_y - self.base_depth
        flap_top_y = main_top_y + self.base_depth
        t = self.thickness

        # Main base outline
        dwg.add(dwg.polyline([
            (main_left_x, main_bottom_y),
            (main_right_x, main_bottom_y),
            (main_right_x, main_top_y),
            (main_left_x, main_top_y),
            (main_left_x, main_bottom_y)
        ], stroke="red", fill="none", stroke_width='0.1'))

        path = dwg.path(stroke="black", fill="none", stroke_width='0.1')

        # Top flap with fold lines
        path.push("M", main_left_x, main_top_y)
        path.push("L", main_left_x - t, main_top_y, main_left_x - t, main_top_y + self.base_depth / 2, 
                  main_left_x, main_top_y + self.base_depth / 2, main_left_x, flap_top_y,
                  main_right_x, flap_top_y, main_right_x, main_top_y + self.base_depth / 2, 
                  main_right_x + t, main_top_y + self.base_depth / 2, main_right_x + t, main_top_y, 
                  main_right_x, main_top_y)

        # Bottom flap with fold lines
        path.push("M", main_left_x, main_bottom_y)
        path.push("L", main_left_x - t, main_bottom_y, main_left_x - t, main_bottom_y - self.base_depth / 2, 
                  main_left_x, main_bottom_y - self.base_depth / 2, main_left_x, flap_bottom_y,
                  main_right_x, flap_bottom_y, main_right_x, main_bottom_y - self.base_depth / 2, 
                  main_right_x + t, main_bottom_y - self.base_depth / 2, main_right_x + t, main_bottom_y, 
                  main_right_x, main_bottom_y)

        # Left flap with fold lines
        path.push("M", main_left_x, main_bottom_y)
        path.push("L", main_left_x - self.base_depth / 2, main_bottom_y, 
                  main_left_x - self.base_depth / 2, main_bottom_y - t, flap_left_x, main_bottom_y - t,
                  flap_left_x, main_top_y + t, main_left_x - self.base_depth / 2, main_top_y + t, 
                  main_left_x - self.base_depth / 2, main_top_y, main_left_x, main_top_y)

        # Right flap with fold lines
        path.push("M", main_right_x, main_bottom_y)
        path.push("L", flap_right_x - self.base_depth / 2, main_bottom_y, 
                  flap_right_x - self.base_depth / 2, main_bottom_y - t, flap_right_x, main_bottom_y - t,
                  flap_right_x, main_top_y + t, flap_right_x - self.base_depth / 2, main_top_y + t, 
                  flap_right_x - self.base_depth / 2, main_top_y, main_right_x, main_top_y)

        dwg.add(path) 