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

class MultiInstanceLayout:
    def __init__(self, components, instances, spacing=10, margin=20):
        self.components = components
        self.instances = instances
        self.spacing = spacing
        self.margin = margin
        self._compute_grid()
    
    def _compute_grid(self):
        # Calculate total width and height of all components
        total_comp_width = max(comp.total_width for comp in self.components)
        total_comp_height = sum(comp.total_height for comp in self.components) + self.spacing * (len(self.components) - 1)
        
        # Calculate grid dimensions
        import math
        grid_cols = math.ceil(math.sqrt(self.instances))
        grid_rows = math.ceil(self.instances / grid_cols)
        
        # Calculate total layout dimensions
        self.total_width = grid_cols * total_comp_width + (grid_cols - 1) * self.spacing + 2 * self.margin
        self.total_height = grid_rows * total_comp_height + (grid_rows - 1) * self.spacing + 2 * self.margin
        
        # Store grid info for background rectangle
        self.grid_cols = grid_cols
        self.grid_rows = grid_rows
        self.component_width = total_comp_width
        self.component_height = total_comp_height
    
    def arrange(self):
        # Arrange multiple instances in a grid
        layout = []
        instance_count = 0
        
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if instance_count >= self.instances:
                    break
                    
                x_offset = self.margin + col * (self.component_width + self.spacing)
                y_offset = self.margin + row * (self.component_height + self.spacing)
                
                # Add all components for this instance
                current_y = y_offset
                for comp in self.components:
                    layout.append((comp, x_offset, current_y))
                    current_y += comp.total_height
                    if comp != self.components[-1]:
                        current_y += self.spacing
                
                instance_count += 1
            
            if instance_count >= self.instances:
                break
        
        return layout
    
    def get_background_rectangle(self):
        """Returns the dimensions for the background rectangle representing the full cardboard"""
        return {
            'x': 0,
            'y': 0,
            'width': self.total_width,
            'height': self.total_height
        } 