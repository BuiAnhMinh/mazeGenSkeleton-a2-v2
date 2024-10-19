# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Kruskal's maze generator.
#
# __author__ = Anh Minh Bui
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze import Maze
from maze.util import Coordinates
import random

# reference : https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
class Edge:
    #edge in maze
    def __init__(self):
        self.edges = []
    
    def addEdge(self, u, v, weight):
        #add edge of 2 vertices with weight
        self.edges.append((u, v, weight))

class DisjointSet:
    #disjoint set DS
    def __init__(self, n):
        # initialize parent
        self.parent = list(range(n))  # each vertex is each own parent
        self.rank = [0] * n  #rank to keep track of tree depth
    
    def find(self, u):
        #find representative of set with path compression
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # path compression
        return self.parent[u]
    
    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

class KruskalMazeGenerator:
    #kruskal with weighted graph
    def generateMaze(self, maze: Maze):
        graph = Edge()  # store the edge
        cells = maze.getCoords()  #get the coord of all the vertices
        num_cells = len(cells)
        
        #map cell coordinates to disjoinset
        cell_index = {cell: idx for idx, cell in enumerate(cells)}
        
        # add wall between neighors (exclude outer wall)
        for cell in cells:
            neighbors = maze.neighbours(cell)
            for neighbor in neighbors:
                if maze.hasEdge(cell, neighbor):  # ensure edge exists
                    if not self.isOuterWall(cell, neighbor, maze):  # skip outer wall
                        weight = maze.edgeWeight(cell, neighbor)  # get edge weight
                        graph.addEdge(cell, neighbor, weight)

        # initialize disjoinset
        disjoint_set = DisjointSet(num_cells)

        # sort the edge based on weight
        graph.edges.sort(key=lambda edge: edge[2]) 

        # process in sorted order
        for edge in graph.edges:
            u, v, weight = edge
            u_idx = cell_index[u]
            v_idx = cell_index[v]

            #if u and v not in the same set, remove wall
            if disjoint_set.find(u_idx) != disjoint_set.find(v_idx):
                maze.removeWall(u, v)  # remove the wall between u and v
                disjoint_set.union(u_idx, v_idx)  # merge the sets

        return maze
    
    def isOuterWall(self, u: Coordinates, v: Coordinates, maze: Maze) -> bool:
        #check if edge is outer wall
        width = maze.colNum()  
        height = maze.rowNum()  

        if (u.getRow() == -1 or u.getRow() == height or v.getRow() == -1 or v.getRow() == height) or \
        (u.getCol() == -1 or u.getCol() == width or v.getCol() == -1 or v.getCol() == width):
            return True  # on the outer boundary (invalid)
        
        return False  # on inner wall that should be considered for removal