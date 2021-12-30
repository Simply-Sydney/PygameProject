from colors import *
import random
import maps
from AI import Pathing

class Person:
	def __init__(self, name, species, pos, color=grey):
		self.name = name
		self.species = species
		self.pos = pos
		self.startingPos = pos
		self.color = color
		self.path = []

	def setColor(self, color):
		self.color = color

	def getColor(self):
		return self.color

	def updatePos(self, pos):
		self.pos = pos

	def getPos(self, axis):
		if(axis == 'row'):
			return self.pos[0]
		elif(axis == 'col'):
			return self.pos[1]

	def getStartPos(self, axis):
		if(axis == 'row'):
			return self.startingPos[0]
		elif(axis == 'col'):
			return self.startingPos[1]



class AI(Person):
	def __init__(self, behaviour, name, species, pos, color=grey):
		Person.__init__(self, name, species, pos, color)
		self.behaviour = behaviour
		self.waitQ = 0
		self.dest = pos
		self.path = []

	def getWaitQ(self):
		return self.waitQ

	def setWaitQ(self, time):
		self.waitQ = time

	def waitQTick(self):
		if(self.waitQ > 0):
			self.waitQ -= 1

	def setPath(self, path):
		self.path = path
		
	def getPath(self):
		return self.path

	def setDest(self, destination):
		self.dest = destination
		
	def getDest(self):
		return self.dest
		
	def executeAction(self, mapList, mapOffsetColumn, mapOffsetRow):
		if(self.behaviour == 1):
		#Randomly wander action
			#Character is not done waiting
			if(self.getWaitQ() != 0):
				if(DEBUG):
					print("Waiting tick for " + self.name)
				self.waitQTick()
				return

			#Do one move
			if(DEBUG):
				print("Moving character " + self.name)
				print("Next Pos: ")
				print (self.path[0])
			self.updatePos((self.path[0][0]+mapOffsetRow,self.path[0][1]+mapOffsetColumn))
			self.startingPos = (self.path[0][0]+mapOffsetRow,self.path[0][1]+mapOffsetColumn)
			self.path.pop(0)
			
	def chooseDestination(self, mapList):
		newPathRow = random.randint(0,19)
		newPathCol = random.randint(0,19)
		while(mapList[newPathRow][newPathCol] == 1) or (mapList[newPathRow][newPathCol] == 0):
			newPathRow = random.randint(0,19)
			newPathCol = random.randint(0,19)
		self.setDest((newPathRow,newPathCol))
		return ((newPathRow,newPathCol))