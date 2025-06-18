import svgwrite
import math

class InternalLiningBaseForBookTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.width = width_cm * 10  # convert to mm
        self.height = height_cm * 10
        self.depth = depth_cm * 10
        self.thickness = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self._total_width = self.width + 2 * self.depth
        self._total_height = self.height + 2 * self.depth

    @property
    def total_width(self):
        return self._total_width

    @property
    def total_height(self):
        return self._total_height
    
    def draw(self, dwg, x_offset, y_offset):
        main_left_x = self.depth + x_offset
        main_right_x = main_left_x + self.width
        main_bottom_y = self.depth + y_offset
        main_top_y = main_bottom_y + self.height
        flap_left_x = main_left_x - self.depth
        flap_right_x = main_right_x + self.depth
        flap_bottom_y = main_bottom_y - self.depth
        flap_top_y = main_top_y + self.depth
        t = self.thickness
        clearance = 15

        path = dwg.path(stroke="navy", fill="none", stroke_width='0.1')

        path.push("M", main_left_x, main_top_y)

        path.push("L", 
                  main_left_x - t, main_top_y, 
                  main_left_x - t, main_top_y + self.depth / 2, 
                  main_left_x, main_top_y + self.depth / 2, 
                  main_left_x, flap_top_y + clearance,
                  main_right_x, flap_top_y + clearance, 
                  main_right_x, main_top_y + self.depth / 2, 
                  main_right_x + t, main_top_y + self.depth / 2, 
                  main_right_x + t, main_top_y, 
                  main_right_x, main_top_y
                  )

        path.push("M", main_left_x, main_bottom_y)

        path.push("L", 
                  main_left_x - t, main_bottom_y, 
                  main_left_x - t, main_bottom_y - self.depth / 2, 
                  main_left_x, main_bottom_y - self.depth / 2, 
                  main_left_x, flap_bottom_y,
                  main_right_x, flap_bottom_y, 
                  main_right_x, main_bottom_y - self.depth / 2, 
                  main_right_x + t, main_bottom_y - self.depth / 2, 
                  main_right_x + t, main_bottom_y, 
                  main_right_x, main_bottom_y
                  )

        path.push("M", main_left_x, main_bottom_y)

        path.push("L", 
                  main_left_x - self.depth / 2, main_bottom_y, 
                  main_left_x - self.depth / 2, main_bottom_y - t, 
                  flap_left_x, main_bottom_y - t,
                  flap_left_x, main_top_y + t, 
                  main_left_x - self.depth / 2, main_top_y + t, 
                  main_left_x - self.depth / 2, main_top_y, 
                  main_left_x, main_top_y
                  )

        path.push("M", main_right_x, main_bottom_y)

        path.push("L", 
                  flap_right_x - self.depth / 2, main_bottom_y, 
                  flap_right_x - self.depth / 2, main_bottom_y - t, 
                  flap_right_x, main_bottom_y - t,
                  flap_right_x, main_top_y + t, 
                  flap_right_x - self.depth / 2, main_top_y + t, 
                  flap_right_x - self.depth / 2, main_top_y, 
                  main_right_x, main_top_y
                  )

        dwg.add(path) 