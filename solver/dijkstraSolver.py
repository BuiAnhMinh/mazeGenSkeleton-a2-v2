# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Dijkstra's maze solver.
#
# __author__ =  <Your Name>
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

import heapq
from typing import List
from maze.util import Coordinates
from maze.maze import Maze

# reference : https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/

class DijkstraSolver:

    def __init__(self):
        # Path taken by the solver
        self.m_solverPath: List[Coordinates] = list()
        # Number of cells explored
        self.m_cellsExplored = 0
        # Entrance used to enter the maze
        self.m_entranceUsed = None
        # Exit found and used by the solver
        self.m_exitUsed = None

    def solveMaze(self, maze: Maze, entrance: Coordinates):
        # Initialize the priority queue (min-heap)
        pq = []
        # Push the entrance to the priority queue with distance 0
        heapq.heappush(pq, (0, entrance))

        # Store the entrance used
        self.m_entranceUsed = entrance

        # Distance map: store the minimum distance from the entrance to each cell
        dist = {entrance: 0}

        # Predecessor map: to reconstruct the path
        predecessors = {}

        # Visited set to track cells that have been fully processed
        visited = set()

        # Start exploring from the entrance
        while pq:
            # Pop the cell with the smallest distance
            current_dist, curr_cell = heapq.heappop(pq)

            # Mark the cell as visited
            visited.add(curr_cell)

            # If the current cell is an exit, we are done
            if curr_cell in maze.getExits():
                self.m_exitUsed = curr_cell
                break

            # Get neighbors of the current cell
            for neighbor in maze.neighbours(curr_cell):
                if neighbor in visited or maze.hasWall(curr_cell, neighbor):
                    continue

                # Calculate the tentative distance
                new_dist = current_dist + maze.edgeWeight(curr_cell, neighbor)

                # If the new distance is shorter, update the distance and predecessor maps
                if neighbor not in dist or new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    predecessors[neighbor] = curr_cell
                    heapq.heappush(pq, (new_dist, neighbor))

            # Count cells explored
            self.m_cellsExplored += 1

        # Reconstruct the path from the exit to the entrance
        if self.m_exitUsed:
            path = []
            curr = self.m_exitUsed
            while curr is not None:
                path.append(curr)
                curr = predecessors.get(curr, None)
            # Reverse the path to get it from entrance to exit
            self.m_solverPath = path[::-1]


	