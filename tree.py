import math
import random

import pygame
from pygame import gfxdraw

from node import Node
from cdgrid import CDGrid


class Tree(object):

	def __init__(self, size, rad, rand_var, rand_mean, rad_lower_lim, boundary_rad=None):
		node1 = Node((-rad, 0), rad)
		node2 = Node(( rad, 0), rad)
		self.cdg = CDGrid(size, rad)
		self.cdg.add(node1)
		self.cdg.add(node2)
		self.node_set = [ node1, node2 ]
		self.edge_set = [(node1, node2)]
		self.edge_batch = self.edge_set[:]
		self.triangle_set = []
		self.rand_var = rand_var
		self.rand_mean = rand_mean
		self.rad_lower_lim = rad_lower_lim
		self.boundary_rad = boundary_rad

	def build(self, iters):
		for i in xrange(iters):
			temp_edge_batch = []

			for node1, node2 in self.edge_batch:
				rand_rat = self.rand_var * (random.random() - 0.5) + self.rand_mean
				node3_rad = ((node1.rad + node2.rad) / 2.) * rand_rat

				if node3_rad < self.rad_lower_lim:
					continue

				# Use Law of Cosines to calculate position of new node
				A = node1.rad + node3_rad
				B = node1.rad + node2.rad
				C = node2.rad + node3_rad
				theta = (math.acos((A*A + B*B - C*C) / float(A*B + A*B)) +
						 math.atan2(node2.y - node1.y, node2.x - node1.x))

				node3 = Node((A * math.cos(theta) + node1.x,
					          A * math.sin(theta) + node1.y),
				             node3_rad)

				# Check node for collision at boundary
				if self.boundary_rad:
					dist = math.sqrt(node3.x * node3.x + node3.y * node3.y)
					if self.boundary_rad < dist + node3.rad:
						continue

				# Check node for collisions with other nodes using the
				# spatial indexer ``cdg'' (collision detector grid)
				addresses = self.cdg.address_node(node3)
				for node in self.cdg.get_neighbors(addresses):
					if Node.intersect(node3, node):
						break

				# If no collisions are detected, we:
				#   (1) add node to our collision detector grid,
				#   (2) add node to our collection of tree nodes,
				#   (3) add "triangle" to our collection of "triangles",
				#   (4) add "edge" to our working batch of "edges".
				else:
					self.cdg.add(node3)
					self.node_set.append(node3)
					self.triangle_set.append((node1, node2, node3))
					temp_edge_batch.extend([(node1, node3), (node3, node2)])

			self.edge_batch = temp_edge_batch[:]
			self.edge_set.extend(temp_edge_batch)

	def draw_nodes(self, surf, color, filled, aalias):
		for node in self.node_set:
			x, y = Node.center_wrt_surf(node.pos, surf)
			if aalias:
				pygame.gfxdraw.aacircle(surf, x, y, int(node.rad), color)
			if filled:
				pygame.gfxdraw.filled_circle(surf, x, y, int(node.rad), color)
			elif not aalias:
				pygame.draw.circle(surf, color, (x, y), int(node.rad), 1)

	def draw_edges(self, surf, color, aalias):
		for (node1, node2) in self.edge_set:
			pos1 = Node.center_wrt_surf(node1.pos, surf)
			pos2 = Node.center_wrt_surf(node2.pos, surf)
			if aalias:
				pygame.draw.aaline(surf, color, pos1, pos2)
			else:
				pygame.draw.line(surf, color, pos1, pos2)

	def draw_triangles(self, surf, color, filled, aalias):
		for (node1, node2, node3) in self.triangle_set:
			pos1 = Node.center_wrt_surf(node1.pos, surf)
			pos2 = Node.center_wrt_surf(node2.pos, surf)
			pos3 = Node.center_wrt_surf(node3.pos, surf)
			if aalias:
				pygame.gfxdraw.aapolygon(surf, (pos1, pos2, pos3), color)
			if filled:
				pygame.gfxdraw.filled_polygon(surf, (pos1, pos2, pos3), color)
			elif not aalias:
				pygame.gfxdraw.polygon(surf, (pos1, pos2, pos3), color)
