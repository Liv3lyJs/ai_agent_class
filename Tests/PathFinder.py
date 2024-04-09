from queue import PriorityQueue
import csv
import time


#mazefile = 'assets/Mazes/mazeMedium_0'
class PathFinder:

    maze = []
    
    
    def __init__(self, mazefile,currentrow, currentcol, endrow, endcol):
        self.currentrow = currentrow
        self.currentcol = currentcol
        self.mazefile = mazefile
        self.endrow = endrow
        self.endcol = endcol
        self.path = {}

    def A_Star(self):

        with open(self.mazefile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.maze.append(row)

        start = (self.currentrow,self.currentcol)
        end = (self.endrow,self.endcol)
        cumulCost = {(x, y): float('inf') for x, row in enumerate(self.maze) for y, _ in enumerate(row)}
        totalCost = cumulCost
        cumulCost[start] = 0
        totalCost[start] = self.Manhattan(start,end)

        prioQ = PriorityQueue()
        prioQ.put((totalCost[start], self.Manhattan(start,end), start))
        revPath = {}
        while not prioQ.empty():
            currentCell = prioQ.get()[2]
            if currentCell != end:
                for neighbor in self.CheckPath(currentCell, self.maze):
                    temp_cumul_cost = cumulCost[currentCell] + 1
                    temp_total_cost = temp_cumul_cost + self.Manhattan(neighbor, end)

                    if temp_total_cost < totalCost[neighbor]:
                        cumulCost[neighbor] = temp_cumul_cost
                        totalCost[neighbor] = temp_total_cost
                        prioQ.put((totalCost[neighbor], self.Manhattan(neighbor, end), neighbor))
                        revPath[neighbor] = currentCell
                        
        cell = end
        while cell != start:
            self.path[revPath[cell]] = cell
            cell = revPath[cell]

    def Manhattan(self, case1, case2):
        x1,y1 = case1
        x2,y2 = case2
        return abs(x1-x2)+ abs(y1-y2)

    def CheckPath(self, cell, matrix):
        row,col= cell
        num_rows = len(matrix)
        num_cols = len(matrix[0]) if matrix else 0
        
        # Define possible directions
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Left, Up, Right, Down
        
        neighbors = []
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check if the new coordinates are within the matrix boundaries
            if 0 <= new_row < num_rows and 0 <= new_col < num_cols:
                value = matrix[new_row][new_col]
                
                # Check if the value is not '1'
                if value != '1':
                    neighbors.append((new_row, new_col))
        
        return neighbors
    
    def NextMove(self, currentX, currentY):
        currentCell = (currentX,currentY)
        nextX, nextY = self.path[currentCell]
        if nextX == currentX + 1:
            instruction = 'DOWN'
        elif nextX == currentX - 1:
            instruction = 'UP'
        elif nextY == currentY + 1:
            instruction = 'RIGHT'
        elif nextY == currentY - 1:
            instruction = 'LEFT'

        return nextX, nextY, instruction
        

      

