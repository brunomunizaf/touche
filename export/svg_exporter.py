import svgwrite

class SVGExporter:
    def __init__(self, width, height):
        # width and height in mm
        self.dwg = svgwrite.Drawing(profile='full', size=(f"{width}mm", f"{height}mm"))
        # Add viewBox to ensure proper scaling
        self.dwg.attribs['viewBox'] = f"0 0 {width} {height}"
    def add_component(self, component, x_offset, y_offset):
        # Draw the component at the given offset
        component.draw(self.dwg, x_offset, y_offset)
    def save(self, filename):
        # Save the SVG to a file
        self.dwg.saveas(filename) 