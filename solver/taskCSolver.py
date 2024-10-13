# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Greedy maze solver for all entrance, exit pairs
#
# __author__ = '<Anh Minh Bui>'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze
from typing import List
import heapq

class ComparableCoordinates:
    """
    A wrapper class for Coordinates that allows comparison based on distance.
    This is necessary because Coordinates cannot be directly compared in a heapq.
    """
    def __init__(self, distance: int, coordinates: Coordinates):
        self.distance = distance
        self.coordinates = coordinates

    def __lt__(self, other):
        # Compare based on distance for the priority queue
        return self.distance < other.distance

    def __eq__(self, other):
        # Equality check based on distance and coordinates
        return self.distance == other.distance and self.coordinates == other.coordinates

    def __hash__(self):
        # Allows the object to be used in sets and dictionaries
        return hash((self.distance, self.coordinates))

    def __repr__(self):
        # String representation for debugging
        return f"ComparableCoordinates(distance={self.distance}, coordinates={self.coordinates})"

class greedySolver:
    def __init__(self):
        self.paths = []  # To store the paths from entrances to exits
        self.used_cells = set()  # Track the cells that have been used in paths
        self.total_cost = 0  # Total cost of paths found
        self.all_solved = False  # Initialize the all_solved flag

    def heuristic(self, current: Coordinates, goal: Coordinates) -> int:
        # Use Manhattan distance as a heuristic
        return abs(current.getRow() - goal.getRow()) + abs(current.getCol() - goal.getCol())

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]) -> bool:
        all_paths_found = True  # Flag to check if all paths are found

        for entrance, exit in zip(entrances, exits):
            path = self.find_path(maze, entrance, exit)
            if path:
                self.paths.append(path)
                self.total_cost += self.calculate_path_cost(maze, path)
                # Mark cells in this path as used
                for cell in path:
                    self.used_cells.add(cell)
            else:
                all_paths_found = False  # If any path can't be found, mark it as false
                break  # Stop processing if any path is not found

        # Set the all_solved flag based on whether all paths were found
        self.all_solved = all_paths_found
        return all_paths_found

    def find_path(self, maze: Maze, start: Coordinates, goal: Coordinates) -> List[Coordinates]:
        # Priority queue for the greedy search
        queue = []
        heapq.heappush(queue, ComparableCoordinates(0, start))  # Use the wrapper class
        came_from = {start: None}
        cost_so_far = {start: 0}

        while queue:
            current = heapq.heappop(queue)  # Get the ComparableCoordinates object
            curr_coordinates = current.coordinates

            if curr_coordinates == goal:
                return self.reconstruct_path(came_from, start, goal)

            for neighbor in maze.neighbours(curr_coordinates):
                if neighbor in self.used_cells or maze.hasWall(curr_coordinates, neighbor):
                    continue  # Skip cells that are already used or have walls

                new_cost = cost_so_far[curr_coordinates] + maze.edgeWeight(curr_coordinates, neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(queue, ComparableCoordinates(priority, neighbor))  # Use the wrapper class
                    came_from[neighbor] = curr_coordinates

        return None  # No valid path was found

    def reconstruct_path(self, came_from, start, goal) -> List[Coordinates]:
        # Reconstruct the path from start to goal
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()  # Reverse the path to go from start to goal
        return path

    def calculate_path_cost(self, maze: Maze, path: List[Coordinates]) -> int:
        """
        Calculate the total cost of the path using the edge weights in the maze.
        """
        cost = 0
        for i in range(len(path) - 1):
            cost += maze.edgeWeight(path[i], path[i + 1])
        return cost

    def cellsExplored(self) -> int:
        """
        Returns the number of unique cells explored during the search.
        """
        return len(self.used_cells)

    def totalPathCost(self) -> int:
        """
        Returns the total cost of all paths found.
        """
        return self.total_cost
