import svgwrite
import math

class InternalLiningBookTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.width = width_cm * 10  # convert to mm
        self.height = height_cm * 10
        self.depth = depth_cm * 10
        self.thickness = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.in_between_spacing = self._get_in_between_spacing(self.thickness)
        self.offset = 15 / 2
        self.rect_width = self.width + 15
        self.rect_height = self.height + 10
        self.total_width = self.rect_width
        self.total_height = self.height + 36

    def _get_in_between_spacing(self, thickness):
        if 1.5 <= thickness <= 2:
            return 6
        else:
            return 8

    def draw(self, dwg, x_offset, y_offset):
        # Internal lining is a simple rectangle (see paper/top_book.py, internal branch)
        left_x = x_offset + self.offset
        right_x = left_x + self.rect_width - self.offset * 2
        top_y = y_offset
        bottom_y = top_y + self.height + 36
        dwg.add(dwg.polyline([
            (0, 0),
            (right_x - left_x, 0),
            (right_x - left_x, bottom_y - top_y),
            (0, bottom_y - top_y),
            (0, 0)
        ], stroke='navy', fill="none", stroke_width='0.1')) 