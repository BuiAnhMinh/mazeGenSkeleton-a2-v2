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
    """
    Solver class implementing a greedy approach to find non-overlapping paths between
    entrance-exit pairs in a maze.
    """
    def __init__(self):
        # dictionary to store paths for each entrance-exit pair
        self.entrance_exit_paths = {}
        # number of cells explored during the search
        self.total_explored_cells = 0
        # flag to indicate if all paths were found
        self.all_solved = False
        #total cost of all the paths found
        self.total_cost = 0

    class ComparableCoordinates:
       #wrapper class for Coordinates to compare distance, since Coordinates cannot be compare in heapq
        def __init__(self, total_cost: int, coordinates: Coordinates):
            self.total_cost = total_cost
            self.coordinates = coordinates

        def __lt__(self, other):
            # compare based on total cost (distance + heuristic)
            return self.total_cost < other.total_cost

        def __repr__(self):
            # string representation for debugging purposes
            return f"ComparableCoordinates(total_cost={self.total_cost}, coordinates={self.coordinates})"

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]) -> bool:
        # solve maze by finding non-overlapping paths for each entrance-exit pair using a greedy approach.
        # clear paths and reset state
        self.entrance_exit_paths.clear()
        used_cells = set()  # track cells used by any path
        total_cost = 0
        all_paths_found = True

        # process each entrance-exit pair
        for i in range(len(entrances)):
            entrance = entrances[i]
            exit = exits[i]
            path, cost = self._greedy_search(maze, entrance, exit, used_cells)

            if path:
                # store the path and its cost
                self.entrance_exit_paths[(entrance, exit)] = path
                total_cost += cost
                used_cells.update(path)  # mark cells as used
            else:
                # path can't find path, stop the process
                all_paths_found = False
                print(f"Can't find path")
                break

        self.all_solved = all_paths_found
        self.total_cost = total_cost
        print(f"Total path cost: {self.total_cost}")
        return all_paths_found

    def _greedy_search(self, maze: Maze, start: Coordinates, goal: Coordinates, used_cells: set) -> Tuple[List[Coordinates], int]:
        # greedy search algorithm to find the shortest path between start and goal using Manhattan distance as the heuristic.
        
        # priority queue for the open list
        pq = []
        # distance to each cell
        dist = {start: 0}
        # to reconstruct the path
        predecessors = {}
        # push start with its Manhattan distance to the goal
        heapq.heappush(pq, self.ComparableCoordinates(0 + self._manhattan_distance(start, goal), start))

        while pq:
            # get the cell with the lowest total cost
            current = heapq.heappop(pq)
            current_cost = dist[current.coordinates]
            curr_cell = current.coordinates

            # goal is reached, reconstruct the path
            if curr_cell == goal:
                return self._reconstruct_path(predecessors, curr_cell), current_cost

            # explore neighbors 
            for neighbor in maze.neighbours(curr_cell):
                # skip cell
                if neighbor in used_cells or maze.hasWall(curr_cell, neighbor):
                    continue

                # calculate the cost to reach neighbor
                new_cost = current_cost + maze.edgeWeight(curr_cell, neighbor)

                # update the distance and predecessor maps if a shorter path is found
                if neighbor not in dist or new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    predecessors[neighbor] = curr_cell
                    # push the neighbor with its total cost (new cost + heuristic)
                    heapq.heappush(pq, self.ComparableCoordinates(new_cost + self._manhattan_distance(neighbor, goal), neighbor))

        # return empty path and 0 cost if no valid path was found
        return [], 0

    def _manhattan_distance(self, start: Coordinates, goal: Coordinates) -> int:
        #manhattan distance(refer to source)
        return abs(start.getRow() - goal.getRow()) + abs(start.getCol() - goal.getCol())

    def _reconstruct_path(self, predecessors: dict, current: Coordinates) -> List[Coordinates]:
        #recontstruct path
        path = []
        while current:
            # add the current cell to the path
            path.append(current)
            current = predecessors.get(current, None)
        # reverse the path 
        return path[::-1]

    def cellsExplored(self) -> int:
        return self.total_explored_cells

    def totalPathCost(self) -> int:
        return self.total_cost
