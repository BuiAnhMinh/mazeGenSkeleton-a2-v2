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
    """
    Represents an edge in the graph, consisting of two vertices and a weight.
    """
    def __init__(self):
        self.edges = []
    
    def addEdge(self, u, v, weight):
        """Add an edge between two vertices with a given weight."""
        self.edges.append((u, v, weight))

class DisjointSet:
    """
    Represents the disjoint-set (union-find) data structure.
    """
    def __init__(self, n):
        # Initialize parent and rank arrays
        self.parent = list(range(n))  # Each vertex is initially its own parent
        self.rank = [0] * n  # Rank is used to keep track of the tree depth
    
    def find(self, u):
        """Find the representative of the set containing u (with path compression)."""
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Path compression
        return self.parent[u]
    
    def union(self, u, v):
        """Union by rank, merges the sets containing u and v."""
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
    """
    Kruskal's algorithm maze generator with weighted edges, excluding outer walls from the edge list.
    """
    
    def generateMaze(self, maze: Maze):
        graph = Edge()  # Graph to store the edges
        cells = maze.getCoords()  # All the cells (vertices) in the maze
        num_cells = len(cells)
        
        # Map cell coordinates to an index for the DisjointSet (since it uses integers)
        cell_index = {cell: idx for idx, cell in enumerate(cells)}
        
        # Add walls (edges) between neighboring cells, but skip outer wall edges
        for cell in cells:
            neighbors = maze.neighbours(cell)
            for neighbor in neighbors:
                if maze.hasEdge(cell, neighbor):  # Ensure an edge exists
                    if not self.isOuterWall(cell, neighbor, maze):  # Skip outer walls
                        weight = maze.edgeWeight(cell, neighbor)  # Get edge weight
                        graph.addEdge(cell, neighbor, weight)

        # Initialize disjoint sets for all cells
        disjoint_set = DisjointSet(num_cells)

        # Sort the edges based on their weights (for the weighted approach)
        graph.edges.sort(key=lambda edge: edge[2])  # Sort by the weight

        # Process each edge in sorted order (Kruskal's algorithm)
        for edge in graph.edges:
            u, v, weight = edge
            u_idx = cell_index[u]
            v_idx = cell_index[v]

            # If u and v are not in the same set, remove the wall between them
            if disjoint_set.find(u_idx) != disjoint_set.find(v_idx):
                maze.removeWall(u, v)  # Remove the wall between u and v
                disjoint_set.union(u_idx, v_idx)  # Merge the sets

        return maze
    
    def isOuterWall(self, u: Coordinates, v: Coordinates, maze: Maze) -> bool:
        """
        Checks if the edge between two cells u and v is part of the outer wall.
        The outer walls are those that are on the boundaries of the maze.
        """
        width = maze.colNum()  # Number of columns in the maze
        height = maze.rowNum()  # Number of rows in the maze

        # u or v should only be considered on the outer wall if it is not connected to a valid cell inside the maze
        if (u.getRow() == -1 or u.getRow() == height or v.getRow() == -1 or v.getRow() == height) or \
        (u.getCol() == -1 or u.getCol() == width or v.getCol() == -1 or v.getCol() == width):
            return True  # This means it's on the outermost boundary (invalid)
        
        return False  # Otherwise, it is an inner wall that should be considered for removal