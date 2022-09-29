import pygame
from pygame.locals import*
import json
from random import random

class Game:
	def __init__(self):
		self.model = Model()
		self.view = View(self.model)
		self.controller = Controller(self.model)

		pygame.init()

		self.clock = pygame.time.Clock()

	def run(self):
		while self.controller.running:
			self.update()

	def update(self):
		pass

		self.controller.update()
		self.model.update()
		self.view.update()

		self.clock.tick(40)

class View:
    size = width, height = 1000, 750

    def __init__(self, model):
        self.model = model
        self.screen = pygame.display.set_mode(self.size)
        self.blue = (0,0, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.purple = (200,100,230)

    def update(self):
        pygame.draw.rect(self.screen, self.blue, (1000 - self.model.cameraPosX, 0 - self.model.cameraPosY, 1000, 750))
        pygame.draw.rect(self.screen, self.purple, (0 - self.model.cameraPosX, 0 - self.model.cameraPosY, 1000, 750))
        pygame.draw.rect(self.screen, self.red, (0 - self.model.cameraPosX, 750 - self.model.cameraPosY, 1000, 750))
        pygame.draw.rect(self.screen, self.green, (1000 - self.model.cameraPosX, 750 - self.model.cameraPosY, 1000, 750))
        for sprite in self.model.sprites:
            sprite.drawImages(self.screen, self.model.cameraPosX, self.model.cameraPosY)

        pygame.display.update()

class Controller:
    def __init__(self, model):
        self.model = model
        self.key_right = False
        self.key_left = False
        self.key_up = False
        self.key_down = False 
        self.key_ctrl = False
        self.running = True


    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    self.model.sprites.append(Boomerang(self.model.link.x, self.model.link.y, self.model.link.w, self.model.link.h, self.model.link.D))

        self.key_right = pygame.key.get_pressed().__getitem__(pygame.K_RIGHT)
        self.key_left = pygame.key.get_pressed().__getitem__(pygame.K_LEFT)
        self.key_up = pygame.key.get_pressed().__getitem__(pygame.K_UP)
        self.key_down = pygame.key.get_pressed().__getitem__(pygame.K_DOWN)
        self.key_ctrl = pygame.key.get_pressed().__getitem__(pygame.K_LCTRL)

        if self.key_right:
            self.model.link.D = 3
            self.model.link.x += 10
            if(self.model.link.imageNum < 34 or self.model.link.imageNum >= 43):
                self.model.link.imageNum = 34
            self.model.link.imageNum+=1

        elif self.key_left:
            self.model.link.D = 2
            self.model.link.x -= 10
            if(self.model.link.imageNum < 14 or self.model.link.imageNum >= 23):
                self.model.link.imageNum = 14
            self.model.link.imageNum+=1

        elif self.key_up:
            self.model.link.D = 1
            self.model.link.y -= 10
            if(self.model.link.imageNum < 24 or self.model.link.imageNum >= 33):
                self.model.link.imageNum = 24
            self.model.link.imageNum+=1

        elif self.key_down:
            self.model.link.D = 4
            self.model.link.y += 10
            if(self.model.link.imageNum < 4 or self.model.link.imageNum >= 13):
                self.model.link.imageNum = 4
            self.model.link.imageNum+=1

class Sprite:
    def __init__(self, x, y, w, h, stype, D):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.stype = stype
        self.D = D
        self.counter = 0

    def updateSides(self):
        self.top = self.y
        self.bot = self.y + self.h
        self.left = self.x
        self.right = self.x + self.w
    
    def update(self):
        pass

    def loadImages(self, file_name):
        temp = pygame.image.load(file_name)
        temp = pygame.transform.smoothscale(temp, (50, 50))
        self.images.append(temp)

class Link(Sprite):
    def __init__(self, x, y, w, h, D):
        super().__init__(x, y, w, h, "Link", D)
        self.images = []
        self.imageNum = 0
        for i in range(0, 44):
            self.loadImages(f"./linkSprite/link ({i}).png")

    def drawImages(self, screen, cameraPosX, cameraPosY):
        screen.blit(self.images[self.imageNum], (self.x - cameraPosX, self.y - cameraPosY))
        
    def update(self):
        pass

class Brick(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "Brick", 0)
        self.images = []
        self.imageNum = 0
        self.loadImages("brick.jpg")
    
    def drawImages(self, screen, cameraPosX, cameraPosY):
        screen.blit(self.images[self.imageNum], (self.x - cameraPosX, self.y - cameraPosY))

    def update(self):
        pass

class Pot(Sprite):
    def __init__(self, x, y, w, h, D):
        super().__init__(x, y, w, h, "Pot", D)
        self.images = []
        self.imageNum = 0
        self.loadImages("pot.png")
        self.loadImages("pot_broken.png")
    
    def drawImages(self, screen, cameraPosX, cameraPosY):
        screen.blit(self.images[self.imageNum], (self.x - cameraPosX, self.y - cameraPosY))

    def update(self):
        if self.imageNum == 1:
            self.counter+=1
        if self.D == 3:
            self.x += 30
        elif self.D == 2:
            self.x -= 30
        elif self.D == 1:
            self.y -= 30
        elif self.D == 4:
            self.y += 30

class Boomerang(Sprite):
    def __init__(self, x, y, w, h, D):
        super().__init__(x, y, w, h, "Boomerang", D)
        self.images = []
        self.imageNum = 1
        for i in range(1, 5):
            self.loadImages(f"./boomerangSprite/boomerang{i}.png")

    def drawImages(self, screen, cameraPosX, cameraPosY):
        if(self.D > 0):
            screen.blit(self.images[self.D - 1], (self.x - cameraPosX, self.y - cameraPosY))

    def update(self):
        if(self.D == 3):
            self.x += 15
        if(self.D == 2):
            self.x -= 15
        if(self.D == 1):
            self.y -= 15
        if(self.D == 4):
            self.y += 15

class Model:
    def __init__(self):
        self.cameraPosX = 0
        self.cameraPosY = 0
        self.link = Link(110, 80, 50, 50, 0)
        self.sprites = []
        self.sprites.append(self.link)

        map = open("map.json")
        brickArr = json.load(map)
        for i in brickArr["bricks"]:
            self.sprites.append(Brick(i["x"], i["y"], i["w"], i["h"]))
        map.close()

        map = open("map.json")
        PotArr = json.load(map)
        for i in PotArr["pots"]:
            self.sprites.append(Pot(i["x"], i["y"], i["w"], i["h"], self.link.D))
        map.close()

    def update(self):
        self.roomChange()

        for sprite in self.sprites:
            sprite.update()
            sprite.updateSides()

        #Link and  Brick/Pot
        for sprite in self.sprites:
            if sprite.stype == "Brick" and self.checkCollisions(self.link, sprite):
                self.collisionGetOut(self.link, sprite)
            elif sprite.stype == "Pot" and self.checkCollisions(self.link, sprite):
                self.collisionGetOut(self.link, sprite)
                sprite.D = self.link.D

        #Pot and Brick
        for sprite in self.sprites:
            if sprite.stype == "Pot":
                for i in self.sprites:
                    if i.stype == "Brick":
                        if(self.checkCollisions(sprite, i)):
                            self.collisionGetOut(sprite, i)
                            sprite.imageNum = 1
        #Pot Removal
        for sprite in self.sprites:
            if sprite.stype == "Pot" and sprite.imageNum == 1:
                if sprite.counter >= 100:
                    self.sprites.remove(sprite)

        #Boomerang and Brick
        for sprite in self.sprites:
            if sprite.stype == "Boomerang":
                for i in self.sprites:
                    if i.stype == "Brick":
                        if(self.checkCollisions(sprite, i)):
                            self.sprites.remove(sprite)
                            break
        #Boomerand and Pot
        for sprite in self.sprites:
            if sprite.stype == "Boomerang":
                for i in self.sprites:
                    if i.stype == "Pot":
                        if(self.checkCollisions(sprite, i)):
                            self.collisionGetOut(sprite, i)
                            i.imageNum = 1
                            self.sprites.remove(sprite)
                            break


    def roomChange(self):
        if(self.link.x + self.link.w > 1000 and self.cameraPosX < 1000):
            self.cameraPosX += 10

        if(self.link.x < 1000 and self.cameraPosX > 0):
            self.cameraPosX -= 10

        if(self.link.y + self.link.h > 750 and self.cameraPosY < 750):
            self.cameraPosY += 10

        if(self.link.y < 750 and self.cameraPosY > 0):
            self.cameraPosY -= 10

    def checkCollisions(self, collider1, collider2):
        if(collider1.right < collider2.left or
            collider1.bot < collider2.top or
            collider1.top > collider2.bot or 
            collider1.left > collider2.right):
            return False
        else:
            return True
	
    def collisionGetOut(self, collider1, collider2):
        leftCollision = abs(collider1.left - collider2.right)
        botCollision = abs(collider1.top - collider2.bot)
        topCollision = abs(collider2.top - collider1.bot)
        rightCollision = abs(collider2.left - collider1.right)
        maxCollision = max(leftCollision, botCollision, topCollision, rightCollision)

        if leftCollision == maxCollision:
            collider1.x = collider2.left - collider1.w 

        if rightCollision == maxCollision:
            collider1.x = collider2.right

        if botCollision == maxCollision:
            collider1.y = collider2.top - collider1.h		

        if topCollision == maxCollision:
            collider1.y = collider2.bot 

game = Game()
game.run()