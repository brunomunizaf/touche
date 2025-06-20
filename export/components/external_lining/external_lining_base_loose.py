import svgwrite

class ExternalLiningBaseLooseComponent:
    def __init__(self, width_cm, height_cm, depth_cm, thickness_mm):
        self.w = width_cm * 10
        self.h = height_cm * 10
        self.d = depth_cm * 10
        self.t = thickness_mm
        self._compute_geometry()

    def _compute_geometry(self):
        paper_clearance = 15
        self.total_width = self.d + paper_clearance + self.w + self.d + paper_clearance
        self.total_height = self.d + paper_clearance + self.h + self.d + paper_clearance

    def draw(self, dwg, x_offset, y_offset):
        paper_clearance = 15

        W = self.w
        H = self.h
        D = self.d
        T = self.t

        x0 = D + paper_clearance + x_offset
        x1 = x0 + W
        xL = x0 - D
        xR = x1 + D
        xRR = xR + paper_clearance

        y0 = D + paper_clearance + y_offset
        y1 = y0 + H
        yB = y0 - D
        yT = y1 + D
        yTT = yT + paper_clearance

        path = dwg.path(
            stroke="navy",
            fill="none",
            stroke_width='0.1'
        )

        path.push("M", xR + paper_clearance, y1)
        path.push("L", xR + paper_clearance, y0)
        path.push("L", xR + 6, y0)
        path.push("L", xR + 3, y0 - 1.5)
        path.push("L", x1 + T + 0.5, y0 - 1.5)
        path.push("L", x1 + T + paper_clearance, y0 - 3.5)
        path.push("L", x1 + T + paper_clearance, yB - 1.2)
        path.push("L", x1 + 1.9, yB - 3.1)
        path.push("L", x1 + 1.9, yB - 5)
        path.push("L", x1, yB - 5)
        path.push("L", x1, yB - paper_clearance)
        path.push("L", x0, yB - paper_clearance)
        path.push("L", x0, yB - 5)
        path.push("L", x0 - 1.9, yB - 5)
        path.push("L", x0 - 1.9, yB - 3.1)
        path.push("L", x0 - T - paper_clearance, yB - 1.2)
        path.push("L", x0 - T - paper_clearance, y0 - 3.5)
        path.push("L", x0 - T - 0.5, y0 - 1.5)
        path.push("L", xL - 3, y0 - 1.5)
        path.push("L", xL - 6, y0)
        path.push("L", xL - paper_clearance, y0)
        path.push("L", xL - paper_clearance, y1)

        path.push("L", xL - 6, y1)
        path.push("L", xL - 3, y1 + 1.5)
        path.push("L", x0 - T - 0.5, y1 + 1.5)
        path.push("L", x0 - T - paper_clearance, y1 + 3.5)
        path.push("L", x0 - T - paper_clearance, yT + 1.2)
        path.push("L", x0 - 1.9, yT + 3.1)
        path.push("L", x0 - 1.9, yT + 5)
        path.push("L", x0, yT + 5)
        path.push("L", x0, yT + paper_clearance)
        path.push("L", x1, yT + paper_clearance)
        path.push("L", x1, yT + 5)
        path.push("L", x1 + 1.9, yT + 5)
        path.push("L", x1 + 1.9, yT + 3.1)
        path.push("L", x1 + T + paper_clearance, yT + 1.2)
        path.push("L", x1 + T + paper_clearance, y1 + 3.5)
        path.push("L", x1 + T + 0.5, y1 + 1.5)
        path.push("L", xR + 3, y1 + 1.5)
        path.push("L", xR + 6, y1)
        path.push("L", xR + 15, y1)

        dwg.add(path)