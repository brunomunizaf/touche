import svgwrite

class InternalLiningMagnetTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.width = width_cm * 10  # convert to mm
        self.height = height_cm * 10
        self.depth = depth_cm * 10
        self.thickness = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.in_between_spacing = self._get_in_between_spacing(self.thickness)
        self.total_width = self.width
        self.total_height = (self.depth - 5) + self.in_between_spacing + self.height + 42

    def _get_in_between_spacing(self, thickness):
        if 1.5 <= thickness <= 2:
            return 6
        else:
            return 8

    def draw(self, dwg, x_offset, y_offset):
        dwg.add(dwg.polyline([
            (0 + x_offset, 0 + y_offset),
            (self.total_width + x_offset, 0 + y_offset),
            (self.total_width + x_offset, self.total_height + y_offset),
            (0 + x_offset, self.total_height + y_offset),
            (0 + x_offset, 0 + y_offset)
        ], stroke='navy', fill="none", stroke_width='0.1')) 