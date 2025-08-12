import svgwrite

class CardboardBaseComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm, with_magnets=False):
        self.width_cm = width_cm
        self.height_cm = height_cm
        self.depth_cm = depth_cm
        self.thickness_mm = thickness_mm
        self.with_magnets = with_magnets
        self.width = width_cm * 10  # convert to mm
        self.height = height_cm * 10
        self.depth = depth_cm * 10
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

    def get_magnets_x(self, x0, x1, W):
        if 150 <= W <= 200:
            xL = x0 + 30
            xR = x1 - 30
        elif 200 < W <= 300:
            xL = x0 + 40
            xR = x1 - 40
        else:
            xL = x0 + 45
            xR = x1 - 45
        return xL, xR

    def draw_magnet(self, x, y, radius, dwg, color):
        dwg.add(dwg.circle(
            center=(x, y),
            r=radius,
            stroke=color,
            fill="none",
            stroke_width='0.1'
        ))

    def draw(self, dwg, x_offset, y_offset):
        main_left_x = self.depth + x_offset
        main_right_x = main_left_x + self.width
        main_bottom_y = self.depth + y_offset
        main_top_y = main_bottom_y + self.height
        flap_left_x = main_left_x - self.depth
        flap_right_x = main_right_x + self.depth
        flap_bottom_y = main_bottom_y - self.depth
        flap_top_y = main_top_y + self.depth
        t = self.thickness_mm

        dwg.add(dwg.polyline([
            (main_left_x, main_bottom_y),
            (main_right_x, main_bottom_y),
            (main_right_x, main_top_y),
            (main_left_x, main_top_y),
            (main_left_x, main_bottom_y)
        ], stroke="red", fill="none", stroke_width='0.1'))

        path = dwg.path(stroke="black", fill="none", stroke_width='0.1')

        path.push("M", main_left_x, main_top_y)

        path.push("L", main_left_x - t, main_top_y, main_left_x - t, main_top_y + self.depth / 2, main_left_x, main_top_y + self.depth / 2, main_left_x, flap_top_y,
                  main_right_x, flap_top_y, main_right_x, main_top_y + self.depth / 2, main_right_x + t, main_top_y + self.depth / 2, main_right_x + t, main_top_y, main_right_x, main_top_y)

        path.push("M", main_left_x, main_bottom_y)

        path.push("L", main_left_x - t, main_bottom_y, main_left_x - t, main_bottom_y - self.depth / 2, main_left_x, main_bottom_y - self.depth / 2, main_left_x, flap_bottom_y,
                  main_right_x, flap_bottom_y, main_right_x, main_bottom_y - self.depth / 2, main_right_x + t, main_bottom_y - self.depth / 2, main_right_x + t, main_bottom_y, main_right_x, main_bottom_y)

        path.push("M", main_left_x, main_bottom_y)

        path.push("L", main_left_x - self.depth / 2, main_bottom_y, main_left_x - self.depth / 2, main_bottom_y - t, flap_left_x, main_bottom_y - t,
                  flap_left_x, main_top_y + t, main_left_x - self.depth / 2, main_top_y + t, main_left_x - self.depth / 2, main_top_y, main_left_x, main_top_y)

        path.push("M", main_right_x, main_bottom_y)

        path.push("L", flap_right_x - self.depth / 2, main_bottom_y, flap_right_x - self.depth / 2, main_bottom_y - t, flap_right_x, main_bottom_y - t,
                  flap_right_x, main_top_y + t, flap_right_x - self.depth / 2, main_top_y + t, flap_right_x - self.depth / 2, main_top_y, main_right_x, main_top_y)

        dwg.add(path)

        # Draw magnets if requested
        if self.with_magnets:
            magnet_radius = 7  # 7mm radius
            
            # Calculate Y position based on depth
            if self.depth >= 100:
                yM = main_top_y + 30
            else:
                yM = main_top_y + (self.depth / 2)
            
            if self.width + 15 > 100:
                xL, xR = self.get_magnets_x(main_left_x, main_right_x, self.width)
                self.draw_magnet(xL, yM, magnet_radius, dwg, 'black')
                self.draw_magnet(xR, yM, magnet_radius, dwg, 'black')
            else:
                xM = main_left_x + (main_right_x - main_left_x) / 2
                self.draw_magnet(xM, yM, magnet_radius, dwg, 'black') 