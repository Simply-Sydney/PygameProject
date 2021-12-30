class Node():
    '''Node class to use with A* pathfinding'''
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Pathing:
    def __init__(self, maze):
        self.maze = maze

    def astar(self, cost, start, end):
        #Create start and end nodes with initialized vals for g, h, and f
        start_node = Node(None, tuple(start))
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, tuple(end))
        end_node.g = end_node.h = end_node.f = 0

        #Initialize yet_to_visit and visited lists
        #In this list will be all nodes that are yet to be visited for exploration
        #From here will find the lowest cost node to expand next
        yetToVisitList = []
        #In this list will be all nodes that have already been explored
        visitedList = []
        #Add start node
        yetToVisitList.append(start_node)

        #Add a stopping condition to avoid infinite loops and stop after reasonable number of steps
        outer_iterations = 0
        max_iterations = (len(self.maze) // 2) ** 10

        #Define what squares to be searched
        move = [[-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, 1], [-1, 1], [1, -1]]

        #Define length of rows and columns
        num_rows = len(self.maze)
        num_cols = len(self.maze[0])

        #Loop until end is found
        while len(yetToVisitList) > 0:
            #Increment limit counter
            outer_iterations += 1

            #Get current node
            current_node = yetToVisitList[0]
            current_index = 0
            for index, item in enumerate(yetToVisitList):
		    	#If current item cost less than current node, assign item to current_node
                if(item.f < current_node.f):
                        current_node = item
                        current_index = index

            #Return incomplete path if max limit reached
            if (outer_iterations > max_iterations):
                if(DEBUG):
                    print("Giving up pathfinding, too many iterations")
                return self.returnPath(current_node)

            #Pop current node out of yetToVisitList, add to visitedList
            yetToVisitList.pop(current_index)
            visitedList.append(current_node)

            #Test if goal was reached, if yes then return path
            if(current_node == end_node):
                return self.returnPath(current_node)

            #Generate children from all adjacent squares
            children = []

            for new_position in move:
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                #Make sure position is within range
                if (node_position[0] > (num_rows - 1) or
                    node_position[0] < 0 or 
                    node_position[1] > (num_cols - 1) or
                    node_position[1] < 0):
                    continue

                #Check that terrain is walkable
                if (self.maze[node_position[0]][node_position[1]] == 1) or (self.maze[node_position[0]][node_position[1]] == 0):
                    continue

                #Create new node
                new_node = Node(current_node, node_position)

                #Append new node
                children.append(new_node)

                #Loop through children
            for child in children:
                #Child is already on the visitedList
                if (len([visited_child for visited_child in visitedList if visited_child == child]) > 0):
                    continue

                #Create f, g, and h values
                child.g = current_node.g + cost
                #Heuristic costs calc here, using eucledian distance
                child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))

                child.f = child.g + child.h

                #Child is already in the yetToVisitList and g cost is already lower
                if (len([i for i in yetToVisitList if child == i and child.g > i.g]) > 0):
                    continue

                #Add child to the yetToVisitList
                yetToVisitList.append(child)
				

    def returnPath(self, current_node):
        #initialize empty path
        path = []
        #Number of rows and columns
        num_rows = len(self.maze)
        num_cols = len(self.maze[0])
        #Here we create the initialized result maze with -1 in every pos
        result = [[-1 for i in range(num_cols)]for j in range(num_rows)]
        current = current_node
        while(current is not None):
            path.append(current.position)
            current = current.parent
        #Return reversed path
        path = path[::-1]
        start_value = 0
        #Update the path of start to end found by A-star search with every step incremented by 1
        for i in range(len(path)):
            result[path[i][0]][path[i][1]] = start_value
            start_value += 1
        return path
