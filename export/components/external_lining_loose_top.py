import svgwrite

class ExternalLiningLooseTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.box_width_mm = width_cm * 10  # convert to mm
        self.box_height_mm = height_cm * 10
        self.box_depth_mm = depth_cm * 10
        self.cardboard_thickness_mm = thickness_mm
        self._compute_geometry()

    def _compute_geometry(self):
        self.outer_offset_mm = 15
        self.spacing_between_panels_mm = self._get_spacing_between_panels(self.cardboard_thickness_mm)
        self.panel_height_mm = self.box_height_mm + 10
        self.panel_width_mm = self.box_width_mm + 15
        # Calculate all y positions
        self.top_inner_y = self.outer_offset_mm
        self.top_panel_end_y = self.top_inner_y + self.panel_height_mm
        self.top_spacing_end_y = self.top_panel_end_y + self.spacing_between_panels_mm
        self.spine_panel_end_y = self.top_spacing_end_y + self.box_depth_mm
        self.bottom_spacing_start_y = self.spine_panel_end_y + self.spacing_between_panels_mm
        self.bottom_panel_end_y = self.bottom_spacing_start_y + self.panel_height_mm
        # Calculate all x positions
        self.left_inner_x = self.outer_offset_mm
        self.right_inner_x = self.left_inner_x + self.box_width_mm + 15
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
        # External lining is a simple rectangle
        points = [
            (self.left_outer_x + x_offset, self.top_outer_y + y_offset),
            (self.right_outer_x + x_offset, self.top_outer_y + y_offset),
            (self.right_outer_x + x_offset, self.bottom_outer_y + y_offset),
            (self.left_outer_x + x_offset, self.bottom_outer_y + y_offset),
            (self.left_outer_x + x_offset, self.top_outer_y + y_offset)
        ]
        path = dwg.path(stroke="navy", fill="none", stroke_width='0.1')
        path.push("M", *points[0])
        for pt in points[1:]:
            path.push("L", *pt)
        dwg.add(path) 