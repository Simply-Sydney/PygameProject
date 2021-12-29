import pygame
WHITE = (255,255,255)

class Player(pygame.sprite.Sprite):
	
	#Inherent stats
	oxygen = 100		#Self explanitory
	hitpoints = 100		#Hit point
	stamina = 100		#Out-of-breathness from doing actions
	endurance = 100		#Fatigue and other physical stress from the day
	freshness = 100		#Mental fatigue level, improved through shower / coffee / etc
	
	#Player basic stats
	Hel = 5				#Health (General healthiness level for event rolls)
	Str = 5				#Strength
	Int = 5				#Intelligence
	Cha = 5				#Charisma
	Wis = 5				#Wisdom
	Dex = 5				#Dexterity
	Con = 5				#Constitution
	Emp = 5				#Empathy
	
	#Player skills
	Hand2hand = 15
	Command = 15
	Survival = 15
	
	def __init__(self, color, width, height):
		#Call parant class (Sprite) constructor
		super().__init__()
		
		#Create surface of the player
		self.image = pygame.Surface([width, height])
		#Fill the image white
		self.image.fill(WHITE)
		#Set transparency to be white
		self.image.set_colorkey(WHITE)

		

		#Draw the player
		pygame.draw.rect(self.image, color, [0, 0, width, height])
		
		#Set the image of the player
		self.image = pygame.image.load("Player.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (128, 128))

		#Assign the image to self.rect
		self.rect = self.image.get_rect()
	
	#REMOVE LATER, PLAYER SHOULD ALWAYS BE CENTER
	def moveRight(self):
		self.image = pygame.image.load("Player-Right.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (128, 128))
		
	def moveLeft(self):
		self.image = pygame.image.load("Player-Left.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (128, 128))
		
	def moveDown(self):
		self.image = pygame.image.load("Player.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (128, 128))
	
	def moveUp(self):
		self.image = pygame.image.load("Player-Back.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (128, 128))
		
		