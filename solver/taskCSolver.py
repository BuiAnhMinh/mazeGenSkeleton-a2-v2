# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Greedy maze solver for all entrance, exit pairs
#
# __author__ = '<Anh Minh Bui>'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


import heapq
from typing import List, Tuple
from maze.util import Coordinates
from maze.maze import Maze

class greedySolver:
    def __init__(self):
        self.entrance_exit_paths = {}
        self.total_explored_cells = 0
        self.all_solved = False
        self.total_cost = 0

    class ComparableCoordinates:
        """
        A wrapper class for Coordinates that compares based on total cost (distance + heuristic).
        """
        def __init__(self, total_cost: int, coordinates: Coordinates):
            self.total_cost = total_cost
            self.coordinates = coordinates

        def __lt__(self, other):
            return self.total_cost < other.total_cost

        def __repr__(self):
            return f"ComparableCoordinates(total_cost={self.total_cost}, coordinates={self.coordinates})"

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]) -> bool:
        self.entrance_exit_paths.clear()
        used_cells = set()
        total_cost = 0
        all_paths_found = True

        for i in range(len(entrances)):
            entrance = entrances[i]
            exit = exits[i]
            path, cost = self._greedy_search(maze, entrance, exit, used_cells)

            if path:
                self.entrance_exit_paths[(entrance, exit)] = path
                total_cost += cost
                used_cells.update(path)
            else:
                all_paths_found = False
                print(f"Can't find path")
                break

        self.all_solved = all_paths_found
        self.total_cost = total_cost
        print(f"Total path cost: {self.total_cost}")
        return all_paths_found

    def _greedy_search(self, maze: Maze, start: Coordinates, goal: Coordinates, used_cells: set) -> Tuple[List[Coordinates], int]:
        pq = []
        dist = {start: 0}
        predecessors = {}
        heapq.heappush(pq, self.ComparableCoordinates(0 + self._manhattan_distance(start, goal), start))

        while pq:
            current = heapq.heappop(pq)
            current_cost = dist[current.coordinates]
            curr_cell = current.coordinates

            if curr_cell == goal:
                return self._reconstruct_path(predecessors, curr_cell), current_cost

            for neighbor in maze.neighbours(curr_cell):
                if neighbor in used_cells or maze.hasWall(curr_cell, neighbor):
                    continue

                new_cost = current_cost + maze.edgeWeight(curr_cell, neighbor)

                if neighbor not in dist or new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    predecessors[neighbor] = curr_cell
                    heapq.heappush(pq, self.ComparableCoordinates(new_cost + self._manhattan_distance(neighbor, goal), neighbor))

        return [], 0

    def _manhattan_distance(self, start, goal):
        return abs(start.getRow() - goal.getRow()) + abs(start.getCol() - goal.getCol())

    def _reconstruct_path(self, predecessors: dict, current: Coordinates) -> List[Coordinates]:
        path = []
        while current:
            path.append(current)
            current = predecessors.get(current, None)
        return path[::-1]

    def cellsExplored(self) -> int:
        return self.total_explored_cells

    def totalPathCost(self) -> int:
        return self.total_cost