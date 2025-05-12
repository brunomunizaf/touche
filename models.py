class Box:
	def __init__(
		self, 
		client_name, 
		width, 
		height, 
		depth, 
		thickness
	):
		self.client_name = client_name
		self.width = width
		self.height = height
		self.depth = depth
		self.thickness = thickness

class ExportBundle:
	def __init__(
		self,
		svg_string,
		file_name
	):
		self.svg_string = svg_string
		self.file_name = file_name