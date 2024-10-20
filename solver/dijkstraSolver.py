# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Dijkstra's maze solver.
#
# __author__ =  <Anh Minh Bui>
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

    class ComparableCoordinates:
        #wrapper class for Coordinates to compare distance, since Coordinates cannot be compare in heapq
        def __init__(self, distance, coordinates):
            self.distance = distance
            self.coordinates = coordinates

        def __lt__(self, other):
            #compare based on distance
            return self.distance < other.distance

    def solveMaze(self, maze: Maze, entrance: Coordinates):
        # init a priority queue
        pq = []
        # push the entrance with index 0
        heapq.heappush(pq, DijkstraSolver.ComparableCoordinates(0, entrance))

        #store the used entrace
        self.m_entranceUsed = entrance

        # distance map: store the minimum distance from the entrance to each cell
        dist = {entrance: 0}

        # predecessor map: to reconstruct the path
        predecessors = {}

        # visited set to track cells that have been fully processed
        visited = set()

        # exploring
        while pq:
            # remove cell with the smallest distance
            current = heapq.heappop(pq)
            current_dist = current.distance
            curr_cell = current.coordinates

            # mark cell as visited
            visited.add(curr_cell)

            # current cell = exit, done 
            if curr_cell in maze.getExits():
                self.m_exitUsed = curr_cell
                break

            # get neighbor of current cell
            for neighbor in maze.neighbours(curr_cell):
                if neighbor in visited or maze.hasWall(curr_cell, neighbor):
                    continue

                #calculate tentative distance
                new_dist = current_dist + maze.edgeWeight(curr_cell, neighbor)

                # new_dist < current_dist, update the distance and predecessor maps
                if neighbor not in dist or new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    predecessors[neighbor] = curr_cell
                    heapq.heappush(pq, DijkstraSolver.ComparableCoordinates(new_dist, neighbor))

            # count explored cells
            self.m_cellsExplored += 1

        # reconstruct path
        if self.m_exitUsed:
            path = []
            curr = self.m_exitUsed
            while curr is not None:
                path.append(curr)
                curr = predecessors.get(curr, None)
            # reverse path
            self.m_solverPath = path[::-1]
            
    def compare_coordinates(self, coord1, coord2):
        if coord1.x < coord2.x:
            return -1
        elif coord1.x > coord2.x:
            return 1
        else:  # x values are equal, compare y values
            if coord1.y < coord2.y:
                return -1
            elif coord1.y > coord2.y:
                return 1
            else:
                return 0  #x == y
