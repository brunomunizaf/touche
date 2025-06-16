class BoxLayout:
    def __init__(self, components, spacing=10):
        self.components = components
        self.spacing = spacing
    def arrange(self):
        # Arrange components vertically with spacing between them
        current_y = 0
        layout = []
        for i, comp in enumerate(self.components):
            layout.append((comp, 0, current_y))
            current_y += comp.total_height
            if i < len(self.components) - 1:
                current_y += self.spacing
        return layout 