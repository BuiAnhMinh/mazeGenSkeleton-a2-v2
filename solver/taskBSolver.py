# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Brute force maze solver for all entrance, exit pairs
#
# __author__ = '<Anh Minh Bui>
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


import heapq
from typing import List, Tuple
from maze.util import Coordinates
from maze.maze import Maze

class bruteForceSolver:
    def __init__(self):
        self.entrance_exit_paths = {}
        self.total_explored_cells = 0
        self.all_solved = False
        self.total_cost = 0

    class ComparableCoordinates:
        """
        A wrapper class for Coordinates that compares based on distance.
        This is needed because Coordinates cannot be directly compared in a heapq.
        """
        def __init__(self, distance: int, coordinates: Coordinates):
            self.distance = distance
            self.coordinates = coordinates

        def __lt__(self, other):
            # Compare based on distance only, as required for the priority queue
            return self.distance < other.distance

        def __eq__(self, other):
            # Needed for heapq operations
            return self.distance == other.distance and self.coordinates == other.coordinates

        def __hash__(self):
            # Ensures the object can be used in sets and dictionaries
            return hash((self.distance, self.coordinates))

        def __repr__(self):
            # String representation for debugging purposes
            return f"ComparableCoordinates(distance={self.distance}, coordinates={self.coordinates})"

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]) -> bool:
        """
        Solves the maze by finding non-overlapping paths using Dijkstra's algorithm for each entrance-exit pair.
        Ensures that no cell is reused across different paths, and the total cost of all paths is minimized.
        """
        # Clear any previous paths and reset state
        self.entrance_exit_paths.clear()
        used_cells = set()  # To track cells used by any path
        total_cost = 0
        all_paths_found = True

        # Process each entrance-exit pair
        for i in range(len(entrances)):
            entrance = entrances[i]
            exit = exits[i]
            path, cost = self._dijkstra(maze, entrance, exit, used_cells)
            
            if path:
                self.entrance_exit_paths[(entrance, exit)] = path
                total_cost += cost
                used_cells.update(path)  # Mark these cells as used
            else:
                all_paths_found = False
                break  # If any path can't be found, stop the process

        self.all_solved = all_paths_found
        self.total_cost = total_cost
        print(f"Total path cost: {self.total_cost}")
        return all_paths_found

    def _dijkstra(self, maze: Maze, start: Coordinates, goal: Coordinates, used_cells: set) -> Tuple[List[Coordinates], int]:
        """
        Implements Dijkstra's algorithm to find the shortest path between start and goal.
        Takes into account cells already used in previous paths.
        Returns the path and its cost.
        """
        pq = []  # Priority queue for the open list
        dist = {start: 0}  # Distance to each cell
        predecessors = {}  # To reconstruct the path
        heapq.heappush(pq, self.ComparableCoordinates(0, start))  # Push start with distance 0
        
        while pq:
            current = heapq.heappop(pq)
            current_dist = current.distance
            curr_cell = current.coordinates

            if curr_cell == goal:  # Exit found, stop and construct path
                return self._reconstruct_path(predecessors, curr_cell), current_dist

            # Explore neighbors
            for neighbor in maze.neighbours(curr_cell):
                if neighbor in used_cells or maze.hasWall(curr_cell, neighbor):
                    continue  # Skip if cell is already used or there is a wall

                new_dist = current_dist + maze.edgeWeight(curr_cell, neighbor)

                # Update shortest distance if a better path is found
                if neighbor not in dist or new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    predecessors[neighbor] = curr_cell
                    heapq.heappush(pq, self.ComparableCoordinates(new_dist, neighbor))
        
        return [], 0  # Return empty path and 0 cost if no valid path was found

    def _reconstruct_path(self, predecessors: dict, current: Coordinates) -> List[Coordinates]:
        """
        Reconstructs the path from the goal back to the start using the predecessors map.
        """
        path = []
        while current:
            path.append(current)
            current = predecessors.get(current, None)
        return path[::-1]  # Reverse the path to go from start to goal

    def cellsExplored(self) -> int:
        """
        Returns the number of cells explored during the search.
        """
        return self.total_explored_cells

    def totalPathCost(self) -> int:
        """
        Returns the total cost of all paths found.
        """
        return self.total_cost
