import svgwrite

class SVGExporter:
    def __init__(self, width, height):
        # width and height in mm
        self.dwg = svgwrite.Drawing(size=(f"{width}mm", f"{height}mm"))
    def add_component(self, component, x_offset, y_offset):
        # Draw the component at the given offset
        component.draw(self.dwg, x_offset, y_offset)
    def save(self, filename):
        # Save the SVG to a file
        self.dwg.saveas(filename) 