

grey = (128,128,128)

class Person:
    def __init__(self, name, species, pos, color=grey):
        self.name = name
        self.species = species
        self.pos = pos
        self.startingPos = pos
        self.color = color

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

    def setDest(self, destination):
        self.dest = destination
