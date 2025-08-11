class CardboardBookTopComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.width = width_cm * 10  # convert to mm
        self.height = height_cm * 10
        self.depth = depth_cm * 10
        self.thickness = thickness_mm
        self._compute_size()

    def _compute_size(self):
        self.in_between_spacing = self._get_in_between_spacing(self.thickness)
        self.offset = 0
        self.rect_width = self.width + 15
        self.rect_height = self.height + 10
        self.total_width = self.rect_width
        self.total_height = (
            self.rect_height * 2 + self.depth + self.in_between_spacing * 2
        )

    def _get_in_between_spacing(self, thickness):
        if 1.5 <= thickness <= 2:
            return 6
        else:
            return 8

    def draw(self, dwg, x_offset, y_offset):
        left_x = x_offset
        right_x = left_x + self.rect_width

        # First rectangle (top panel)
        first_rect_top_y = y_offset
        first_rect_bottom_y = first_rect_top_y + self.rect_height

        # Middle rectangle (spine)
        middle_rect_top_y = first_rect_bottom_y + self.in_between_spacing
        middle_rect_bottom_y = middle_rect_top_y + self.depth

        # Bottom rectangle (bottom panel)
        bottom_rect_top_y = middle_rect_bottom_y + self.in_between_spacing
        bottom_rect_bottom_y = bottom_rect_top_y + self.rect_height

        # Draw three rectangles stacked vertically
        for top_y, bottom_y in [
            (first_rect_top_y, first_rect_bottom_y),
            (middle_rect_top_y, middle_rect_bottom_y),
            (bottom_rect_top_y, bottom_rect_bottom_y)
        ]:
            dwg.add(dwg.polyline([
                (left_x, top_y),
                (right_x, top_y),
                (right_x, bottom_y),
                (left_x, bottom_y),
                (left_x, top_y)
            ], stroke="black", fill="none", stroke_width='0.1')) 