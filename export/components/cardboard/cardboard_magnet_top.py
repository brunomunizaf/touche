import svgwrite
import math

class CardboardMagnetTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.width = width_cm * 10  # convert to mm
        self.height = height_cm * 10
        self.depth = depth_cm * 10
        self.thickness = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.clearance = 15
        self.in_between_spacing = self._get_in_between_spacing(self.thickness)
        self.magnet_radius = 7
        self.rect_width = self.width + self.clearance
        self.total_width = self.rect_width
        # Estimate total height for layout
        self.total_height = (
            (self.depth - 5) + self.in_between_spacing + self.height + self.in_between_spacing + self.depth + self.in_between_spacing + self.height + 7
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
        
        # Rectangle heights
        first_rect_top_y = y_offset
        first_rect_bottom_y = first_rect_top_y + self.depth - 5
        second_rect_top_y = first_rect_bottom_y + self.in_between_spacing
        second_rect_bottom_y = second_rect_top_y + self.height
        third_rect_top_y = second_rect_bottom_y + self.in_between_spacing
        third_rect_bottom_y = third_rect_top_y + self.depth
        fourth_rect_top_y = third_rect_bottom_y + self.in_between_spacing
        fourth_rect_bottom_y = fourth_rect_top_y + self.height + 7
        
        # Draw four rectangles stacked vertically
        for top_y, bottom_y in [
            (first_rect_top_y, first_rect_bottom_y),
            (second_rect_top_y, second_rect_bottom_y),
            (third_rect_top_y, third_rect_bottom_y),
            (fourth_rect_top_y, fourth_rect_bottom_y)
        ]:
            dwg.add(dwg.polyline([
                (left_x, top_y),
                (right_x, top_y),
                (right_x, bottom_y),
                (left_x, bottom_y),
                (left_x, top_y)
            ], stroke="black", fill="none", stroke_width='0.1'))
        
        # Draw magnets on the first rectangle
        width = self.width
        if width + self.clearance > 100:
            xLM, xRM = self._get_magnets_x(left_x + (self.clearance/2), right_x - (self.clearance/2), width)
            yM = first_rect_top_y + 30 if self.depth >= 100 else first_rect_top_y + (self.depth - 5) / 2
            dwg.add(dwg.circle(center=(xLM, yM), r=self.magnet_radius, fill="none", stroke="black", stroke_width=0.1))
            dwg.add(dwg.circle(center=(xRM, yM), r=self.magnet_radius, fill="none", stroke="black", stroke_width=0.1))
        else:
            xM = left_x + (right_x - left_x) / 2
            yM = first_rect_top_y + (self.depth - 5) / 2
            dwg.add(dwg.circle(center=(xM, yM), r=self.magnet_radius, fill="none", stroke="black", stroke_width=0.1)) 