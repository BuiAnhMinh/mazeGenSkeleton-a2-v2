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
        # Stores paths for each entrance-exit pair
        self.entrance_exit_paths = {}
        # Total number of cells explored
        self.total_explored_cells = 0
        # Flag to check if all paths were solved
        self.all_solved = False
        # Total cost of all paths found
        self.total_cost = 0
    class ComparableCoordinates:
        #wrapper class for Coordinates to compare distance, since Coordinates cannot be compare in heapq
        def __init__(self, distance: int, coordinates: Coordinates):
            self.distance = distance
            self.coordinates = coordinates

        def __lt__(self, other):
            #compare based on distance
            return self.distance < other.distance

        def __eq__(self, other):
            # needed for heapq 
            return self.distance == other.distance and self.coordinates == other.coordinates

        def __hash__(self):
            # ensures the object can be used in sets and dictionaries
            return hash((self.distance, self.coordinates))

        def __repr__(self):
            #debugging
            return f"ComparableCoordinates(distance={self.distance}, coordinates={self.coordinates})"

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]) -> bool:
        # solve maze by finding non-overlapping paths using Dijkstra's algorithm for each entrance-exit pair.
        # clear path, reset state
        self.entrance_exit_paths.clear()
        used_cells = set() #track cells that used by other paths
        total_cost = 0
        all_paths_found = True

        # process each entrance-exit pair
        for i in range(len(entrances)):
            entrance = entrances[i]
            exit = exits[i]
            path, cost = self._dijkstra(maze, entrance, exit, used_cells)
            
            if path:
                # print(f"Path found from {entrance} to {exit}: {path}, Cost: {cost}") 
                self.entrance_exit_paths[(entrance, exit)] = path
                total_cost += cost
                used_cells.update(path)  # Mark these cells as used
            else:
                # print(f"No path found from {entrance} to {exit}")
                all_paths_found = False
                print(f"Can't find path")
                break  # Cant find path,stop

        self.all_solved = all_paths_found
        self.total_cost = total_cost
        print(f"Total path cost: {self.total_cost}")
        return all_paths_found

    def _dijkstra(self, maze: Maze, start: Coordinates, goal: Coordinates, used_cells: set) -> Tuple[List[Coordinates], int]:
    #    Dijkstra's algorithm to find the shortest path between start and goal.
        pq = []  # priority queue
        dist = {start: 0}  # distance to each cell
        predecessors = {}  # to reconstruct the path
        heapq.heappush(pq, self.ComparableCoordinates(0, start))  # push start with dist 0
        
        while pq:
            current = heapq.heappop(pq)
            current_dist = current.distance
            curr_cell = current.coordinates
            # print(f"Exploring {curr_cell} with distance {current_dist}")

            if curr_cell == goal:  # exit found, stop and reconstruct
                return self._reconstruct_path(predecessors, curr_cell), current_dist

            # explore neighbors
            for neighbor in maze.neighbours(curr_cell):
                if neighbor in used_cells or maze.hasWall(curr_cell, neighbor):
                    # print(f"Skipping neighbor {neighbor}: already used or blocked by a wall")
                    continue  # skip if cell used or a wall infront

                new_dist = current_dist + maze.edgeWeight(curr_cell, neighbor)

                # update shortest distance if a better path found
                if neighbor not in dist or new_dist < dist[neighbor]:
                    # print(f"Updating neighbor {neighbor}: new shortest distance {new_dist}")
                    dist[neighbor] = new_dist
                    predecessors[neighbor] = curr_cell
                    heapq.heappush(pq, self.ComparableCoordinates(new_dist, neighbor))
        
        return [], 0  # return empty path and 0 cost if no valid path found

    def _reconstruct_path(self, predecessors: dict, current: Coordinates) -> List[Coordinates]:
        path = []
        while current:
            # print(f"Reconstructing path, adding {current}")
            path.append(current)
            current = predecessors.get(current, None)
        return path[::-1]  # reverse the path 

    def cellsExplored(self) -> int:
        return self.total_explored_cells

    def totalPathCost(self) -> int:
        return self.total_cost
