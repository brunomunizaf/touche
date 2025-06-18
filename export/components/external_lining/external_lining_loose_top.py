import svgwrite

class ExternalLiningLooseTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.w = width_cm * 10
        self.h = height_cm * 10
        self.d = depth_cm * 10
        self.t = thickness_mm
        self._compute_geometry()

    def _compute_geometry(self):
        self.outer_offset_mm = 15
        self.spacing_between_panels_mm = self._get_spacing_between_panels(self.t)
        self.panel_height_mm = self.h + 10
        self.panel_width_mm = self.w + 15
        
        # Calculate all y positions
        self.top_inner_y = self.outer_offset_mm
        self.top_panel_end_y = self.top_inner_y + self.panel_height_mm
        self.top_spacing_end_y = self.top_panel_end_y + self.spacing_between_panels_mm
        self.spine_panel_end_y = self.top_spacing_end_y + self.d
        self.bottom_spacing_start_y = self.spine_panel_end_y + self.spacing_between_panels_mm
        self.bottom_panel_end_y = self.bottom_spacing_start_y + self.panel_height_mm
        
        # Calculate all x positions
        self.left_inner_x = self.outer_offset_mm
        self.right_inner_x = self.left_inner_x + self.panel_width_mm
        self.left_outer_x = 0
        self.right_outer_x = self.right_inner_x + self.outer_offset_mm
        self.top_outer_y = 0
        self.bottom_outer_y = self.bottom_panel_end_y + self.outer_offset_mm
        
        self.total_width = self.right_outer_x
        self.total_height = self.bottom_outer_y

    def _get_spacing_between_panels(self, thickness):
        if 1.5 <= thickness <= 2:
            return 6
        else:
            return 8

    def draw(self, dwg, x_offset, y_offset):
        c = 15  # corner radius in mm
        
        # Draw top panel
        points = [
            (self.left_inner_x, self.top_inner_y + self.t),
            (self.left_inner_x + self.t * 0.5, self.top_inner_y + c),
            (self.right_inner_x - (self.t * 0.5), self.top_inner_y + c),
            (self.right_inner_x, self.top_inner_y + self.t),
            (self.right_inner_x + self.t, self.top_inner_y + 2 * self.t),
            (self.right_inner_x + 1.5 * self.t, self.top_inner_y + c),
            (self.right_inner_x + self.h - 2 * self.t, self.top_inner_y + c),
            (self.right_inner_x + self.h - 2 * self.t, self.top_inner_y + 2 * self.t),
            (self.right_inner_x + self.h - self.t, self.top_inner_y + 2 * self.t),
            (self.right_inner_x + self.h - self.t, self.top_inner_y + self.t),
            (self.right_inner_x + self.h - self.t + c, self.top_inner_y),
            (self.right_inner_x + self.h - self.t + c, self.top_inner_y - self.d),
            (self.right_inner_x + self.h - self.t, self.top_inner_y - self.d - self.t),
            (self.right_inner_x + self.h - self.t, self.top_inner_y - self.d - 2 * self.t),
            (self.right_inner_x + self.h - 2 * self.t, self.top_inner_y - self.d - 2 * self.t),
            (self.right_inner_x + self.h - 2 * self.t, self.top_inner_y - self.d - c),
            (self.right_inner_x + self.t, self.top_inner_y - self.d - c),
            (self.right_inner_x + self.t, self.top_inner_y - self.d - 2 * self.t),
            (self.right_inner_x, self.top_inner_y - self.d - self.t),
            (self.right_inner_x, self.top_inner_y - self.d - c),
            (self.left_inner_x, self.top_inner_y - self.d - c),
            (self.left_inner_x, self.top_inner_y - self.d - self.t),
            (self.left_inner_x - self.t, self.top_inner_y - self.d - 2 * self.t),
            (self.left_inner_x - self.t, self.top_inner_y - self.d - c),
            (self.left_inner_x - self.h + 2 * self.t, self.top_inner_y - self.d - c),
            (self.left_inner_x - self.h + 2 * self.t, self.top_inner_y - self.d - 2 * self.t),
            (self.left_inner_x - self.h + self.t, self.top_inner_y - self.d - 2 * self.t),
            (self.left_inner_x - self.h + self.t, self.top_inner_y - self.d - self.t),
            (self.left_inner_x - self.h + self.t - c, self.top_inner_y - self.d),
            (self.left_inner_x - self.h + self.t - c, self.top_inner_y),
            (self.left_inner_x - self.h + self.t, self.top_inner_y + self.t),
            (self.left_inner_x - self.h + self.t, self.top_inner_y + 2 * self.t),
            (self.left_inner_x - self.h + 2 * self.t, self.top_inner_y + 2 * self.t),
            (self.left_inner_x - self.h + 2 * self.t, self.top_inner_y + c),
            (self.left_inner_x - self.t * 1.5, self.top_inner_y + c),
            (self.left_inner_x - self.t, self.top_inner_y + 2 * self.t),
            (self.left_inner_x, self.top_inner_y + self.t)
        ]
        
        # Apply offsets
        points = [(x + x_offset, y + y_offset) for x, y in points]
        
        path = dwg.path(stroke="navy", fill="none", stroke_width='0.1')
        path.push("M", *points[0])
        for pt in points[1:]:
            path.push("L", *pt)
        dwg.add(path) 