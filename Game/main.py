import pygame
from pygame.locals import *
import person
import random

pygame.init()

white = (255,255,255)
blue = (100,100,255)
grey = (128,128,128)
black = (0,0,0)
cell_colors = (255,255,255), (0,0,0)

screen = pygame.display.set_mode((320, 320))

playervel = 16
cell_margin = 1
mapOffsetRow = 0
mapOffsetColumn = 0
movement = False

pygame.display.flip()
pygame.display.set_caption('Tiles')
font = pygame.font.SysFont("timesnewroman", 16)
pygame.display.flip()

clock = pygame.time.Clock()

class Node():
    """Node class in use with A* pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def returnPath(current_node, maze):
    #initialize empty path
    path = []
    #Number of rows and columns
    num_rows = len(maze)
    num_cols = len(maze[0])
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

def astar(maze, cost, start, end):
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
    max_iterations = (len(maze) // 2) ** 10

    #Define what squares to be searched
    move = [[-1, 0], [0, -1], [1, 0], [0, 1]]

    #Define length of rows and columns
    num_rows = len(maze)		#Should be -1?
    num_cols = len(maze[0])		#Should be -1?

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
            print("Giving up pathfinding, too many iterations")
            return returnPath(current_node, maze)

        #Pop current node out of yetToVisitList, add to visitedList
        yetToVisitList.pop(current_index)
        visitedList.append(current_node)

        #Test if goal was reached, if yes then return path
        if(current_node == end_node):
			return returnPath(current_node, maze)

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
            if maze[node_position[0]][node_position[1]] != 0:
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






def drawMap(screen):
    for rowTemp in range(len(mapList)):
        for columnTemp in range(len(mapList[0])):
            if((mapList[rowTemp][columnTemp]) == 1):
                screen.fill(white,getCellRect(rowTemp, columnTemp, screen))

def getCellRect(coordRow, coordCol, screen):
    row = coordRow
    column = coordCol
    cell_width = 16
    adjusted_width = cell_width - cell_margin
    return pygame.Rect((column * cell_width + cell_margin)+(mapOffsetColumn*cell_width), (row * cell_width + cell_margin)+(mapOffsetRow*cell_width), adjusted_width, adjusted_width)

def executeAction(character):
    if(character.behaviour == 1):
    #Randomly wander action
        #Character is not done waiting
        if(character.getWaitQ() != 0):
            print("Waiting tick for " + character.name)
            character.waitQTick()
            return

        #Character is done moving and needs to wait
        if((character.getPos('row'),character.getPos('col')) == (character.dest)):
            chooseDestination(character)
            character.setWaitQ(10)
            return

        #Do one move
        print("Moving character " + character.name)
        print("Next Pos: ")
        print (character.path[0])
        character.updatePos(character.path[0])
        character.path.pop(0)
        
        
def chooseDestination(character):
    newPathRow = random.randint(0,19)
    newPathCol = random.randint(0,19)
    while(mapList[newPathRow][newPathCol] == 1):
        newPathRow = random.randint(0,19)
        newPathCol = random.randint(0,19)
        print("Choosing new destination")
    character.setDest((newPathRow,newPathCol))
    print("Finding path for " + character.name + ", currentPos: ")
    print(character.pos)
    print(" newPos: ")
    print(character.dest)
    path = astar(mapList, 1, character.pos, character.dest)
    character.path = (path)
    print("New path for " + character.name + ": ")
    print(character.path)

#
#PERSON CLASS ABSTRACTED
#



mapList = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
           [1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
           [1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1],
           [1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
           [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
           [1,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
           [1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,1],
           [1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1],
           [1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1],
           [1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1],
           [1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
           [1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

officer1 = person.AI(1, "Maggie", "human_unmod", (6,6))
officer1.setColor(blue)
officer1.text = font.render('@', True, officer1.getColor(), black)

player = person.Person("Sydney", "human_unmod", (6,10))
player.setColor(white)
player.text = font.render('@', True, player.getColor(), black)

characters = {officer1}

exitKey = False
#Game Loop
while not exitKey:
    #Execution code
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitKey = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and (mapList[player.getPos('row')][player.getPos('col')-1] != 1):
        """print("Moving player to pos: ")
        print(player.getPos('row'))
        print(player.getPos('col')-1)
        print(player.pos)
        print("New col offset:")
        print(mapOffsetColumn+1)"""
        movement = True
        mapOffsetColumn += 1
        player.updatePos((player.getPos('row'),(player.getPos('col')-1)))
        print("LEFT")
    if keys[pygame.K_RIGHT] and (mapList[player.getPos('row')][player.getPos('col')+1] != 1):
        movement = True
        mapOffsetColumn -= 1
        player.updatePos(((player.getPos('row')),(player.getPos('col')+1)))
        print("RIGHT")
    if keys[pygame.K_UP] and (mapList[player.getPos('row')-1][player.getPos('col')] != 1):
        movement = True
        mapOffsetRow += 1
        player.updatePos(((player.getPos('row')-1),(player.getPos('col'))))
        print("UP")
    if keys[pygame.K_DOWN] and (mapList[player.getPos('row')+1][player.getPos('col')] != 1):
        movement = True
        mapOffsetRow -= 1
        player.updatePos(((player.getPos('row')+1),(player.getPos('col'))))
        print("DOWN")

    screen.fill(black)

    for character in characters:
        #Update officer1 action and pos
        executeAction(character)
        if(character.pos == player.startingPos):
            print("Collision detected!")
        if(movement): #and (character.pos != player.startingPos):
            character.updatePos((character.getStartPos('row')+mapOffsetRow,character.getStartPos('col')+mapOffsetColumn))
        screen.blit(character.text, (character.getPos('col')*16,character.getPos('row')*16))
    
    screen.blit(player.text, (player.getStartPos('col')*16,player.getStartPos('row')*16))

    movement = False

    #tilePosXCounter = 0
    #tilePosYCounter = 0
    #for tiles in mapList:
        #Update map tiles based on char movement
    #    if(tiles == 1):
    #        screen.blit(font.render('#', True, white, black), ((tilePosXCounter*16)+(mapOffsetX*16),(tilePosYCounter*16)+(mapOffsetY*16)))
    #    tilePosXCounter+=1
    #    if(tilePosXCounter == 8):
    #        tilePosXCounter = 0
    #        tilePosYCounter+=1

    drawMap(screen)


    if keys[pygame.K_ESCAPE]:
        exitKey = True
        print("Exit Game...")

    pygame.display.update()
