import svgwrite

class ExternalLiningBaseComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.w = width_cm * 10
        self.h = height_cm * 10
        self.d = depth_cm * 10
        self.t = thickness_mm
        self._compute_geometry()

    def _compute_geometry(self):
        self.total_width = self.w + 2.5 * self.t
        self.total_height = self.h + 2 * self.t

    def draw(self, dwg, x_offset, y_offset):
        c = 15 # mm
        
        points = [
            (0, self.t),
            (self.t * 0.5, c),
            (self.w - (self.t * 0.5), c),
            (self.w, self.t),
            (self.w + self.t, 2 * self.t),
            (self.w + 1.5 * self.t, c),
            (self.w + self.h - 2 * self.t, c),
            (self.w + self.h - 2 * self.t, 2 * self.t),
            (self.w + self.h - self.t, 2 * self.t),
            (self.w + self.h - self.t, self.t),
            (self.w + self.h - self.t + c, 0),
            (self.w + self.h - self.t + c, -self.d),
            (self.w + self.h - self.t, -self.d - self.t),
            (self.w + self.h - self.t, -self.d - 2 * self.t),
            (self.w + self.h - 2 * self.t, -self.d - 2 * self.t),
            (self.w + self.h - 2 * self.t, -self.d - c),
            (self.w + self.t, -self.d - c),
            (self.w + self.t, - self.d - 2 * self.t),
            (self.w, -self.d - self.t),
            (self.w, -self.d - c),
            (0, -self.d - c),
            (0, -self.d - self.t),
            (-self.t, -self.d - 2 * self.t),
            (-self.t, -self.d - c),
            (-self.h + 2 * self.t, -self.d - c),
            (-self.h + 2 * self.t, -self.d - 2 * self.t),
            (-self.h + self.t, -self.d - 2 * self.t),
            (-self.h + self.t, -self.d - self.t),
            (-self.h + self.t - c, -self.d),
            (-self.h + self.t - c, 0),
            (-self.h + self.t, self.t),
            (-self.h + self.t, 2 * self.t),
            (-self.h + 2 * self.t, 2 * self.t),
            (-self.h + 2 * self.t, c),
            (-self.t * 1.5, c),
            (-self.t, 2 * self.t),
            (0, self.t)
        ]
        path = dwg.path(stroke="navy", fill="none", stroke_width='0.1')
        path.push("M", *points[0])
        for pt in points[1:]:
            path.push("L", *pt)
        dwg.add(path)