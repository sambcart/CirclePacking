import math
import random
import pygame
from pygame import gfxdraw
from node import Node
from collision import CollisionDetectionGrid as CDG

class Tree(object):

    def __init__(self, size, rad, rand_var, rand_mean, rad_lower_lim, boundary_rad=None):
        node1 = Node((-rad, 0), rad)
        node2 = Node(( rad, 0), rad)
        self.size = size
        self.cdg = CDG(size, rad)
        self.cdg.add(node1)
        self.cdg.add(node2)
        self.node_set = [ node1, node2 ]
        self.edge_set = [(node1, node2), (node2, node1)]
        self.edge_batch = self.edge_set[:]
        self.triangle_set = []
        self.rand_var = rand_var
        self.rand_mean = rand_mean
        self.rad_lower_lim = rad_lower_lim
        self.boundary_rad = boundary_rad

    def build_node(self, node1, node2):
        rand_rat = self.rand_var * (random.random() - 0.5) + self.rand_mean
        node3_rad = ((node1.rad + node2.rad) / 2.) * rand_rat
        A = node1.rad + node3_rad
        B = node1.rad + node2.rad
        C = node2.rad + node3_rad
        theta = (math.acos((A*A + B*B - C*C) / float(A*B + A*B)) +
                 math.atan2(node2.y - node1.y, node2.x - node1.x))
        node3 = Node((A * math.cos(theta) + node1.x,
                      A * math.sin(theta) + node1.y),
                     node3_rad)
        return node3

    def check_node(self, node):
        if node.rad < self.rad_lower_lim:
            return False

        if node.x < -self.size / 2 or node.x > self.size / 2:
            return False

        if node.y < -self.size / 2 or node.y > self.size / 2:
            return False

        if self.boundary_rad:
            dist = math.sqrt(node.x * node.x + node.y * node.y)
            if self.boundary_rad < dist + node.rad:
                return False

        addresses = self.cdg.address_node(node)
        for neighbor in self.cdg.get_neighbors(addresses):
            if Node.intersect(node, neighbor):
                return False

        return True

    def build_FIFO(self):
        while self.edge_batch:
            temp_edge_batch = []
            for node1, node2 in self.edge_batch:
                node3 = self.build_node(node1, node2)
                if self.check_node(node3):
                    self.cdg.add(node3)
                    self.node_set.append(node3)
                    self.triangle_set.append((node1, node2, node3))
                    temp_edge_batch.extend([(node1, node3), (node3, node2)])
            self.edge_batch = temp_edge_batch[:]
            self.edge_set.extend(temp_edge_batch)

    def build_LIFO(self):
        while self.edge_batch:
            node1, node2 = self.edge_batch.pop()
            node3 = self.build_node(node1, node2)
            if self.check_node(node3):
                self.cdg.add(node3)
                self.node_set.append(node3)
                self.triangle_set.append((node1, node2, node3))
                self.edge_batch.extend([(node1, node3), (node3, node2)])
                self.edge_set.extend([(node1, node3), (node3, node2)])

    """
    def build_FIFO_draw(self, screen, color, filled, aalias):
        import sys
        import pygame
        while self.edge_batch:
            temp_edge_batch = []
            for event in pygame.event.get(pygame.locals.QUIT):
                sys.exit()
            for node1, node2 in self.edge_batch:
                node3 = self.build_node(node1, node2)
                if self.check_node(node3):
                    self.cdg.add(node3)
                    temp_edge_batch.extend([(node1, node3), (node3, node2)])
                    #self.draw_node(screen, color, node3, False, aalias)
                    self.draw_triangle(screen, color, node1, node2, node3, filled, aalias)
                    pygame.display.update()
            self.edge_batch = temp_edge_batch[:]

    def build_LIFO_draw(self, screen, color, filled, aalias):
        import sys
        import pygame
        while self.edge_batch:
            for event in pygame.event.get(pygame.locals.QUIT):
                sys.exit()
            node1, node2 = self.edge_batch.pop()
            node3 = self.build_node(node1, node2)
            if self.check_node(node3):
                self.cdg.add(node3)
                self.edge_batch.extend([(node1, node3), (node3, node2)])
                #self.draw_node(screen, color, node3, False, aalias)
                self.draw_triangle(screen, color, node1, node2, node3, filled, aalias)
                pygame.display.update()
    """

    def draw_node(self, surf, color, node, filled, aalias):
        x, y = Node.center_wrt_surf(node.pos, surf)
        if aalias:
            pygame.gfxdraw.aacircle(surf, x, y, int(node.rad), color)
        if filled:
            pygame.gfxdraw.filled_circle(surf, x, y, int(node.rad), color)
        elif not aalias:
            pygame.draw.circle(surf, color, (x, y), int(node.rad), 1)

    def draw_edge(self, surf, color, node1, node2, aalias):
        pos1 = Node.center_wrt_surf(node1.pos, surf)
        pos2 = Node.center_wrt_surf(node2.pos, surf)
        if aalias:
            pygame.draw.aaline(surf, color, pos1, pos2)
        else:
            pygame.draw.line(surf, color, pos1, pos2)

    def draw_triangle(self, surf, color, node1, node2, node3, filled, aalias):
        pos1 = Node.center_wrt_surf(node1.pos, surf)
        pos2 = Node.center_wrt_surf(node2.pos, surf)
        pos3 = Node.center_wrt_surf(node3.pos, surf)
        if aalias:
            pygame.gfxdraw.aapolygon(surf, (pos1, pos2, pos3), color)
        if filled:
            pygame.gfxdraw.filled_polygon(surf, (pos1, pos2, pos3), color)
        elif not aalias:
            pygame.gfxdraw.polygon(surf, (pos1, pos2, pos3), color)

    def draw_nodes(self, surf, color, filled, aalias):
        for node in self.node_set:
            self.draw_node(surf, color, node, filled, aalias)

    def draw_edges(self, surf, color, aalias):
        for (node1, node2) in self.edge_set:
            self.draw_edge(surf, color, node1, node2, aalias)

    def draw_triangles(self, surf, color, filled, aalias):
        for (node1, node2, node3) in self.triangle_set:
            self.draw_triangle(surf, color, node1, node2, node3, filled, aalias)
