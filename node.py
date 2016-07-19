class Node(object):

	def __init__(self, (x, y), rad):
		self.x = x
		self.y = y
		self.pos = (x, y)
		self.rad = rad

	def distance(self, node):
		dx = self.x - node.x
		dy = self.y - node.y
		return (dx * dx + dy * dy) ** 0.5

	def intersect(self, node):
		return self.distance(node) <= self.rad + node.rad - 1		

	@staticmethod
	def center_wrt_surf(pos, surf):
		x, y = pos
		cx =  x + surf.get_width() / 2.
		cy = -y + surf.get_height() / 2.
		return map(int, (cx, cy))
