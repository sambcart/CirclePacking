class CDGrid(object):

	def __init__(self, size, max_rad):
		self.surf_size = size
		self.cell_size = int(2 * max_rad)
		self.node_list = []
		self.grid = {}

		p = size / self.cell_size + 1
		for i in xrange(-1,p+1):
			for j in xrange(-1,p+1):
				self.grid[i,j] = []

	def address_node(self, node):
		xi = (int(node.x) + self.surf_size / 2) / self.cell_size
		yi = (int(node.y) + self.surf_size / 2) / self.cell_size
		return [(xi-1, yi-1), (xi, yi-1), (xi+1, yi-1),
		        (xi-1, yi),   (xi, yi),   (xi+1, yi),
		        (xi-1, yi+1), (xi, yi+1), (xi+1, yi+1)]

	def add(self, node):
		self.node_list.append(node)
		for address in self.address_node(node):
			self.grid[address].append(node)

	def get_neighbors(self, addresses):
		for address in addresses:
			for neighbor in self.grid[address]:
				yield neighbor
